"""
IL-2 Sturmovik: Great Battles ``.wtr`` layer files: ``water.wtr`` (rivers,
reservoirs, lakes), ``forest_map.wtr`` / ``forest.wtr``, ``forest_cut.wtr``,
``debris/*.wtr``.

Worked out from the map files alone; no game code was read or disassembled.

Container (decoded completely, every byte accounted for on 15 files)
--------------------------------------------------------------------
The file is a pyramid of 4 levels written one after another, finest first.
Each level:

    u16  tiles_z, tiles_x       tile grid (columns east, rows north->south)
    u16  tile_dm                tile edge in decametres (1280 = 12.8 km)
    u8   0x29                   constant
    u8   codec                  1: blobs start 'ad 22/23' (most water.wtr)
                                0: blobs start '87 c3' (forest_cut, debris,
                                   one map family's water)
    tiles_x * tiles_z tiles, row-major, row 0 = north, column 0 = west:
        u8   present            0: empty tile, nothing follows
                                1: a block table follows
        u32  offset[N]          N = g*g blocks, g = tile_dm / 40, so a block
                                is 400 m at level 0 (800, 1600, 3200 m above)
        u16  size[N]            offset[i+1] = offset[i] + size[i]
        u8   empty[N]           1: nothing in the block; 0: something
        blob bytes              block i = blob[offset[i] : offset[i]+size[i]]

    block state:  empty=1                  -> 0 (land / no forest ...)
                  empty=0 and size=0       -> 2 (block fully covered)
                  empty=0 and size>0       -> 1 (partly covered; the blob
                                              holds the shape inside)

Blocks are row-major inside a tile, row 0 north.  Level 0 spans exactly the
heightmap: tiles * g * 400 m = width/height * cellSize on every map checked
(eleven maps of this install, one of them at 12.5 m cells).  So a level-0 block covers
400 / cellSize heightmap samples (8 at 50 m) and block (r, c) covers samples
rows r*8 .. r*8+7, columns c*8 .. c*8+7 (best correlation with the
height_w > height mask at zero shift; rivers line up on the hillshade).

Not decoded: the blob inside a partly covered block.  It is a bit stream
(MSB first); codec 1 blobs share a 15-bit prefix (ad 22/23 >> 1), an empty
block row repeats as the 17-bit unit 00000 111111111111, the stream parses
as Exp-Golomb codes into plausible small numbers, and identical bit runs
repeat for straight shores, so it is a row-wise entropy code of a finer
raster or of a per-pixel value; the row length and the run/value semantics
were not established.  ``info['blobs']`` keeps the raw blobs for later.

So ``read_wtr`` gives the exact water network at 400 m block resolution
(0 land, 1 shore/river block, 2 open water), and ``refine`` narrows the
partial blocks with the height_w > height mask.
"""
from __future__ import annotations

import struct

import numpy as np

__all__ = ["read_wtr", "read_levels", "refine", "LAND", "PARTIAL", "FULL"]

LAND, PARTIAL, FULL = 0, 1, 2


class WtrError(ValueError):
    pass


def read_levels(data: bytes) -> list[dict]:
    """All pyramid levels with their raw block tables (no blob decoding)."""
    data = bytes(data)
    out = []
    p = 0
    while p + 8 <= len(data):
        tz, tx, tile_dm, const, codec = struct.unpack_from("<HHHBB", data, p)
        if tile_dm % 40 or not tz or not tx:
            raise WtrError(f"bad level header at {p}")
        g = tile_dm // 40
        n = g * g
        q = p + 8
        tiles = []
        for _ in range(tx * tz):
            if q >= len(data):
                raise WtrError("truncated")
            flag = data[q]
            if flag == 0:
                tiles.append(None)
                q += 1
                continue
            if flag != 1:
                raise WtrError(f"tile flag {flag} at {q}")
            off = np.frombuffer(data, "<u4", n, q + 1).astype(np.int64)
            sz = np.frombuffer(data, "<u2", n, q + 1 + 4 * n).astype(np.int64)
            empty = np.frombuffer(data, "u1", n, q + 1 + 6 * n)
            blob0 = q + 1 + 7 * n
            if n > 1 and not np.array_equal(off[1:], off[:-1] + sz[:-1]):
                raise WtrError(f"offset table inconsistent at {q}")
            tiles.append({"offset": off, "size": sz, "empty": empty, "blob_start": blob0})
            q = blob0 + int(off[-1] + sz[-1])
        out.append({"at": p, "tiles_z": tz, "tiles_x": tx, "tile_m": tile_dm * 10.0, "const": const,
                    "codec": codec, "g": g, "block_m": tile_dm * 10.0 / g, "tiles": tiles, "end": q})
        p = q
    if p != len(data):
        raise WtrError(f"{len(data) - p} trailing bytes")
    return out


