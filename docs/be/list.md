---
title: "Пошук карт: list"
nav_order: 2
lang: "be"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Пошук карт: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Упершыню ў камандным радку? Спачатку прачытайце [Перад пачаткам](before-you-start.md).

1. Усталюйце адзін раз: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, адкрыйце
   тэрмінал у гэтай папцы і выканайце `python -m pip install -e .` (Python 3.10
   або навейшы; ён прыносіць numpy; `python -m pip install -e .[fast]` дадае numba).
2. Выканайце `heat3d-il2-level list`.
3. Кожная карта друкуецца ў адным радку, праз табуляцыю: яе назва (імя, якое
   прымае `extract`), гульня (`Great Battles` або `Korea` для [другой гульні](archives-without-table.md)), карта вышынь, якую яна чытае, і
   дзе яна ляжыць на зямлі - скрынка шыраты/даўгаты па вуглах
   карты, або падгонка па арыенцірах, што яе змяшчае, або «not placed on the earth».
   Апошні радок (у stderr) лічыць карты і называе ўсталёўкі.

![list на сінтэтычнай усталёўцы](../assets/img/list.svg)

Малюнак — гэта запуск на ўсталёўцы, якую будуюць тэсты
(`tests/synth.py`), а не на гульні.

## Дзе знаходзяцца ўсталёўкі {#where-the-installs-are-found}

Праз Steam; інакш `--game <folder>` (можна паўтараць, па адной на ўсталёўку) або
зменная асяроддзя `HEAT3D_IL2_GAME`. Усталёўка — гэта папка, у чыім `data`
ёсць архівы `Maps*.gtp`.

| Опцыя | Што робіць |
|---|---|
| `--game FOLDER` | папка IL-2; паўтарайце для некалькіх усталёвак |

Статус выхаду: 0 — гатова, 2 — усталёўка не знойдзена.
