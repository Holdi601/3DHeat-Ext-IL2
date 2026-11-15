---
title: "Градење нивоа: extract"
nav_order: 3
lang: "mk"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Градење нивоа: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Чекор по чекор {#step-by-step}

Нови сте со командната линија? Прво прочитајте [Пред да започнете](before-you-start.md).

1. Најдете го името на мапата со [`list`](list.md).
2. Пуштете `heat3d-il2-level extract <map> -o levels`. Имињата може да користат џокери (wildcards),
   во наводници (`"<family>_*"`); `--all` ја зема секоја мапа.
3. За да поставите снимка на нивото без чекор за поставување, дајте го нејзиното потекло:
   `--origin <lat> <lon>` поставено на `geo` на снимката (референтната точка на нејзината
   сесија). Без тоа, центарот на мапата е потеклото, а
   `geo` во `.json` кажува кое.
4. Командата печати по една линија за мапа додека ја декодира, потоа
   `ok <glb> <triangles> (<frame> frame)` или `failed <map>: <why>`.
5. Вчитајте `<folder>/<map>/<map>.glb` во панелот Позадина / ниво на прегледувачот.

![extract на синтетичка инсталација](../assets/img/extract.svg)

Во сопствените метри на играта, без водата:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Второ извршување над веќе запишани мапи:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Опции {#options}

| Опција | Стандардно | Што прави |
|---|---|---|
| `maps` | - | имиња на мапи како што ги печати `list`; џокери се дозволени |
| `--all` | исклучено | секоја мапа; сезоните што делат мапа на височини и мапа на вода се запишуваат еднаш |
| `-o`, `--out` | задолжително | излезната папка; секоја мапа оди во `<out>/<map>/` |
| `--game FOLDER` | пронајдена | папка на IL-2 (може да се повтори) |
| `--max-grid N` | `1024` | најмногу примероци од мапата на височини по страна (1024: околу 2 милиони триаголници); мапата се семплира на секои *k* примероци за да собере |
| `--frame` `enu` или `game` | `enu` | `enu`: метри на исток, висина, на север од `--origin`, како табелите Tacview на Watcher; `game`: сопствените метри на играта (x север, y нагоре, z исток). Мапа што не може да се постави на земјата се пишува во `game` како и да е побарано |
| `--origin LAT LON` | центарот на мапата | потеклото на рамката `enu` (`geo` на снимка) |
| `--no-water` | исклучено | ја изоставува водата |
| `--no-towns` | исклучено | ги изоставува отпечатоците на градовите |
| `--skip-existing` | исклучено | ги прескокнува мапите чија `.glb` веќе постои |

Секоја опција, како што ја печати програмата: [Упатство за команди](../cli-reference.md).

Поставете `HEAT3D_DEBUG` за да се испечати целиот traceback на мапа што не успеала. `.glb` се
пишува во `<map>.glb.part` и се преименува кога ќе заврши.

Излезен статус: 0 секоја мапа е запишана, 1 било која не успеала (останатите сепак се
запишани), 2 не е пронајдена инсталација или мапа што се совпаѓа.

## Примери {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Што има во датотеките: [Датотеките на нивото и рамките](output.md).
