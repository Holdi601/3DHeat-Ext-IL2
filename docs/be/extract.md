---
title: "Пабудова ўзроўняў: extract"
nav_order: 3
lang: "be"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Пабудова ўзроўняў: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Крок за крокам {#step-by-step}

Упершыню ў камандным радку? Спачатку прачытайце [Перад пачаткам](before-you-start.md).

1. Знайдзіце назву карты праз [`list`](list.md).
2. Выканайце `heat3d-il2-level extract <map> -o levels`. У назвах можна выкарыстоўваць
   сімвалы падстаноўкі ў двукоссі (`"<family>_*"`); `--all` бярэ кожную карту.
3. Каб запіс ляжаў на ўзроўні без этапу размяшчэння, дайце яго пачатак адліку:
   `--origin <lat> <lon>`, роўны `geo` запісу (апорная
   кропка яго сесіі). Без гэтага пачаткам адліку з'яўляецца цэнтр карты, а
   `geo` у `.json` кажа, які менавіта.
4. Каманда друкуе радок на кожную карту па меры яе расшыфроўкі, потым
   `ok <glb> <triangles> (<frame> frame)` або `failed <map>: <why>`.
5. Загрузіце `<folder>/<map>/<map>.glb` на панэлі «Фон / узровень» праглядальніка.

![extract на сінтэтычнай усталёўцы](../assets/img/extract.svg)

Ва ўласных метрах гульні, без вады:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Другі запуск па картах, што ўжо запісаны:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Опцыі {#options}

| Опцыя | Па змаўчанні | Што робіць |
|---|---|---|
| `maps` | - | назвы карт, як іх друкуе `list`; сімвалы падстаноўкі дазволены |
| `--all` | выключана | кожная карта; сезоны, што дзеляць карту вышынь і карту вады, пішуцца адзін раз |
| `-o`, `--out` | абавязкова | выходная папка; кожная карта ідзе ў `<out>/<map>/` |
| `--game FOLDER` | знаходзіцца | папка IL-2 (можна паўтараць) |
| `--max-grid N` | `1024` | максімум адзнак карты вышынь на бок (1024: каля 2 мільёнаў трохвугольнікаў); карта бярэцца праз кожныя *k* адзнак, каб улезці |
| `--frame` `enu` або `game` | `enu` | `enu`: метры на ўсход, вышыня, на поўнач ад `--origin`, як у табліцах Tacview у Watcher; `game`: уласныя метры гульні (x на поўнач, y уверх, z на ўсход). Карта, якую нельга змясціць на зямлю, пішацца ў `game`, што б ні прасілі |
| `--origin LAT LON` | цэнтр карты | пачатак адліку сістэмы `enu` (`geo` запісу) |
| `--no-water` | выключана | не ўключаць ваду |
| `--no-towns` | выключана | не ўключаць контуры гарадоў |
| `--skip-existing` | выключана | прапусціць карты, чый `.glb` ужо існуе |

Кожная опцыя, як яе друкуе праграма: [Даведнік каманд](../cli-reference.md).

Задайце `HEAT3D_DEBUG`, каб надрукаваць поўны traceback збойнай карты. `.glb`
пішацца ў `<map>.glb.part` і перайменоўваецца, калі гатовы.

Статус выхаду: 0 — кожная карта запісана, 1 — якая-небудзь не ўдалася (астатнія
усё роўна запісаны), 2 — няма ўсталёўкі або ніводная карта не падышла.

## Прыклады {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Што ў файлах: [Файлы ўзроўню і сістэмы каардынат](output.md).
