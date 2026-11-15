# Changelog

## 0.2.0

- Maps whose `height.hini` carries another map's corners placed on the earth by a landmark fit.
- The game's water mask (`water.wtr`) and town footprints; `--no-water`, `--no-towns`.
- `list` counts one map in the singular.

## 0.1.0

- First version: IL-2 Sturmovik: Great Battles maps as 3DHeat levels; `list`, `extract`.

## Docs

Where each feature is documented
([holdi601.github.io/3DHeat-Ext-IL2](https://holdi601.github.io/3DHeat-Ext-IL2/)):

| Feature | Page |
|---|---|
| Installing, a first run | [Before you start](docs/before-you-start.md) |
| Finding installs and maps (`list`, `--game`, `HEAT3D_IL2_GAME`) | [Finding maps: list](docs/list.md) |
| Building levels (`extract` and its options, `HEAT3D_DEBUG`) | [Building levels: extract](docs/extract.md) |
| The `.glb` parts, the `.json`, the `enu` and `game` frames | [The level files and frames](docs/output.md) |
| Archives, the heightmap codec, water, towns, landmark fits | [How the files are read](docs/reading.md) |
| The second game, whose archives have no file table | [Archives without a file table](docs/archives-without-table.md) |
| Speed (numba), tests, the game's terms, licence | [Speed, tests, terms](docs/terms.md) |
| Every option and output key, generated | [Command reference](docs/cli-reference.md) |
| Release checklist for the docs | [Maintaining these docs](docs/maintaining.md) |
