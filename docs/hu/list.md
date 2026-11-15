---
title: "Térképek keresése: list"
nav_order: 2
lang: hu
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Térképek keresése: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          ugyanaz, telepítés nélkül
```

Még nem használt parancssort? Előbb olvasd el a [Mielőtt elkezded](before-you-start.md) oldalt.

1. Telepítés egyszer: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, nyiss terminált ebben a
   mappában, és futtasd a `python -m pip install -e .` parancsot (Python 3.10 vagy újabb; ez hozza a numpy-t;
   a `python -m pip install -e .[fast]` a numba-t is hozzáadja).
2. Futtasd a `heat3d-il2-level list` parancsot.
3. Minden térkép egy sort ír ki, tabulátorral elválasztva: a nevét (ezt veszi át az `extract`), a játékot
   (`Great Battles`, vagy `Korea` [a második játékhoz](archives-without-table.md)), a magassági térképet, amelyet
   olvas, és hogy hol fekszik a földön – a szélességi/hosszúsági fokos doboza a térkép sarkaiból, vagy az a
   tájékozódó illesztés, amely elhelyezi, vagy a „not placed on the earth” (nincs elhelyezve a földön) szöveg.
   Az utolsó sor (a szabványos hibakimeneten) megszámolja a térképeket, és megnevezi a telepítéseket.

![list egy szintetikus telepítésen](../assets/img/list.svg)

Az ábra egy olyan telepítésen készült futtatás, amelyet a tesztek íróiből építettek (`tests/synth.py`),
nem a játékon.

## Hol találhatók a telepítések {#where-the-installs-are-found}

A Steamen keresztül; egyébként a `--game <folder>` (ismételhető, telepítésenként egy), vagy a
`HEAT3D_IL2_GAME` környezeti változó. Telepítés az a mappa, amelynek `data` mappájában `Maps*.gtp` archívumok vannak.

| Kapcsoló | Mit csinál |
|---|---|
| `--game FOLDER` | egy IL-2 mappa; több telepítéshez ismételje meg |

Kilépési állapot: 0 kész, 2 nem található telepítés.
