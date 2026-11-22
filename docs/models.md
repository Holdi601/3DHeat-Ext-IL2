---
title: "Unit models: models and catalog"
nav_order: 4
---

# Unit models: `models` and `catalog`

```text
heat3d-il2-level models  [--levels FOLDER | -o PACK] [--units a,b] [--domains air,ground,sea] [--limit N] [--force] [--game FOLDER ...]
heat3d-il2-level catalog [--levels FOLDER | -o FILE] [--list] [--game FOLDER ...]
heat3d-il2-level --check [--json]
```

New to the command line? Read [Before you start](before-you-start.md) first.

**What it does:** `models` turns the aircraft, vehicles, guns and ships of your
own IL-2 Sturmovik: Great Battles install into a *model pack*: one `.glb` per
unit and an index, `model-pack.json`. The 3DHeat viewer then draws each unit of
a recording as its own model, at its true size, instead of a generic figure:
propellers turn, the landing gear folds away in flight, a tank's turret and gun
follow the data. `catalog` writes the list of those units with the real
vehicle each one is (`Bf 109 G-6`, `Spitfire Mk IXe`, `Il-2 mod.1943`) and the
other names it goes by, so units of other games find these models and the
other way round.

**One command:** set the 3DHeat levels folder once, then

```bash
heat3d-il2-level models --levels "D:\3DHeat\levels"
heat3d-il2-level catalog --levels "D:\3DHeat\levels"
```

With the standalone program (no Python needed) the same commands are
`heat3d-il2 models ...` and `heat3d-il2 catalog ...`.

That writes `<levels>\model-packs\il2\` and `<levels>\il2\catalog.json`. With
`HEAT3D_LEVELS` set, `--levels` can be left out. A first run takes a few
minutes; a later run redoes only units whose files changed (`--force` redoes
all).

`--check` says what was found and what is missing (the install, the archives,
free disk space) and stops; `--check --json` says the same as one JSON object.

## What a unit's model holds

- three levels of detail, made from the game's own: the full model, its
  coarser form and its far form, each posed as the game shows the unit at rest
  (landing gear down, control surfaces centred) and simplified to the viewer's
  budget (about 16,000, 3,000 and 800 triangles for an aircraft);
- parts the viewer moves, from the model's own node names and animations:
  `rotor.N` for each propeller (its hub, axis and diameter), `gear` for
  retractable landing gear (fixed gear stays on the airframe), `turret` and
  `gun` for a vehicle's turret and gun (as joints: the turret turns, the gun
  raises on it);
- `dm`: the hit regions, one per piece the game can shoot away (wing panels,
  control surfaces, engine cowling, fuselage sections), named by the piece;
- `aerial`: a vehicle's radio aerials, drawn but left out of its size.

### Tanks you drive (Tank Crew)

A tank or assault gun the player drives is put together the way the game puts
it together: the hull, and each crew station with a weapon (the turret or the
assault gun's mount, the commander's cupola, the hull machine gun) at its place
on the hull. The hull comes from the game's own outside levels of detail; the
gun is posed level and straight ahead, the hatches shut and the machine guns
pointing forward, so the model has the vehicle's true size. Its index entry
adds:

- `turret` and `gun` as joints (`turret` turns about its ring, `gun` raises on
  the turret; an assault gun's limited traverse is its `turret`), with the
  traverse and elevation limits the game gives (`yawLimits`, `pitchLimits`);
- `dm`: every armour plate of the hull and the stations with its thickness
  (`mm`, the millimetres of armour steel the game counts for it) and the part
  it moves with, and the modules: `ammo`, `fuel`, `engine`, `transmission`,
  `radiator`, `electrics`, `optics`, `gun`, `drive` (turret traverse), and the
  outside parts (`tracks`, `wheel`, `structure`: covers, side screens, spare
  parts). The viewer's vehicle hit analysis shows these plates, the armour
  along a shot's way and the angle it met the plate;
- `armoured` (how many armour plates), `armourMm` (thinnest and thickest),
  `drivable: true`.

In the catalogue these tanks carry the game's own name for them (`Pz.Kpfw.IV
Ausf.G`, beside the computer-driven `PzKpfw IV Ausf.G`) and `drivable: true`.

Muzzle flashes, smoke, lights, markings, propeller blur, damaged states and the
cockpit are left out. A model that does not read as expected is skipped and
named (`skipped <unit>: <why>`); the run goes on.

IL-2 Series (Korea) keeps the file names in its archives hashed; its models are
not read, and `--check` says so.

| Option | Does |
|---|---|
| `--levels FOLDER` | the 3DHeat levels folder (default: `HEAT3D_LEVELS`) |
| `-o` | `models`: the pack folder; `catalog`: the catalogue file |
| `--units a,b` | only these units, by their folder names (`catalog --list` shows them) |
| `--domains` | `air`, `ground`, `sea`, comma-separated |
| `--limit N` | at most N units |
| `--force` | rebuild units that are up to date |
| `--list` | `catalog`: print the units instead of writing the file |
| `--game FOLDER` | an IL-2 folder, if it is not found through Steam |

Exit status: 0 done, 1 every unit failed, 2 no install or nothing to do.

The pack and the catalogue stay on your machine; nothing is uploaded or shared.
