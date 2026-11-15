---
title: "Поиск карт: list"
nav_order: 2
lang: ru
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Поиск карт: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          то же самое, без установки
```

Впервые в командной строке? Сначала прочитайте [С чего начать](before-you-start.md).

1. Установите один раз: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, откройте
   терминал в этой папке и выполните `python -m pip install -e .` (нужен Python 3.10 или новее;
   он подтянет numpy; `python -m pip install -e .[fast]` добавит numba).
2. Выполните `heat3d-il2-level list`.
3. Каждая карта выводит одну строку, разделённую табуляцией: её имя (имя, которое принимает
   `extract`), игру (`Great Battles` или `Korea` для [второй игры](archives-without-table.md)),
   карту высот, которую она читает, и где она лежит на Земле: её прямоугольник широты и долготы по
   углам карты, или подгонка по ориентирам, которая её размещает, или «not placed on the earth»
   (не размещена на Земле). Последняя строка (в stderr) подсчитывает карты и называет установки.

![list на синтетической установке](../assets/img/list.svg)

На картинке — запуск на установке, которую строят тесты (`tests/synth.py`), а не на самой игре.

## Где находятся установки {#where-the-installs-are-found}

Через Steam; иначе `--game <folder>` (можно повторять, по одному на установку) или переменная
окружения `HEAT3D_IL2_GAME`. Установка — это папка, в которой в `data` лежат архивы `Maps*.gtp`.

| Параметр | Что делает |
|---|---|
| `--game FOLDER` | папка IL-2; повторите её для нескольких установок |

Код выхода: 0 — готово; 2 — установка не найдена.
