---
title: "Пошук карт: list"
nav_order: 2
lang: uk
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Пошук карт: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          те саме, але без встановлення
```

Ви лише починаєте працювати з командним рядком? Спершу прочитайте [Перш ніж почати](before-you-start.md).

1. Встановіть один раз: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, відкрийте
   термінал у цій папці і виконайте `python -m pip install -e .` (Python 3.10 або
   новіший; він приносить numpy; `python -m pip install -e .[fast]` додає numba).
2. Виконайте `heat3d-il2-level list`.
3. Кожна карта виводить один рядок, розділений табуляціями: її назву (назву, яку
   приймає `extract`), гру (`Great Battles` або `Korea` для [другої гри](archives-without-table.md)),
   карту висот, яку вона читає, і де вона лежить на Землі — її коробку широти/довготи
   за кутами карти, або підгонку за орієнтирами, яка її розміщує, або «not placed on the earth»
   (не розміщено на Землі). Останній рядок (у stderr) рахує карти і називає інсталяції.

![list на синтетичній інсталяції](../assets/img/list.svg)

Малюнок — це запуск на інсталяції, побудованій засобами тестів (`tests/synth.py`), а
не на самій грі.

## Де шукаються інсталяції {#where-the-installs-are-found}

Через Steam; інакше `--game <folder>` (можна повторювати, по одному на інсталяцію) або
змінна середовища `HEAT3D_IL2_GAME`. Інсталяція — це папка, у `data` якої є архіви
`Maps*.gtp`.

| Параметр | Що робить |
|---|---|
| `--game FOLDER` | папка IL-2; повторіть його для кількох інсталяцій |

Код виходу: 0 — готово, 2 — інсталяцію не знайдено.
