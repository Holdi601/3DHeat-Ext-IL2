# 3DHeat IL-2 map converter

The maps of IL-2 Sturmovik: Great Battles as 3D levels for the 3DHeat viewer:
the terrain, the rivers, lakes and sea, placed on the earth by the map's own
corner coordinates, read from **your own install**. IL-2 Series: Korea is read as far
as its archives allow (see [Korea](#il-2-series-korea)).

```bash
pip install -e .                                   # installs the heat3d-il2-level command
pip install -e .[fast]                             # with numba: decoding 20 to 50 times faster
heat3d-il2-level list                              # every map found, with its latitude/longitude box
heat3d-il2-level extract <map> -o levels           # one map (names as `list` prints them, wildcards allowed)
heat3d-il2-level extract --all -o levels           # every map; seasons sharing a heightmap are written once
heat3d-il2-level extract <map> --origin 56.0 37.0 -o levels   # in the flat map of a recording with that geo
python -m heat3d_ext_il2 ...                       # the same, without installing
```

The installs are found through Steam; `--game <folder>` (repeatable) or
`HEAT3D_IL2_GAME` say where they are otherwise. The command prints
`ok <glb> <triangles>` or `failed <map>: <why>` per map and exits 1 when any
failed, 2 when no install or no map was found.

This converter is kept apart from the 3DHeat tools on purpose: it reads the
game's archives, whose terms (below) were not found. If it ever has to go,
nothing else goes with it.

## What comes out

`<out>/<map>/<map>.glb` and `<map>.json` beside it. The glb is written to
`<map>.glb.part` and renamed when complete.

| Part | What it is |
|---|---|
| `ground:<map>` | the terrain heightmap as a grid, at most `--max-grid` samples a side (default 1024: about 2 million triangles) |
| `water:<map>` | rivers, lakes and sea: flat quads at the water's height, one per grid cell at least half of whose heightmap samples are under water |

The JSON holds the map's **corners and latitude/longitude box** (`corners`,
`extent`), how they were found (`georeference`), the height settings
(`heightMul`, `SeaLevel`), the play area in the game's metres (`playArea`), the
frame and its origin (`frame`, `geo`), triangle counts and any `notes`.

**Coordinates.** Two frames, `--frame`:

- `enu` (default): metres east, altitude above sea level, north of an origin on
  the WGS-84 tangent plane: the flat map the 3DHeat Watcher puts an IL-2 Tacview
  recording in (x east, y altitude, z north, drawn with z mirrored). The glb
  stores (east, altitude, -north). Convert with `--origin <lat> <lon>` set to a
  recording's `geo` (its session's reference point) and the recording lands on
  the level with no placement step; without it the map's centre is the origin,
  and the JSON's `geo` says which.
- `game`: the game's own metres as mission files have them: x north from the
  south edge, y the game's height, z east from the west edge (right-handed as it
  is, so glb = (x, y, z)). Maps that cannot be placed on the earth are written in
  this frame whatever was asked, with a note.

## What is read, and how well

| Part | Status |
|---|---|
| Archives (`data/*.gtp`, Great Battles) | the file table (`S16R`, `STRMFAT?`, `DIR!`/`FILE` records) and the entries (`STRMFILE` header, data stored as is); every `Maps*.gtp` of this machine's install |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, the play limits and `MapNW/NE/SE/SW`; all 30 of this install |
| Heightmaps (`height.dat`) | the codec below; every sector of the five maps decoded in full while working it out uses its bitstream exactly (at most the byte padding left over), the rest checked by header. Checked bit-exactly against the two uncompressed `distlod.raw` files the game ships beside their `distlod.dat`, and on one map against its own distant-LOD heightmap (correlation 0.999) |
| Heights | metres = raw x heightMul / 256 - SeaLevel x heightMul. One map's sea decodes to exactly the 500 m its hini comments; another's border to its `bounds_level` |
| Placement | bilinear between the hini's four corners, row 0 north, column 0 west. Checked on one map against eight known towns, coasts and seas (town heights within about 10 m of the real ones, the seas below sea level). The corners are a quadrilateral, not the game's own projection, so expect some hundreds of metres of error in the middle of a 400 km map. One map family's hini carries the corners of another map (they span 50 km on a 345 km map); these are detected and the map is written in the game frame |
| Water (`height_w.dat`, same codec) | a water surface; where it is above the ground there is water. It over-reports on some maps (marshy, flat ground shows as shallow water), because the game's own water mask (`water.wtr`) is not read |
| Buildings, towns, airfields, bridges (`towns.mesh`, the Locations archives) | **not read** |
| Forests (`forest_map.wtr`), the ground's textures, roads | not read |

### The heightmap codec

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

## IL-2 Series: Korea

Korea's archives have no readable file table (the names are hashed in a block at
the end of each archive) and its settings files are not stored readable, so:

- its heightmap and water map are found by their header (`height.dat` layout,
  sectors of 128 samples; 19,968 samples a side at 25 m);
- it is placed on the earth by fitting the airfields its missions place
  (`data/Missions/**/*.Mission`, read on your machine) to the real airfields'
  published coordinates (`korea.py`): with the four of the shipped demo missions
  the residuals are 20 to 330 m. The JSON lists each landmark and its residual;
- heightMul and SeaLevel are estimated: ships in the missions sit on the sea, so
  their height over the water map's commonest (sea) value gives the scale. Heights
  of known places come out plausible (the Yellow Sea below sea level, Pyongyang
  and Sinuiju at a few metres), not checked further. The JSON marks them estimated.

## Speed

Decoding is pure Python unless numba is installed (`pip install -e .[fast]`):
a 5632-sample map takes about 15 s without it and about a second with it; the
Korea map's 400 million samples about 7 s with it (the first run also compiles).
Memory stays at one row of sectors plus the output grid.

## The terms

The licence agreement of IL-2 Sturmovik: Great Battles and IL-2 Series (1C Game
Studios / 777 Studios) was **not found**: not in the install (whose
`data/Licenses.txt` holds only third-party licences), not on the publisher's site,
and the Steam EULA page did not load. Check it yourself before relying on this.
This tool only reads the archives and never changes them. The levels it writes stay
on your machine: **never publish them**. Nothing here ships any game data, and the
tests build every file they read.

## Tests

```bash
python -m pytest -q
```

`tests/synth.py` builds archives, heightmaps (an encoder for the codec above),
`height.hini` files and Korea-style archives in code.

## Licence

MIT - see [`LICENSE`](LICENSE). Uses numpy (BSD-3-Clause) and, optionally,
numba (BSD-2-Clause). `heat3d_update` is the 3DHeat tools' shared updater.
