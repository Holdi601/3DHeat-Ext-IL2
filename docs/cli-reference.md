---
title: Command reference
nav_order: 90
---

# Command reference

Generated from the code by `tools/gen_docs_reference.py`: do not edit by hand.
The other pages explain each command step by step.

## `heat3d-il2-level`

```text
usage: heat3d-il2-level [-h] [--version] {list,extract} ...

IL-2 Sturmovik maps into 3DHeat .glb levels

positional arguments:
  {list,extract}
    list          list the maps found
    extract       extract maps

options:
  -h, --help      show this help message and exit
  --version       show program's version number and exit
```

## `list`

```text
usage: heat3d-il2-level list [-h] [--game GAME]

options:
  -h, --help   show this help message and exit
  --game GAME  an IL-2 folder (repeatable; default: found through Steam)
```

## `extract`

```text
usage: heat3d-il2-level extract [-h] [--all] -o OUT [--game GAME]
                                [--max-grid MAX_GRID] [--frame {enu,game}]
                                [--origin LAT LON] [--no-water] [--no-towns]
                                [--skip-existing]
                                [maps ...]

positional arguments:
  maps                 map names as `list` prints them (wildcards allowed)

options:
  -h, --help           show this help message and exit
  --all                every map; seasons that share a heightmap and water map are
                       written once
  -o, --out OUT        output folder; each map goes in <out>/<map>/
  --game GAME          an IL-2 folder (repeatable)
  --max-grid MAX_GRID  heightmap samples a side (default 1024)
  --frame {enu,game}   enu: metres east/altitude/north of --origin, like the watcher's
                       Tacview tables (default); game: the game's own metres (x north,
                       y up, z east)
  --origin LAT LON     origin of the enu frame (a recording's geo); default: the map's
                       centre
  --no-water           leave the water out
  --no-towns           leave the town footprints out
  --skip-existing      leave maps whose .glb exists
```

## Output

### `<map>.glb` parts

Parts of the test level: `ground:<map>`, `water:<map>` (a map with town footprints adds `ground:<map> towns`).

### `<map>.json`

Top-level keys: `format`, `tool`, `game`, `map`, `files`, `heightmap`, `notRead`, `playArea`, `corners`, `extent`, `georeference`, `frame`, `geo`, `parts`, `seconds`.
