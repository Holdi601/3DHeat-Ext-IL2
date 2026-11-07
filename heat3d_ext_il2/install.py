"""
Where IL-2 is installed, and which maps it has.

Great Battles: every `height.hini` in the archives is a map (seasons of one map
are separate entries that usually share one heightmap). IL-2 Series (Korea):
the archives have no readable names, so its heightmaps are found by their
header (a `height.dat` layout with sectors of 128 samples), and it ships no
readable `height.hini`, so its maps have no corner coordinates here.
"""

from __future__ import annotations

import os
import re
import struct
from pathlib import Path

import numpy as np

from .gtp import Entry, read_table, scan_chain
from .hini import parse_hini
from .level import MapSource

_LIBRARY_PATH = re.compile(r'"path"\s*"([^"]+)"')
_STEAM_DEFAULTS = (r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam")
_FOLDERS = ("IL-2 Sturmovik Battle of Stalingrad", "IL-2 Sturmovik Great Battles", "IL2Series")


def steam_libraries() -> list[Path]:
    roots: list[Path] = []
    seen: set[str] = set()
    for base in _STEAM_DEFAULTS:
        try:
            text = (Path(base) / "config" / "libraryfolders.vdf").read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for found in _LIBRARY_PATH.finditer(text):
            p = Path(found.group(1).replace("\\\\", "\\"))
            if str(p).lower() not in seen:
                seen.add(str(p).lower())
                roots.append(p)
    return roots


def find_installs(given: list[str] | None = None) -> list[Path]:
    """Every IL-2 folder found: the ones given (`--game`, `HEAT3D_IL2_GAME`), else Steam's."""
    out: list[Path] = []
    wanted = list(given or [])
    if os.environ.get("HEAT3D_IL2_GAME"):
        wanted += os.environ["HEAT3D_IL2_GAME"].split(os.pathsep)
    cands = [Path(g) for g in wanted] or [lib / "steamapps" / "common" / f for lib in steam_libraries() for f in _FOLDERS]
    for c in cands:
        if (c / "data").is_dir() and any((c / "data").glob("Maps*.gtp")) and c not in out:
            out.append(c)
    return out


def _game_name(root: Path) -> str:
    return "Korea" if (root / "bin" / "game" / "IL2Series.exe").exists() else "Great Battles"


def maps_great_battles(root: Path) -> list[MapSource]:
    files: dict[str, Entry] = {}
    for archive in sorted((root / "data").glob("*.gtp")):
        if not archive.name.lower().startswith(("maps", "locations")):
            continue
        for e in read_table(archive):
            files.setdefault(e.name, e)
    out: list[MapSource] = []
    for name, e in sorted(files.items()):
        if not name.endswith("/height.hini"):
            continue
        hini = parse_hini(e.read())
        hm = files.get(hini.path("height_map") or "")
        if hm is None:
            continue
        wm = files.get(hini.path("water_map") or "")
        out.append(MapSource(name.split("/")[-2], hini, hm, wm, "Great Battles"))
    return out


def maps_korea(root: Path) -> list[MapSource]:
    """The Korea map: its heightmap and water map (found by their header), placed by `korea.py`."""
    found: list[tuple[Entry, tuple]] = []
    for archive in sorted((root / "data").glob("Maps*.gtp")):
        with archive.open("rb") as fh:
            for e in scan_chain(archive):
                if e.size < 1 << 20:
                    continue
                fh.seek(e.offset + 32)
                head = fh.read(32)
                w, h, sx, sy, ss = struct.unpack_from("<5I", head, 0)
                (cell,) = struct.unpack_from("<f", head, 20)
                if ss == 128 and 0 < w <= sx * ss and 0 < h <= sy * ss and sx * ss - w < ss and 1 <= cell <= 5000:
                    found.append((e, (w, h, cell)))
    if not found:
        return []
    # The largest file is the terrain; one of the same shape and much smaller is the water map
    # (flat patches compress well). Copies in several archives are the same file.
    found.sort(key=lambda t: -t[0].size)
    height, shape = found[0]
    water = next((e for e, s in found if s == shape and e.size < height.size // 4), None)
    from . import korea
    from .heightdat import read_sampled

    airfields, ship_y = korea.mission_objects(root)
    affine = korea.fit_affine(airfields)
    mode = None
    if water is not None:
        sample, *_ = read_sampled(water.read(), 64)
        vals, counts = np.unique(sample[sample > 0], return_counts=True)
        mode = int(vals[counts.argmax()]) if len(vals) else None
    settings = korea.sea_settings(ship_y, mode)
    notes = []
    if affine:
        notes.append(f"placed by fitting {len(affine['landmarks'])} airfields of the game's missions to the real "
                     f"airfields (rms {affine['rmsMetres']} m)")
    if settings:
        notes.append(f"heightMul {settings['heightMul']} and SeaLevel {settings['SeaLevel']:.4f} estimated: "
                     + settings["from"])
    else:
        notes.append("height scale unknown (no ships on the water in the missions): heights are raw / 256")
    w, h, cell = shape
    return [MapSource("korea", None, height, water, "Korea", affine=affine, heights=settings, notes=notes)]


def all_maps(roots: list[Path]) -> list[MapSource]:
    out: list[MapSource] = []
    for r in roots:
        out += maps_korea(r) if _game_name(r) == "Korea" else maps_great_battles(r)
    return out
