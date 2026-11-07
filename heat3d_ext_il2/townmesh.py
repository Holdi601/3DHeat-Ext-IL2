"""
IL-2 Sturmovik: Great Battles ground-decal meshes: ``towns.mesh``,
``cities.mesh``, ``city.mesh``, ``city_finn.mesh``, ``city_ussr.mesh`` (and,
with the same layout, ``roads_fields.mesh``, ``nature.mesh``,
``sand_swamp.mesh``, ``rivers_area.mesh`` ...).

Worked out from the map files alone; no game code was read or disassembled.

What they are
-------------
Flat, textured ground overlays, not buildings: every vertex has y = 0 and the
polygons are draped on the terrain by the game.  Each draw record names a
texture triple from the file's own table (diffuse, ``_nm`` normal map,
``_aux``), e.g. ``village_11.dds``, ``ground_city_01.dds``,
``ground_industrial_01_300m.dds``, ``lay_vil_lin_01.dds`` (village layouts),
``field_03.dds``, ``ground_railroads_ways.dds``.  The town records are the
built-up footprints of towns and villages; other records in the same file
are fields, forest floor, paths and railway ground.

File layout (little endian)
---------------------------
    u8   version                 1
    u32  table_offset            absolute offset of the tile index
    f32  tile_size               25600.0 (metres)
    u32  tiles_x, tiles_z        tile grid, = floor(map extent / 25600) + 2
    chunks, one per non-empty tile, until table_offset:
        u16  tx, tz              tile index (tx along game x = north, tz along z = east)
        u8   0x80 | n_records
        n_records x 28 bytes:
            u16  tex[8]          texture-table ids, 0xFFFF = unused;
                                 [0] diffuse, [1] normal map, [3] aux
            u32  flags           material / layer flags (low byte 0)
            u32  first_index     into this chunk's index list
            u32  index_count     triangles * 3
        u32  n_vertices
        n_vertices x 44 bytes:
            f32  x, y, z         tile-local metres, y always 0
            f32  u0, v0, u1, v1  texture coordinates (u1,v1 repeat u0,v0 so far)
            f32  dx, dz          unit vector in the ground plane (texture direction)
            u8   r, g, b, a      vertex colour (a = blend weight)
            u32  extra           packed bytes, meaning unknown
        u32  n_indices
        u16  indices[n_indices]  triangle list, local to the chunk
    at table_offset:
        u16  n_tiles; n_tiles x (u32 tx * tiles_z + tz, u32 chunk offset)
        u16  n_textures; n_textures x (u16 id, u8 len, char path[len] incl. NUL, u32 0)

Coordinates
-----------
The tile grid has a one-tile border on the low side: tile (tx, tz) is centred
on game (x, z) = ((tx - 0.5) * tile_size, (tz - 0.5) * tile_size), so

    game_x (north, from the south edge) = (tx - 0.5) * tile_size + local_x
    game_z (east, from the west edge)   = (tz - 0.5) * tile_size + local_z

Checked by overlaying the decals on the heightmap hillshade and the water
mask of three maps (one square, one not): town and field edges follow the
river banks; a centred-grid
alternative (shift 6400 m) and a 12800 m shift are visibly wrong.
"""
from __future__ import annotations

import struct

import numpy as np

__all__ = ["read_town_mesh", "texture_category"]

VERTEX_DTYPE = np.dtype([
    ("pos", "<f4", 3), ("uv0", "<f4", 2), ("uv1", "<f4", 2), ("dir", "<f4", 2),
    ("rgba", "u1", 4), ("extra", "<u4"),
])
assert VERTEX_DTYPE.itemsize == 44



def texture_category(path: str | None) -> str:
    """'town', 'industrial', 'forest', 'road' or 'ground', from a texture file name.

    Names seen across the maps: ground_city_*, town_NN, town_med/lrg, village_NN,
    villages_bg, lay_vil_*/lay_twn_*/lay_cnt_* (settlement layouts) -> town;
    ground_industrial_*, factory_zone*, port -> industrial; town_forest,
    ground_forest_*, carpet_forest -> forest; *road*, *pathway*, *railroads*,
    line_road_* -> road; fields, gardens, grass, sand, soil ... -> ground."""
    n = (path or "").lower().replace("\\", "/").rsplit("/", 1)[-1]
    if any(k in n for k in ("industrial", "factory", "port")):
        return "industrial"
    if "forest" in n:
        return "forest"
    if "city" not in n and any(k in n for k in ("road", "path", "rail", "_way", "way_")):
        return "road"
    if any(k in n for k in ("city", "town", "vil", "lay_twn", "lay_cnt", "mansion")) and not any(
            k in n for k in ("sand", "grass")):
        return "town"
    return "ground"


class TownMeshError(ValueError):
    pass


def _textures(data: bytes, p: int) -> dict[int, str]:
    (n,) = struct.unpack_from("<H", data, p)
    p += 2
    tex: dict[int, str] = {}
    for _ in range(n):
        if p + 3 > len(data):
            break
        i, ln = struct.unpack_from("<HB", data, p)
        p += 3
        tex[i] = data[p:p + ln].split(b"\0")[0].decode("cp1251", "replace").replace("\\", "/")
        p += ln + 4
    return tex


