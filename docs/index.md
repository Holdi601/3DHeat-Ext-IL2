---
title: Home
nav_order: 1
---

# 3DHeat IL-2

**What is it?** A small program that turns the maps of **IL-2 Sturmovik:
Great Battles**, read from **your own install**, into 3D models - levels -
you can fly over in the [3DHeat](https://github.com/Holdi601/3DHeat) viewer
([documentation](https://holdi601.github.io/3DHeat/)): the hills, rivers,
lakes, sea and towns, placed where they lie on the earth. A second IL-2 game
whose archives hide their file table is read as far as they allow
([details](archives-without-table.md)).

**Why would I use it?** To see your IL-2 flights over the game's own map.

**Example:** `heat3d-il2-level extract <map> -o levels` ->
`levels/<map>/<map>.glb` (the level) + `<map>.json` (where it lies on the
earth). A heightmap is a grid of heights, like a relief map; a Tacview
recording is a file of a flight that Tacview writes.

What it is useful for:

- **Flights on the game's own map.** An IL-2 Tacview recording, converted by
  the 3DHeat Watcher with the same origin, lands on the level with no
  placement step.
- **Every map at once.** `extract --all` writes every map found; seasons that
  share a heightmap are written once.
- **Where on the earth.** Each level's `.json` carries its corners and
  latitude/longitude box, and how they were found.

![From an IL-2 install to a 3DHeat level](assets/img/flow.svg)

## The standalone program (no Python needed)

Each [release](https://github.com/Holdi601/3DHeat-Ext-IL2/releases/latest)
has a ready-to-run program for Windows (`heat3d-il2-<version>-windows-x64.zip`)
and Linux (`heat3d-il2-<version>-linux-x64.tar.gz`, for IL-2 installed by
Steam under Proton, Steam Deck included), with a `SHA256SUMS` file to check
the download. Unpack it anywhere and start `heat3d-il2`.

Started without arguments it opens a window that:

- finds IL-2 Sturmovik: Great Battles and IL-2 Series: Korea in any Steam
  library (Windows, Linux native and flatpak, Steam Deck) and the launcher's
  usual folders, or lets you choose each one's folder;
- says what is missing: a game, free disk space;
- lists the maps (each season of a map is one) as new, changed by a game
  update, extracted by an older version, or up to date, and extracts the ones
  you pick, one at a time, into the 3DHeat levels folder (`HEAT3D_LEVELS`, by
  default `%LOCALAPPDATA%\3DHeat\levels` on Windows and
  `~/.local/share/3dheat/levels` on Linux), under `il2/` (Korea under
  `il2-korea/`), where the viewer finds them: `<map>/<map>.glb` and its
  `.json`;
- checks for updates and asks before installing one, unless you tick
  *Update automatically*.

A map an update adds or changes is found the next time: each extracted map is
recorded in `<levels>/il2/.heat3d-extract.json` with the version that
extracted it and the size and SHA-256 of the archives its files are in.

The same program runs every command below: `heat3d-il2 heat3d-il2-level list`,
`heat3d-il2 heat3d-il2-level extract <map> -o <folder>`. For scripts:
`heat3d-il2 status --json` reports the maps' state,
`heat3d-il2 extract --new` extracts only the new ones and
`heat3d-il2 --check --json` says what is found and missing. The 3DHeat app's
Extractors panel installs, updates and starts it for you.
`python -m heat3d_ext_il2.standalone_spec` opens the same window from the
source.

## Quick start (Python)

You need Windows, Python 3.10 or later ("Add python.exe to PATH" ticked in its
installer), IL-2 Sturmovik: Great Battles installed through Steam (found by
itself) and about 30 MB of disk space a map; no Git. New to the command line?
Read [Before you start](before-you-start.md) first.

```bash
python -m pip install https://github.com/Holdi601/3DHeat-Ext-IL2/archive/refs/tags/v0.2.0.zip
python -m pip install numba                               # optional: decoding 20 to 50 times faster
heat3d-il2-level list                                     # every map found, with its latitude/longitude box
heat3d-il2-level extract landscape_stalin_s -o levels     # one map (names as `list` prints them, wildcards allowed)
heat3d-il2-level extract --all -o levels                  # every map
```

You should see a line per map from `list`, and
`ok <glb> <n> triangles (enu frame)` per map from `extract`. Each map goes into
its own folder: `levels\landscape_stalin_s\landscape_stalin_s.glb` (the level,
about 30 MB, in seconds with numba) and `landscape_stalin_s.json` beside it
(where it lies on the earth). An install outside Steam needs
`--game "<IL-2 folder>"`.

Then open the `.glb` in the [3DHeat viewer](https://github.com/Holdi601/3DHeat#quick-start):
download it (**Code -> Download ZIP**, unpack), double-click `start.bat` (it
offers to install Node.js when it is missing and opens `http://127.0.0.1:5273`),
then **Background / level -> 3D model...** and pick the file
([Levels](https://holdi601.github.io/3DHeat/levels.html)). The level stays on
your machine.

When a new release is out, the tool says so when it starts, shows its notes
and asks: update now, later, or skip this version. It updates without asking
only when you chose that: `--auto-update` (this run), the standalone window's
*Update automatically*, or `HEAT3D_AUTO_UPDATE=1`.

Each game reader is its own small project with its own licence file, releases
and issue tracker, so it can be installed, updated, maintained - or withdrawn
on a rights holder's request - on its own, without affecting the viewer or the
other tools.

## Pages

| Page | What it covers |
|---|---|
| [Before you start](before-you-start.md) | Python, a terminal, a first run |
| [Finding maps: list](list.md) | where the installs are found, what `list` prints |
| [Building levels: extract](extract.md) | every option, step by step, examples |
| [The level files and frames](output.md) | the `.glb` parts, the `.json`, the `enu` and `game` frames |
| [How the files are read](reading.md) | archives, the heightmap codec, water, towns, landmark fits |
| [Archives without a file table](archives-without-table.md) | the second game, read as far as its archives allow |
| [Speed, tests, terms](terms.md) | numba, the tests, what is read and what is not shipped, the licence |
| [Command reference](cli-reference.md) | every option, generated from the code |
| [Maintaining these docs](maintaining.md) | the release checklist |

## Related

- The 3DHeat viewer: [github.com/Holdi601/3DHeat](https://github.com/Holdi601/3DHeat),
  documentation at [holdi601.github.io/3DHeat](https://holdi601.github.io/3DHeat/).
- Telemetry for these levels: the [3DHeat Watcher](https://holdi601.github.io/3DHeat-Watcher/)
  converts IL-2 Tacview recordings; the viewer's file formats, including its
  one-file-a-match container, are described in
  [One file a match (.3dheat)](https://holdi601.github.io/3DHeat/container.html).

## The 3DHeat tools

| Tool | What it does | Code | Docs |
|---|---|---|---|
| 3DHeat viewer | shows the data: heatmaps, race analysis, match review | [3DHeat](https://github.com/Holdi601/3DHeat) | [docs](https://holdi601.github.io/3DHeat/) |
| GameFiles | levels and courses from a game's own files | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [docs](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | lap telemetry, and levels rebuilt from gameplay video | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [docs](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | an Unreal Editor plugin: a level as one `.glb` | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [docs](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | Counter-Strike 2 demos and maps | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [docs](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | records what games publish while you play | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [docs](https://holdi601.github.io/3DHeat-Watcher/) |
| Ext-WarThunder | War Thunder replays | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [docs](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| Ext-WoT | World of Tanks replays | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [docs](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| Ext-WoWs | World of Warships replays | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [docs](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Ext-Squad | Squad server demos | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [docs](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| Ext-DCS | DCS World maps as 3D levels | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [docs](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| Ext-IL2 | IL-2 Sturmovik maps as 3D levels | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [docs](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Ext-Dota | the Dota 2 map from your own install as a 3D level | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [docs](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Ext-DotaReplay | Dota 2 replays | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [docs](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Ext-Riot | League of Legends and VALORANT replays (what they carry unencrypted) | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [docs](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Ext-Forza | Forza courses, races and cars from your own install | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [docs](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Ext-Battlefield | Battlefield levels (Frostbite) as 3D levels | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [docs](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| Ext-BeamNG | BeamNG.drive courses | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [docs](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| Ext-ACRally | Assetto Corsa Rally stages as courses | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [docs](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Ext-Reforger | Arma Reforger worlds (Enfusion) as 3D levels | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [docs](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| Ext-R6 | Rainbow Six Siege match replays | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [docs](https://holdi601.github.io/3DHeat-Ext-R6/) |
