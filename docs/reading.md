---
title: How the files are read
nav_order: 5
---

# How the files are read

| Part | Status |
|---|---|
| Archives (`data/*.gtp`, Great Battles) | the file table (`S16R`, `STRMFAT?`, `DIR!`/`FILE` records) and the entries (`STRMFILE` header, data stored as is); every `Maps*.gtp` of the test install |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, the play limits and `MapNW/NE/SE/SW`; every one of the test install |
| Heightmaps (`height.dat`) | the codec below; every sector of the maps decoded in full while working it out uses its bitstream exactly (at most the byte padding left over), the rest checked by header. Checked bit-exactly against the uncompressed `distlod.raw` files the game ships beside their `distlod.dat`, and against a map's own distant-LOD heightmap (correlation 0.999) |
| Heights | metres = raw x heightMul / 256 - SeaLevel x heightMul. A map's sea decodes to exactly the height its hini comments give; another's border to its `bounds_level` |
| Placement | bilinear between the hini's four corners, row 0 north, column 0 west. Checked on a map against known towns, coasts and seas (town heights within about 10 m of the real ones, the seas below sea level). The corners are a quadrilateral, not the game's own projection, so expect some hundreds of metres of error in the middle of a large map. One map family's hini carries the corners of another map (they span a fraction of its real size); this is detected, and that family is placed instead by a landmark fit: towns and airfields of the game's own location databases (`*.ldfbin`) against their real positions, rms of a couple of kilometres (towns against the airfields named after them, and coordinates of the real places to about a kilometre); the JSON lists every landmark and its residual |
| Water mask (`water.wtr`: four pyramid levels of tiles, each tile a table of 400 m blocks, each block land, full or partly water with its shape in a bit stream) | the container is read on every map (no byte left over on the files decoded in full); the shape inside a partly-water block is **not decoded**. Full blocks are water; in partly-water blocks a sample is water where the water map (`height_w.dat`, same codec as the heightmap) is above the ground, or, next to a lake, where the ground is no higher than the lake; land blocks are dry. That removes the marsh the water map alone reports as water. Rivers narrower than the output grid come out broken into pieces |
| Town footprints (the decal meshes `textures.tini` lists: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: 25.6 km tiles of flat textured triangles) | read on every map; the faces whose texture is a town, village or industrial ground are kept. Checked against the real towns on a few maps (a town on both banks of a river, a confluence). They are footprints: the game places the buildings at run time, and the files hold no buildings |
| Airfields, bridges, buildings | **not read**: airfields are mission objects, buildings come from the game's own placement |
| Forests (`forest_map.wtr`) | its blocks read the same way, but nearly every block is "partly forest", so without the bit stream there is no usable forest mask; not drawn |
| The ground's textures | not read |

## The heightmap codec

Worked out from the data files alone; no game code was read or disassembled.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            from the start of the file, row-major, top row first
sector: u16 count (bytes that follow), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        then a bitstream read MSB first:
  PRE   2 * (log2(sectorSize) - 5) bits, always 0 so far
  LIT   the first sample: sign (1), n (LW bits), magnitude (n + 1 bits)
  then until the sector is full:
    0 LIT       next = previous + LIT
    1 RUN LIT   the previous sample repeats RUN times (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                then (unless the sector is full) next = previous + LIT
  values are 16-bit: read them modulo 65536
```

Partial sectors at the right and bottom edges are padded and cropped. The same
codec holds the water map and the distant-LOD heightmap.

## Landmark fits

Where a map's corners cannot be used, `landmarks.py` fits an affine map from the
game's metres to the earth by least squares: game positions from the user's own
files (mission `Airfield` blocks, the career location databases), real positions
from tables of the places' published coordinates in the code. The JSON's
`georeference` carries the matrix, the origin, every landmark with its residual
and the rms.
