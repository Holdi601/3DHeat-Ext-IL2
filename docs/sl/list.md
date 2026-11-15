---
title: "Iskanje zemljevidov: list"
nav_order: 2
lang: "sl"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Iskanje zemljevidov: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game MAPA ...]
python -m heat3d_ext_il2 list ...          isto, brez namestitve
```

Še nisi vajen ukazne vrstice? Najprej preberi [Preden začneš](before-you-start.md).

1. Namesti enkrat: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, odpri terminal v tej mapi in
   zaženi `python -m pip install -e .` (Python 3.10 ali novejši; prinese numpy; `python -m pip install -e .[fast]`
   doda numba).
2. Zaženi `heat3d-il2-level list`.
3. Vsak zemljevid izpiše eno vrstico, ločeno s tabulatorji: njegovo ime (ime, ki ga sprejme `extract`), igro
   (`Great Battles` ali `Korea` za [drugo igro](archives-without-table.md)), višinsko karto, ki jo bere, in kje
   leži na Zemlji - njegovo škatlo zemljepisne širine in dolžine iz vogalov zemljevida, ali prilagajanje z
   orientiri, ki ga postavi, ali »not placed on the earth«. Zadnja vrstica (na standardni napaki) šteje zemljevide
   in imenuje namestitve.

![list na sintetični namestitvi](../assets/img/list.svg)

Slika je zagon na namestitvi, zgrajeni iz pisateljev testov (`tests/synth.py`), ne na igri.

## Kje so namestitve najdene {#where-the-installs-are-found}

Prek Steama; sicer `--game <mapa>` (lahko se ponovi, ena na namestitev) ali spremenljivka okolja
`HEAT3D_IL2_GAME`. Namestitev je mapa, katere `data` vsebuje arhive `Maps*.gtp`.

| Možnost | Naredi |
|---|---|
| `--game MAPA` | mapa IL-2; ponovi jo za več namestitev |

Izhodna koda: 0 opravljeno, 2 ni najdene namestitve.
