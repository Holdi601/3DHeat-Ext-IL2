---
title: "Levelen bauen: extract"
nav_order: 3
lang: "lb"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Levelen bauen: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Schrëtt fir Schrëtt {#step-by-step}

Nei op der Kommandozeil? Liest fir d'éischt [Ier Dir ufänkt](before-you-start.md).

1. Fannt den Numm vun der Map mat [`list`](list.md).
2. `heat3d-il2-level extract <map> -o levels` ausféieren. Nimm kënne Wildcards benotzen,
   an Ureechnungszeechen (`"<family>_*"`); `--all` hëlt all Map.
3. Fir eng Opnam ouni Placement-Schrëtt op d'Level ze setzen, gitt hiren Urspronk un:
   `--origin <lat> <lon>` op dat `geo` vun der Opnam gesat (de
   Referenzpunkt vun hirer Sessioun). Ouni et ass d'Mëtt vun der Map den Urspronk, an dem
   `.json` säi `geo` seet, wéi eng.
4. De Kommando gëtt eng Zeil pro Map aus, wéi en se dekodéiert, dann
   `ok <glb> <triangles> (<frame> frame)` oder `failed <map>: <why>`.
5. Lued `<folder>/<map>/<map>.glb` am Panel „Hannergrond / Level“ vum Viewer.

![extract op enger syntheteschen Installatioun](../assets/img/extract.svg)

An de Meter vum Spill selwer, ouni d'Waasser:

![extract --frame game --no-water](../assets/img/extract-game.svg)

E zweeten Duerchlaf iwwer Mappen, déi schonn geschriwwe sinn:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Optiounen {#options}

| Optioun | Standard | Mécht |
|---|---|---|
| `maps` | - | Mappennimm, wéi `list` se ausgëtt; Wildcards erlaabt |
| `--all` | aus | all Map; Joreszäiten, déi eng Heightmap a Waasserkaart deelen, ginn eemol geschriwwen |
| `-o`, `--out` | erfuerderlech | den Ausgabdossier; all Map geet an `<out>/<map>/` |
| `--game FOLDER` | fonnt | en IL-2-Dossier (widderhuelbar) |
| `--max-grid N` | `1024` | héchstens sou vill Heightmap-Echantillonen pro Säit (1024: ongeféier 2 Millioune Dräiecker); d'Map gëtt all *k* Echantillone gesampelt, fir ze passen |
| `--frame` `enu` oder `game` | `enu` | `enu`: Meter Ouschten, Héicht, Norden vun `--origin`, wéi dem Watcher seng Tacview-Tabellen; `game`: dem Spill seng eegen Meter (x Norden, y no uewen, z Ouschten). Eng Map, déi net op der Äerd placéiert ka ginn, gëtt a `game` geschriwwen, egal wat gefrot gëtt |
| `--origin LAT LON` | d'Mëtt vun der Map | den Urspronk vum `enu`-Frame (dat `geo` vun enger Opnam) |
| `--no-water` | aus | d'Waasser auslooss |
| `--no-towns` | aus | d'Stad-Foussofdrëck auslooss |
| `--skip-existing` | aus | Mappen auslooss, deenen hir `.glb` schonn existéiert |

All Optioun, esou wéi de Programm se ausgëtt: [Kommando-Referenz](../cli-reference.md).

Setzt `HEAT3D_DEBUG`, fir de ganze Traceback vun enger feelgeschloener Map auszeginn. D'`.glb` gëtt
op `<map>.glb.part` geschriwwen an ëmbenannt, wann se komplett ass.

Exit-Status: 0 all Map geschriwwen, 1 enger feelgeschloen (déi aner ginn trotzdem
geschriwwen), 2 keng Installatioun oder keng Map passt.

## Beispiller {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Wat an den Dateie steet: [D'Level-Dateien an d'Frames](output.md).
