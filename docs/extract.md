---
title: "Building levels: extract"
nav_order: 3
---

# Building levels: `extract`

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Step by step

New to the command line? Read [Before you start](before-you-start.md) first.

1. Find the map's name with [`list`](list.md).
2. Run `heat3d-il2-level extract <map> -o levels`. Names may use wildcards,
   in quotes (`"<family>_*"`); `--all` takes every map.
3. To put a recording on the level with no placement step, give its origin:
   `--origin <lat> <lon>` set to the recording's `geo` (its session's
   reference point). Without it the map's centre is the origin, and the
   `.json`'s `geo` says which.
4. The command prints a line per map as it decodes it, then
   `ok <glb> <triangles> (<frame> frame)` or `failed <map>: <why>`.
5. Load `<folder>/<map>/<map>.glb` in the viewer's Background / level panel.

![extract on a synthetic install](assets/img/extract.svg)

In the game's own metres, without the water:

![extract --frame game --no-water](assets/img/extract-game.svg)

A second run over maps already written:

![extract --all --skip-existing](assets/img/extract-skip.svg)

## Options

| Option | Default | Does |
|---|---|---|
| `maps` | - | map names as `list` prints them; wildcards allowed |
| `--all` | off | every map; seasons that share a heightmap and water map are written once |
| `-o`, `--out` | required | the output folder; each map goes in `<out>/<map>/` |
| `--game FOLDER` | found | an IL-2 folder (repeatable) |
| `--max-grid N` | `1024` | heightmap samples a side at most (1024: about 2 million triangles); the map is sampled every *k* samples to fit |
| `--frame` `enu` or `game` | `enu` | `enu`: metres east, altitude, north of `--origin`, like the Watcher's Tacview tables; `game`: the game's own metres (x north, y up, z east). A map that cannot be placed on the earth is written in `game` whatever is asked |
| `--origin LAT LON` | the map's centre | the origin of the `enu` frame (a recording's `geo`) |
| `--no-water` | off | leave the water out |
| `--no-towns` | off | leave the town footprints out |
| `--skip-existing` | off | leave maps whose `.glb` already exists |

Every option, as the program prints it: [Command reference](cli-reference.md).

Set `HEAT3D_DEBUG` to print the full traceback of a failed map. The `.glb` is
written to `<map>.glb.part` and renamed when complete.

Exit status: 0 every map written, 1 any failed (the others are still
written), 2 no install or no map matched.

## Examples

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

What is in the files: [The level files and frames](output.md).