def read_wtr(data: bytes, level: int = 0, cell: float | None = 50.0, keep_blobs: bool = False):
    """Decode the block classification of a .wtr file.

    Returns (mask uint8, info).  mask values: 0 LAND (nothing), 1 PARTIAL
    (shore / river / partly covered block), 2 FULL (block fully water or
    forest ...).  With ``cell`` (the heightmap's cellSize, 50 or 12.5) the
    mask is expanded to the heightmap grid: [rows, cols], row 0 north,
    column 0 west, the same indexing as height.dat (level 0 only lines up
    exactly; higher levels may overhang the map at the south/east edge and
    are cropped to whole tiles).  With ``cell=None`` the mask is per block.

    info: tiles, g, block_m, codec, levels (count), block_shape, and with
    ``keep_blobs`` a dict {(block_row, block_col): bytes} of partial blocks."""
    data = bytes(data)
    levels = read_levels(data)
    lv = levels[level]
    g, tz, tx = lv["g"], lv["tiles_z"], lv["tiles_x"]
    grid = np.zeros((tx * g, tz * g), np.uint8)
    blobs = {} if keep_blobs else None
    for k, t in enumerate(lv["tiles"]):
        if t is None:
            continue
        r0, c0 = (k // tz) * g, (k % tz) * g
        st = np.where(t["empty"] == 1, LAND, np.where(t["size"] > 0, PARTIAL, FULL)).astype(np.uint8)
        grid[r0:r0 + g, c0:c0 + g] = st.reshape(g, g)
        if keep_blobs:
            for i in np.nonzero(t["size"])[0]:
                a = t["blob_start"] + int(t["offset"][i])
                blobs[(r0 + i // g, c0 + i % g)] = data[a:a + int(t["size"][i])]
    info = {"levels": len(levels), "level": level, "tiles": (tx, tz), "g": g, "block_m": lv["block_m"],
            "codec": lv["codec"], "block_shape": grid.shape,
            "counts": {"land": int((grid == LAND).sum()), "partial": int((grid == PARTIAL).sum()),
                       "full": int((grid == FULL).sum())}}
    if blobs is not None:
        info["blobs"] = blobs
    if cell is None:
        return grid, info
    spb = lv["block_m"] / cell
    if abs(spb - round(spb)) > 1e-6:
        raise WtrError(f"block of {lv['block_m']} m is not a whole number of {cell} m cells")
    spb = int(round(spb))
    info["samples_per_block"] = spb
    return np.repeat(np.repeat(grid, spb, 0), spb, 1), info


def refine(mask: np.ndarray, height_raw: np.ndarray, water_raw: np.ndarray, *,
           spb: int = 8, lake_fill: bool = True, keep_rough_bodies: int = 0) -> np.ndarray:
    """Binary water mask on the heightmap grid from read_wtr's level-0 mask
    (expanded, ``spb`` samples per block) and the raw height.dat /
    height_w.dat arrays (same grid):

    - FULL blocks are water, LAND blocks are dry;
    - PARTIAL blocks are water where height_w > height (rivers carry their
      own water level there);
    - with ``lake_fill``, a PARTIAL block next to FULL blocks is also water
      where the terrain is no higher than the lake: the 90th percentile of
      the terrain in the neighbouring FULL blocks (lakes that height_w does
      not hold);
    - ``keep_rough_bodies`` > 0 also keeps height_w > height components of at
      least that many samples inside LAND blocks (needs scipy).

    The exact shore inside PARTIAL blocks is in the undecoded blobs; this is
    the best stand-in found."""
    R, C = mask.shape
    h = height_raw[:R, :C]
    w = water_raw[:R, :C]
    rough = w > h
    out = (mask == FULL) | ((mask == PARTIAL) & rough)
    if lake_fill and (mask == FULL).any():
        br, bc = R // spb, C // spb
        blk = mask[: br * spb: spb, : bc * spb: spb]
        hb = h[: br * spb, : bc * spb].reshape(br, spb, bc, spb)
        p90 = np.percentile(hb, 90, axis=(1, 3))
        lvl = np.full((br, bc), -1.0)
        full = blk == FULL
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                sf = np.zeros_like(full)
                sp = np.full((br, bc), -1.0)
                rs = slice(max(dr, 0), br + min(dr, 0))
                rd = slice(max(-dr, 0), br + min(-dr, 0))
                cs = slice(max(dc, 0), bc + min(dc, 0))
                cd = slice(max(-dc, 0), bc + min(-dc, 0))
                sf[rd, cd] = full[rs, cs]
                sp[rd, cd] = p90[rs, cs]
                lvl = np.where(sf, np.maximum(lvl, sp), lvl)
        cand = (blk == PARTIAL) & (lvl >= 0)
        L = np.repeat(np.repeat(np.where(cand, lvl, -1.0), spb, 0), spb, 1)
        sub = out[: br * spb, : bc * spb]
        sub |= (L >= 0) & (h[: br * spb, : bc * spb] <= L)
    if keep_rough_bodies:
        from scipy import ndimage
        lab, n = ndimage.label(rough & (mask == LAND))
        if n:
            sizes = np.bincount(lab.ravel())
            big = sizes >= keep_rough_bodies
            big[0] = False
            out |= big[lab]
    return out.astype(np.uint8)
