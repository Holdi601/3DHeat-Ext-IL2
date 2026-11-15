---
title: "Налажење мапа: list"
nav_order: 2
lang: sr
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Налажење мапа: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          исто, без инсталације
```

Први пут у командној линији? Прво прочитајте [Пре почетка](before-you-start.md).

1. Инсталирајте једном: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, отворите
   терминал у тој фасцикли и покрените `python -m pip install -e .` (Python 3.10
   или новији; доноси numpy; `python -m pip install -e .[fast]` додаје numba).
2. Покрените `heat3d-il2-level list`.
3. Свака мапа исписује један ред, раздвојен табулатором: њено име (име које
   узима `extract`), игру (`Great Battles`, или `Korea` за [другу игру](archives-without-table.md)), висинску мапу коју чита, и
   где лежи на Земљи - њену кутију географске ширине и дужине из углова мапе,
   или уклапање по орјентирима које је смешта, или „not placed on the earth" (није
   смештена на Земљу). Последњи ред (на stderr) броји мапе и именује инсталације.

![list на синтетичкој инсталацији](../assets/img/list.svg)

Слика је покретање над инсталацијом направљеном од писача из тестова
(`tests/synth.py`), а не над самом игром.

## Где се инсталације налазе {#where-the-installs-are-found}

Преко Steam-а; иначе `--game <folder>` (може више пута, по једна за сваку
инсталацију) или променљива окружења `HEAT3D_IL2_GAME`. Инсталација је фасцикла
чији `data` садржи `Maps*.gtp` архиве.

| Опција | Шта ради |
|---|---|
| `--game FOLDER` | IL-2 фасцикла; понови је за више инсталација |

Излазни статус: 0 готово, 2 није нађена инсталација.
