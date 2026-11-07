"""
An IL-2 map into the 3DHeat level contract: `ground:<map>` and `water:<map>`
in one `.glb`, with a `.json` beside it that ties the map to the earth.

**Where things are.** A map's `height.hini` gives the latitude and longitude of
its four corners (`MapNW`, `MapNE`, `MapSE`, `MapSW`). Each heightmap sample is
placed by bilinear interpolation between them (row 0 is the north edge, column
0 the west edge; checked on one map against eight known towns, coasts and seas).
Two frames:

- `enu` (default): metres east, altitude, north of an origin, the flat map the
  3DHeat Watcher puts an IL-2 Tacview recording in (`TANGENT_AXES`: x east,
  y altitude, z north, drawn with z mirrored). The glb stores (east, altitude,
  -north), so a recording converted with the same origin (its session's `geo`,
  `--origin <lat> <lon>`) lands on the level. Without `--origin`, the map's
  centre is the origin, and the JSON says so.
- `game`: the game's own metres, as mission files have them: x north from the
  south edge, y the game's height, z east from the west edge. Right-handed as it
  is, so the glb stores (x, y, z).

**Heights.** raw * heightMul / 256 is the game's internal height; the altitude
above sea level subtracts SeaLevel * heightMul (both from height.hini; one
map's file comments its SeaLevel as "-50m", and with it the map's heights come
out at the real range of the region).

**Water.** The map's water map (`height_w.dat`, same codec) holds a water
surface; where it is above the ground there is water: rivers, lakes, the sea.
Each cell of the output grid with water in it becomes a flat quad at the water's
height. Maps without a water map get the sea, at sea level, where the ground is
below it.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import __version__
from .glb import Part, write_glb
from .gtp import Entry
from .heightdat import iter_bands, parse_header, read_sampled
from .hini import Hini, parse_hini

DEFAULT_MAX_GRID = 1024
WGS84_A = 6378137.0
WGS84_E2 = 6.69437999014e-3


@dataclass
class MapSource:
    name: str  # the landscape folder's name
    hini: Hini | None
    height: Entry
    water: Entry | None
    game: str  # "Great Battles" or "Korea"
    #: Game metres (x north, z east) to east/north metres about `origin`, as a 3x2 matrix
    #: applied to (x, z, 1): for a map whose height.hini cannot be read (Korea).
    affine: dict | None = None
    #: Height settings where there is no height.hini to give them: heightMul, SeaLevel.
    heights: dict | None = None
    notes: list[str] = field(default_factory=list)

    def corners(self) -> dict[str, tuple[float, float]] | None:
        """The four corners' (lat, lon), if the map's height.hini gives them."""
        return self.hini.corners() if self.hini else None


def bilinear_latlon(corners: dict[str, tuple[float, float]], u: np.ndarray, v: np.ndarray):
    """(lat, lon) at fractions u (west to east) and v (north to south) of the map."""
    nw, ne, se, sw = (np.array(corners[k], np.float64) for k in ("MapNW", "MapNE", "MapSE", "MapSW"))
    u, v = u[..., None], v[..., None]
    top = nw + (ne - nw) * u
    bottom = sw + (se - sw) * u
    ll = top + (bottom - top) * v
    return ll[..., 0], ll[..., 1]


def _ecef(lat, lon):
    p, l = np.radians(lat), np.radians(lon)
    n = WGS84_A / np.sqrt(1 - WGS84_E2 * np.sin(p) ** 2)
    return n * np.cos(p) * np.cos(l), n * np.cos(p) * np.sin(l), n * (1 - WGS84_E2) * np.sin(p)


def tangent(lat, lon, lat0: float, lon0: float):
    """East and north metres of (lat, lon) from (lat0, lon0) on the WGS-84 tangent plane - the watcher's `Tangent`."""
    x, y, z = _ecef(lat, lon)
    x0, y0, z0 = _ecef(np.float64(lat0), np.float64(lon0))
    dx, dy, dz = x - x0, y - y0, z - z0
    p, l = math.radians(lat0), math.radians(lon0)
    east = -math.sin(l) * dx + math.cos(l) * dy
    north = -math.sin(p) * math.cos(l) * dx - math.sin(p) * math.sin(l) * dy + math.cos(p) * dz
    return east, north


