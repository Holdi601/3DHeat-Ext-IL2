---
title: "Að smíða borð: extract"
nav_order: 3
lang: is
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Að smíða borð: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Skref fyrir skref {#step-by-step}

Hefurðu aldrei notað skipanalínu? Lestu fyrst [Áður en þú byrjar](before-you-start.md).

1. Finndu nafn kortsins með [`list`](list.md).
2. Keyrðu `heat3d-il2-level extract <map> -o levels`. Nöfn mega nota algildisstafi,
   í gæsalöppum (`"<family>_*"`); `--all` tekur öll kort.
3. Til að setja upptöku á borðið án staðsetningarskrefs, gefðu upp upphafspunkt þess:
   `--origin <lat> <lon>` stillt á `geo` upptökunnar (viðmiðunarpunkt lotu
   hennar). Án þess er miðja kortsins upphafspunkturinn, og
   `geo` í `.json` segir hver.
4. Skipunin prentar línu fyrir hvert kort um leið og hún afkóðar það, síðan
   `ok <glb> <triangles> (<frame> frame)` eða `failed <map>: <why>`.
5. Hladdu `<folder>/<map>/<map>.glb` í spjaldið Bakgrunnur / borð í skoðaranum.

![extract á gerviuppsetningu](../assets/img/extract.svg)

Í eigin metrum leiksins, án vatnsins:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Önnur keyrsla yfir kort sem þegar eru skrifuð:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Valkostir {#options}

| Valkostur | Sjálfgefið | Gerir |
|---|---|---|
| `maps` | - | kortanöfn eins og `list` prentar þau; algildisstafir leyfðir |
| `--all` | af | öll kort; árstíðir sem deila hæðarkorti og vatnskorti eru skrifaðar einu sinni |
| `-o`, `--out` | nauðsynlegt | úttaksmappan; hvert kort fer í `<out>/<map>/` |
| `--game FOLDER` | fundin | IL-2 mappa (má endurtaka) |
| `--max-grid N` | `1024` | í mesta lagi svo mörg hæðarkortssýni á hlið (1024: um 2 milljónir þríhyrninga); kortið er sýnatekið á hverju *k*-ta sýni til að passa |
| `--frame` `enu` eða `game` | `enu` | `enu`: metrar til austurs, hæð, til norðurs frá `--origin`, eins og Tacview-töflur Watcher; `game`: eigin metrar leiksins (x norður, y upp, z austur). Kort sem ekki er hægt að setja á jörðina er skrifað í `game` hvað sem beðið er um |
| `--origin LAT LON` | miðja kortsins | upphafspunktur `enu` rammans (`geo` upptöku) |
| `--no-water` | af | sleppa vatninu |
| `--no-towns` | af | sleppa fótsporum bæja |
| `--skip-existing` | af | sleppa kortum sem `.glb` er þegar til fyrir |

Hver valkostur, eins og forritið prentar hann: [Skipanayfirlit](../cli-reference.md).

Stilltu `HEAT3D_DEBUG` til að prenta fulla rakningu (traceback) á korti sem mistókst. `.glb` er
skrifuð í `<map>.glb.part` og endurnefnd þegar hún er tilbúin.

Útgöngustaða: 0 öll kort skrifuð, 1 eitthvert mistókst (hin eru samt
skrifuð), 2 engin uppsetning eða ekkert kort passaði.

## Dæmi {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Hvað er í skránum: [Borðaskrárnar og rammar](output.md).
