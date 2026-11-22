# Changelog

## 0.5.0

- What's new: the tanks you drive in Tank Crew are in the model pack at their true size, with a turret that turns
  and a gun that raises, and with their armour plates (thickness in mm) and modules (ammunition, fuel, engine,
  transmission, radiator...) for the 3DHeat viewer's hit analysis.
- `models`: a drivable tank or assault gun is put together from its hull and crew stations as the game does it
  (before, only the hull was read, from its inside model: no turret, and tracks and aerials that made several
  of them metres too long or tall). The gun is posed level, hatches shut, machine guns forward.
- The computer-driven tanks' turret and gun are joints in the index too (`joints`), as in the other games' packs;
  radio aerials are their own part (`aerial`) and no longer count in a vehicle's size; a wreck form some models
  keep is left out.
- `catalog`: the drivable tanks are tanks with the game's own name for them (they were marked as scenery).

## 0.4.0

- Its own icon: the 3DHeat cube with a text badge for its game (letters in 3DHeat's colours), as the
  program, window, taskbar and docs icon.
- A new window: the 3DHeat look in dark and light (follows the system, switchable), the logo and
  icon, sharp at any display scaling. Four steps: find the game (each requirement with its fix),
  choose (maps ticked when there is something to do, filters, search; jobs with their fields
  inline), work (progress, time left, cancel), done (open in 3DHeat, open the output folder, and
  for a failure what went wrong and what to do, copy details, report a problem).
- No console window on Windows: the program is a window program. From a terminal it still prints
  as before; `heat3d-il2-cli.cmd` beside it waits for it in a terminal and passes its exit code.
- The update offer in the same look: Update now / Later / Skip this version, and "Update
  automatically" from the dialog.
- CI draws every page and dialog of the window (on Linux under a virtual display) and checks the
  Windows build is a window program.

## 0.3.1

- `models`: every aircraft, vehicle, gun and ship of your install as a local 3DHeat model pack, from a new reader for the game's `.mgm` models: three levels of detail posed as the game shows the unit at rest, propellers (`rotor.N`, hub, axis, diameter), retractable landing gear (`gear`, posed down), a vehicle's turret and gun, and the hit regions (`dm`, one per piece the game can shoot away).
- `catalog`: the units with the real vehicle each one is and the names other games give it.
- `--check [--json]`: what is found and what is missing.

## 0.3.0

- A standalone program for Windows and Linux (no Python needed), built by CI with a `SHA256SUMS` file. Without
  arguments it opens a window: what is found and what is missing (Great Battles and Korea installs, disk space),
  the levels folder, the maps as new / changed by a game update / extracted by an older version / up to date,
  and extraction of the picked ones one at a time into `<levels>/il2/` (Korea: `<levels>/il2-korea/`), and
  updates.
- Each extracted map is recorded in `<levels>/il2/.heat3d-extract.json` (extractor version, size and SHA-256 of
  the archives its files are in), so maps an update adds or changes are found and only those extracted:
  `status --json`, `extract [--game il2|il2-korea] --new` / `--changed` / `--outdated` / `<map>...`,
  `--progress-json`.
- Updates ask first (update now / later / skip this version) unless automatic updates were chosen
  (`--auto-update`, the window's checkbox, or `HEAT3D_AUTO_UPDATE=1`).
- Installs are found in every Steam library on Windows and Linux (native, flatpak, Steam Deck; IL-2 under
  Proton) and in the launcher's usual folders on Windows.

## 0.2.0

- Maps whose `height.hini` carries another map's corners placed on the earth by a landmark fit.
- The game's water mask (`water.wtr`) and town footprints; `--no-water`, `--no-towns`.
- `list` counts one map in the singular.
- Installs with one pip line from the release zip, no Git needed; a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

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
| Unit models and the unit list (`models`, `catalog`, `--check`) | [Unit models](docs/models.md) |
| The `.glb` parts, the `.json`, the `enu` and `game` frames | [The level files and frames](docs/output.md) |
| Archives, the heightmap codec, water, towns, landmark fits | [How the files are read](docs/reading.md) |
| The second game, whose archives have no file table | [Archives without a file table](docs/archives-without-table.md) |
| Speed (numba), tests, the game's terms, licence | [Speed, tests, terms](docs/terms.md) |
| Every option and output key, generated | [Command reference](docs/cli-reference.md) |
| Release checklist for the docs | [Maintaining these docs](docs/maintaining.md) |