def inverse_tangent(east, north, lat0: float, lon0: float, iterations: int = 6):
    """(lat, lon) whose `tangent` is (east, north): Newton steps from a spherical first guess."""
    east = np.asarray(east, np.float64)
    north = np.asarray(north, np.float64)
    r = 6371000.0
    lat = lat0 + np.degrees(north / r)
    lon = lon0 + np.degrees(east / (r * np.cos(np.radians(lat))))
    h = 1e-5
    for _ in range(iterations):
        e0, n0 = tangent(lat, lon, lat0, lon0)
        e1, n1 = tangent(lat + h, lon, lat0, lon0)
        e2, n2 = tangent(lat, lon + h, lat0, lon0)
        a, b, c, d = (e1 - e0) / h, (e2 - e0) / h, (n1 - n0) / h, (n2 - n0) / h
        de, dn = east - e0, north - n0
        det = a * d - b * c
        lat = lat + (d * de - b * dn) / det
        lon = lon + (-c * de + a * dn) / det
    return lat, lon


def corners_fit_size(corners: dict[str, tuple[float, float]], width_m: float, height_m: float) -> bool:
    """Whether the corners span about the map's own size (some maps carry another map's corners)."""
    def dist(a, b):
        e, n = tangent(np.array(b[0]), np.array(b[1]), a[0], a[1])
        return float(np.hypot(e, n))
    ew = dist(corners["MapNW"], corners["MapNE"])
    ns = dist(corners["MapNW"], corners["MapSW"])
    return 0.8 < ew / width_m < 1.25 and 0.8 < ns / height_m < 1.25


def _grid_faces(nr: int, nc: int) -> np.ndarray:
    r, c = np.meshgrid(np.arange(nr - 1), np.arange(nc - 1), indexing="ij")
    a = (r * nc + c).ravel()
    b, d, e = a + 1, a + nc, a + nc + 1
    return np.concatenate([np.stack([a, d, b], 1), np.stack([b, d, e], 1)]).astype(np.uint32)


def _water_cells(height: Entry, water: Entry, rows: np.ndarray, cols: np.ndarray, w: int, h: int):
    """Per output cell: how many full-resolution samples have water, and their mean water level (raw)."""
    nr, nc = len(rows) - 1, len(cols) - 1
    count = np.zeros((nr, nc), np.int64)
    total = np.zeros((nr, nc), np.float64)
    # Which output cell each full-resolution row and column falls in.
    col_cell = np.clip(np.searchsorted(cols, np.arange(w), side="right") - 1, 0, nc - 1)
    row_cell = np.clip(np.searchsorted(rows, np.arange(h), side="right") - 1, 0, nr - 1)
    for (r0, g), (_, wt) in zip(iter_bands(height.read()), iter_bands(water.read())):
        wet = wt.astype(np.int32) > g.astype(np.int32)
        if not wet.any():
            continue
        rr, cc = np.nonzero(wet)
        cr, ccell = row_cell[rr + r0], col_cell[cc]
        np.add.at(count, (cr, ccell), 1)
        np.add.at(total, (cr, ccell), wt[rr, cc].astype(np.float64))
    level = np.where(count > 0, total / np.maximum(count, 1), np.nan)
    return count, level


