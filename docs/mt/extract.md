---
title: "Nibnu livelli: extract"
nav_order: 3
lang: "mt"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Nibnu livelli: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Pass b'pass {#step-by-step}

Ġdid mal-linja tal-kmandi? Aqra [Qabel ma tibda](before-you-start.md) l-ewwel.

1. Sib l-isem tal-mappa b'[`list`](list.md).
2. Ħaddem `heat3d-il2-level extract <map> -o levels`. L-ismijiet jistgħu jużaw wildcards,
   bejn il-virgoletti (`"<family>_*"`); `--all` jieħu kull mappa.
3. Biex tqiegħed reġistrazzjoni fuq il-livell mingħajr pass ta' tqegħid, agħti l-oriġini tagħha:
   `--origin <lat> <lon>` issettjat għall-`geo` tar-reġistrazzjoni (il-punt ta'
   referenza tas-sessjoni tagħha). Mingħajru ċ-ċentru tal-mappa huwa l-oriġini, u
   il-`geo` tal-`.json` jgħid liema.
4. Il-kmand jistampa linja għal kull mappa waqt li jiddekodifikaha, imbagħad
   `ok <glb> <triangles> (<frame> frame)` jew `failed <map>: <why>`.
5. Tgħabbi `<folder>/<map>/<map>.glb` fil-pannell Sfond / livell tal-viewer.

![extract fuq installazzjoni sintetika](../assets/img/extract.svg)

Fil-metri proprji tal-logħba, mingħajr l-ilma:

![extract --frame game --no-water](../assets/img/extract-game.svg)

It-tieni użu fuq mapep diġà miktuba:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Għażliet {#options}

| Għażla | Default | X'jagħmel |
|---|---|---|
| `maps` | - | ismijiet tal-mapep kif jistampahom `list`; wildcards permessi |
| `--all` | mitfi | kull mappa; staġuni li jaqsmu heightmap u water map jinkitbu darba |
| `-o`, `--out` | meħtieġa | il-folder tal-output; kull mappa tmur f'`<out>/<map>/` |
| `--game FOLDER` | misjub | folder ta' IL-2 (jista' jiġi ripetut) |
| `--max-grid N` | `1024` | l-aktar kampjuni tal-heightmap kull naħa (1024: madwar 2 miljun trijangolu); il-mappa titkampjona kull *k* kampjuni biex tidħol |
| `--frame` `enu` jew `game` | `enu` | `enu`: metri lvant, altitudni, tramuntana minn `--origin`, bħat-tabelli Tacview tal-Watcher; `game`: il-metri proprji tal-logħba (x tramuntana, y 'il fuq, z lvant). Mappa li ma tistax titqiegħed fuq l-art tinkiteb f'`game` minkejja dak mitlub |
| `--origin LAT LON` | iċ-ċentru tal-mappa | l-oriġini tal-frame `enu` (il-`geo` ta' reġistrazzjoni) |
| `--no-water` | mitfi | ħalli l-ilma barra |
| `--no-towns` | mitfi | ħalli barra l-footprints tal-irħula |
| `--skip-existing` | mitfi | ħalli mapep li l-`.glb` tagħhom diġà jeżisti |

Kull għażla, kif jistampaha l-programm: [Referenza tal-kmandi](../cli-reference.md).

Issettja `HEAT3D_DEBUG` biex jistampa t-traceback sħiħ ta' mappa li fallet. Il-`.glb` jinkiteb
f'`<map>.glb.part` u jinbidel isimu meta jkun komplut.

Status tal-ħruġ: 0 kull mappa nkitbet, 1 xi waħda falliet (l-oħrajn xorta
nkitbu), 2 ebda installazzjoni jew mappa ma qabblet.

## Eżempji {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

X'hemm fil-fajls: [Il-fajls tal-livell u l-frames](output.md).