def read_town_mesh(data: bytes, *, town_only: bool = False):
    """Decode a ground-decal .mesh file.

    Returns (vertices float32 [N, 3] in game metres as (x north, y = 0, z east),
    faces int32 [M, 3], info).  ``info`` holds:
      - ``tile_size``, ``tiles``: header values
      - ``textures``: {id: path}
      - ``face_texture``: int32 [M], diffuse texture id of each face (-1 none)
      - ``face_category``: per-face texture_category() of the diffuse texture
      - ``face_is_town``: bool [M], category 'town' or 'industrial' (built-up)
      - ``uv`` float32 [N, 2], ``rgba`` uint8 [N, 4], ``dir`` float32 [N, 2]
      - ``records``: list of dicts (tile, textures, flags, faces slice)
    With ``town_only=True`` only faces whose texture marks built-up ground are
    returned (vertices are compacted accordingly)."""
    data = bytes(data)
    if len(data) < 17 or data[0] != 1:
        raise TownMeshError("not a ground-decal mesh (version byte != 1)")
    _, table, tile, nx, nz = struct.unpack_from("<BIfII", data, 0)
    if not (17 <= table <= len(data)) or tile <= 0:
        raise TownMeshError("bad header")
    textures = _textures(data, table + 2 + 8 * struct.unpack_from("<H", data, table)[0])

    verts, uvs, rgbas, dirs, faces, ftex = [], [], [], [], [], []
    records = []
    base = 0
    nface = 0
    p = 17
    while p < table:
        tx, tz, nr = struct.unpack_from("<HHB", data, p)
        p += 5
        if not nr & 0x80:
            raise TownMeshError(f"record count byte without 0x80 at {p - 1}")
        recs = []
        for _ in range(nr & 0x7F):
            ids = struct.unpack_from("<8H", data, p)
            flags, first, count = struct.unpack_from("<III", data, p + 16)
            recs.append((ids, flags, first, count))
            p += 28
        (nv,) = struct.unpack_from("<I", data, p)
        p += 4
        v = np.frombuffer(data, VERTEX_DTYPE, nv, p)
        p += 44 * nv
        (ni,) = struct.unpack_from("<I", data, p)
        p += 4
        idx = np.frombuffer(data, "<u2", ni, p).astype(np.int32)
        p += 2 * ni
        if ni and idx.max() >= nv:
            raise TownMeshError(f"tile {tx},{tz}: index out of range")
        pos = v["pos"].astype(np.float64)
        g = np.empty((nv, 3), np.float32)
        g[:, 0] = (tx - 0.5) * tile + pos[:, 0]
        g[:, 1] = pos[:, 1]
        g[:, 2] = (tz - 0.5) * tile + pos[:, 2]
        verts.append(g)
        uvs.append(v["uv0"])
        rgbas.append(v["rgba"])
        dirs.append(v["dir"])
        for ids, flags, first, count in recs:
            tri = idx[first:first + count - count % 3].reshape(-1, 3) + base
            faces.append(tri)
            ftex.append(np.full(len(tri), ids[0] if ids[0] != 0xFFFF else -1, np.int32))
            records.append({
                "tile": (tx, tz),
                "textures": [textures.get(i) if i != 0xFFFF else None for i in ids],
                "flags": flags,
                "faces": slice(nface, nface + len(tri)),
            })
            nface += len(tri)
        base += nv

    V = np.concatenate(verts) if verts else np.zeros((0, 3), np.float32)
    F = np.concatenate(faces).astype(np.int32) if faces else np.zeros((0, 3), np.int32)
    T = np.concatenate(ftex) if ftex else np.zeros(0, np.int32)
    cats = {i: texture_category(s) for i, s in textures.items()}
    cat = np.array([cats.get(int(t), "ground") for t in T], dtype=object)
    is_town = np.isin(cat, ["town", "industrial"]) if len(cat) else np.zeros(0, bool)
    info = {
        "tile_size": float(tile), "tiles": (int(nx), int(nz)), "textures": textures,
        "face_texture": T, "face_category": cat, "face_is_town": is_town,
        "uv": np.concatenate(uvs) if uvs else np.zeros((0, 2), np.float32),
        "rgba": np.concatenate(rgbas) if rgbas else np.zeros((0, 4), np.uint8),
        "dir": np.concatenate(dirs) if dirs else np.zeros((0, 2), np.float32),
        "records": records,
        "frame": "game metres: x north from the south edge, y up (0 = on the ground), z east from the west edge",
    }
    if town_only:
        F = F[is_town]
        used = np.unique(F)
        remap = np.full(len(V), -1, np.int32)
        remap[used] = np.arange(len(used), dtype=np.int32)
        for k in ("uv", "rgba", "dir"):
            info[k] = info[k][used]
        info["face_texture"] = T[is_town]
        info["face_category"] = cat[is_town]
        info["face_is_town"] = is_town[is_town]
        info["records"] = None  # face slices no longer apply
        V, F = V[used], remap[F]
    return V, F, info