def build(src: MapSource, out_dir: Path, *, max_grid: int = DEFAULT_MAX_GRID, frame: str = "enu",
          origin: tuple[float, float] | None = None, water: bool = True, log=print) -> dict:
    t0 = time.time()
    out_dir.mkdir(parents=True, exist_ok=True)
    hini = src.hini
    settings = src.heights or {}
    mul = (hini.number("heightMul", None) if hini else None) or settings.get("heightMul") or 1.0
    sea = hini.number("SeaLevel", None) if hini else None
    if sea is None:
        sea = settings.get("SeaLevel", 0.0)
    payload = src.height.read()
    hd = parse_header(payload)
    w, h, cell = hd["width"], hd["height"], float(hd["cell_size"])
    notes = list(src.notes)
    corners = src.corners()
    if corners and not corners_fit_size(corners, (w - 1) * cell, (h - 1) * cell):
        notes.append("height.hini's corner coordinates do not span this map's size (they look copied from "
                     "another map) and are not used")
        corners = None
    placed = corners is not None or src.affine is not None
    if frame == "enu" and not placed:
        notes.append("no way to place the map on the earth: written in the game's own metres instead")
        frame = "game"
    step = max(1, int(math.ceil(max(w, h) / max_grid)))
    log(f"  {src.name}: {w}x{h} samples at {cell:g} m, every {step}")
    raw, cols, rows, decoded = read_sampled(payload, step)
    del payload
    internal = raw.astype(np.float64) * mul / 256.0
    altitude = internal - sea * mul
    gx = ((h - 1) - rows[:, None]) * cell + 0.0 * cols[None, :]  # game x: north from the south edge
    gz = cols[None, :] * cell + 0.0 * rows[:, None]  # game z: east from the west edge

    def latlon(x, z):
        if corners is not None:
            return bilinear_latlon(corners, z / ((w - 1) * cell), ((h - 1) * cell - x) / ((h - 1) * cell))
        m = np.array(src.affine["matrix"], np.float64)
        e = x * m[0, 0] + z * m[1, 0] + m[2, 0]
        n = x * m[0, 1] + z * m[1, 1] + m[2, 1]
        return inverse_tangent(e, n, *src.affine["origin"])

    record: dict = {
        "format": "heat3d-il2-level",
        "tool": f"heat3d-il2-level {__version__}",
        "game": src.game,
        "map": src.name,
        "files": {"height": src.height.name or f"{src.height.archive.name}@{src.height.offset}",
                  "water": (src.water.name or f"{src.water.archive.name}@{src.water.offset}") if src.water else None},
        "heightmap": {"samples": [w, h], "cell": cell, "step": step, "heightMul": mul, "seaLevel": sea,
                      "metres": "altitude = raw * heightMul / 256 - SeaLevel * heightMul",
                      "settingsFrom": "height.hini" if hini else "estimated (see notes)",
                      "sectors": hd["sectors_x"] * hd["sectors_y"], "badSectors": decoded["bad_sectors"],
                      "suspiciousSectors": decoded["suspicious_sectors"]},
        "notRead": ["buildings, towns and airfields (towns.mesh and the Locations archives are not read)",
                    "forests (forest_map.wtr)", "the ground's textures"],
    }
    if hini:
        lim = {k: hini.number(k) for k in ("limitMinX", "limitMinZ", "limitMaxX", "limitMaxZ")}
        record["playArea"] = {"gameMetres": lim, "note": "x north from the south edge, z east from the west edge"}
    if placed:
        xs = np.array([(h - 1) * cell, (h - 1) * cell, 0.0, 0.0])
        zs = np.array([0.0, (w - 1) * cell, (w - 1) * cell, 0.0])
        la, lo = latlon(xs, zs)
        names = ("MapNW", "MapNE", "MapSE", "MapSW")
        record["corners"] = {k: {"lat": round(float(a), 6), "lon": round(float(b), 6)} for k, a, b in zip(names, la, lo)}
        record["extent"] = {"south": round(float(la.min()), 6), "north": round(float(la.max()), 6),
                            "west": round(float(lo.min()), 6), "east": round(float(lo.max()), 6)}
        if corners is not None:
            record["georeference"] = ("height.hini's MapNW/NE/SE/SW: each sample placed by bilinear interpolation "
                                      "of the corners (row 0 north, column 0 west)")
        else:
            record["georeference"] = {"method": "affine fit of the game's metres to real landmarks", **src.affine}
    if notes:
        record["notes"] = notes

    if frame == "enu":
        lat, lon = latlon(gx, gz)
        if origin is None:
            c_lat, c_lon = latlon(np.array((h - 1) * cell / 2), np.array((w - 1) * cell / 2))
            origin = (round(float(c_lat), 6), round(float(c_lon), 6))
        east, north = tangent(lat, lon, *origin)

        def to_xyz(y):
            return np.stack([np.broadcast_to(east, y.shape).ravel(), y.ravel(),
                             -np.broadcast_to(north, y.shape).ravel()], 1)

        heights = altitude
        record["frame"] = {"name": "enu", "origin": {"lat": origin[0], "lon": origin[1]},
                           "axes": "glb (x, y, z) = (east, altitude above sea level, -north) metres from the origin: "
                                   "the 3DHeat Watcher's Tacview flat map with its flipZ; convert a recording with "
                                   "the same origin (its session geo) and it lands on the level"}
        record["geo"] = {"lat0": origin[0], "lon0": origin[1]}
    else:
        def to_xyz(y):
            return np.stack([np.broadcast_to(gx, y.shape).ravel(), y.ravel(),
                             np.broadcast_to(gz, y.shape).ravel()], 1)

        heights = internal
        record["frame"] = {"name": "game",
                           "axes": "glb (x, y, z) = game (x north from the south edge, y the game's height, "
                                   "z east from the west edge) metres; altitude = y - SeaLevel * heightMul"}

    verts = to_xyz(heights).astype(np.float32)
    faces = _grid_faces(len(rows), len(cols))
    # Make the ground face up whatever the frame did to the winding.
    n = np.cross(verts[faces[:10, 1]] - verts[faces[:10, 0]], verts[faces[:10, 2]] - verts[faces[:10, 0]])
    if n[:, 1].sum() < 0:
        faces = faces[:, [0, 2, 1]]
    positions = [verts]
    parts = [Part(name=f"ground:{src.name}", faces=faces, colour=(0.42, 0.40, 0.34))]
    record["parts"] = {"ground": {"triangles": int(len(faces)), "height": [float(heights.min()), float(heights.max())]}}

    if water:
        nr, nc = len(rows) - 1, len(cols) - 1
        offset = sea * mul if frame == "enu" else 0.0
        if src.water is not None:
            count, level_raw = _water_cells(src.height, src.water, rows, cols, w, h)
            # A cell is water where at least half its samples are: "any" floods every low field that
            # touches a stream once the grid is coarser than the water map.
            cells = np.diff(rows)[:, None] * np.diff(cols)[None, :]
            wet = count >= 0.5 * np.maximum(cells, 1)
            level = level_raw * mul / 256.0 - offset
        else:
            lowest = np.minimum(np.minimum(heights[:-1, :-1], heights[1:, :-1]),
                                np.minimum(heights[:-1, 1:], heights[1:, 1:]))
            wet = lowest < sea * mul - offset
            level = np.full((nr, nc), sea * mul - offset)
        rr, cc = np.nonzero(wet)
        if len(rr):
            corner_r = np.stack([rr, rr, rr + 1, rr + 1], 1).ravel()
            corner_c = np.stack([cc, cc + 1, cc + 1, cc], 1).ravel()
            base = to_xyz(np.zeros_like(heights)).reshape(len(rows), len(cols), 3)
            wv = base[corner_r, corner_c].astype(np.float64)
            wv[:, 1] = np.repeat(level[rr, cc], 4)
            k = np.arange(len(rr), dtype=np.uint32) * 4
            wf = np.concatenate([np.stack([k, k + 3, k + 1], 1), np.stack([k + 1, k + 3, k + 2], 1)])
            nn = np.cross(wv[wf[:1, 1]] - wv[wf[:1, 0]], wv[wf[:1, 2]] - wv[wf[:1, 0]])
            if nn[0, 1] < 0:
                wf = wf[:, [0, 2, 1]]
            off = sum(len(p) for p in positions)
            positions.append(wv.astype(np.float32))
            parts.append(Part(name=f"water:{src.name}", faces=(wf + off).astype(np.uint32), colour=(0.16, 0.30, 0.42)))
            record["parts"]["water"] = {"cells": int(len(rr)), "of": int(nr * nc),
                                        "source": "water map" if src.water is not None else "sea level"}

    glb_path = out_dir / f"{src.name}.glb"
    tmp = glb_path.with_suffix(".glb.part")
    write_glb(tmp, np.concatenate(positions), parts=parts)
    tmp.replace(glb_path)
    record["seconds"] = round(time.time() - t0, 1)
    (out_dir / f"{src.name}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record
