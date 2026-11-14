---
title: "Finding maps: list"
nav_order: 2
---

# Finding maps: `list`

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

1. Install once, from a clone of this repository: `pip install -e .`
   (Python 3.10 or later; needs numpy; `pip install -e .[fast]` adds numba).
2. Run `heat3d-il2-level list`.
3. Each map prints one line, tab-separated: its name (the name `extract`
   takes), the game (`Great Battles` or `Korea`), the heightmap it reads, and
   where it lies on the earth - its latitude/longitude box from the map's
   corners, or the landmark fit that places it, or "not placed on the earth".
   The last line (on stderr) counts the maps and names the installs.

![list on a synthetic install](assets/img/list.svg)

The picture is a run on an install built from the tests' writers
(`tests/synth.py`), not on the game.

## Where the installs are found

Through Steam; otherwise `--game <folder>` (repeatable, one per install) or the
`HEAT3D_IL2_GAME` environment variable. An install is a folder whose `data`
holds `Maps*.gtp` archives.

| Option | Does |
|---|---|
| `--game FOLDER` | an IL-2 folder; repeat it for several installs |

Exit status: 0 done, 2 no install found.
