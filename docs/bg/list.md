---
title: "Намиране на карти: list"
nav_order: 2
lang: bg
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Намиране на карти: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          същото, без инсталиране
```

Нов ли сте в командния ред? Първо прочетете [Преди да започнете](before-you-start.md).

1. Инсталирайте веднъж: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, отворете
   терминал в тази папка и стартирайте `python -m pip install -e .` (Python 3.10
   или по-нов; довежда numpy; `python -m pip install -e .[fast]` добавя numba).
2. Стартирайте `heat3d-il2-level list`.
3. Всяка карта извежда един ред, разделен с табулации: името ѝ (името, което приема `extract`), играта (`Great Battles`, или `Korea` за [втората игра](archives-without-table.md)), височинната карта, която чете, и
   къде е на земята - кутията ѝ по географска ширина и дължина от ъглите на картата, или нагаждането по ориентири, което я поставя, или „not placed on the earth“ (не е поставена на земята).
   Последният ред (в stderr) брои картите и посочва инсталациите.

![list върху синтетична инсталация](../assets/img/list.svg)

Картинката е пускане върху инсталация, изградена от записвачите на тестовете
(`tests/synth.py`), а не върху самата игра.

## Къде се намират инсталациите {#where-the-installs-are-found}

Чрез Steam; иначе `--game <folder>` (може да се повтаря, по една за инсталация) или
променливата на средата `HEAT3D_IL2_GAME`. Инсталацията е папка, чиято `data`
съдържа архиви `Maps*.gtp`.

| Опция | Какво прави |
|---|---|
| `--game FOLDER` | папка на IL-2; повторете я за няколко инсталации |

Статус на изход: 0 - готово; 2 - не е намерена инсталация.
