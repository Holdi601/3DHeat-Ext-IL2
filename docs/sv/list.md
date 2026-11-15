---
title: "Hitta kartor: list"
nav_order: 2
lang: sv
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Hitta kartor: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          samma sak, utan att installera
```

Har du aldrig använt kommandoraden förut? Läs [Innan du börjar](before-you-start.md) först.

1. Installera en gång: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, öppna
   en terminal i mappen och kör `python -m pip install -e .` (Python 3.10
   eller senare; det tar med sig numpy; `python -m pip install -e .[fast]` lägger till numba).
2. Kör `heat3d-il2-level list`.
3. Varje karta skriver en rad, med tabb mellan fälten: dess namn (namnet `extract`
   tar), spelet (`Great Battles`, eller `Korea` för [det andra spelet](archives-without-table.md)), höjdkartan den läser, och
   var den ligger på jorden - dess latitud/longitud-ruta från kartans hörn, eller landmärkesanpassningen som placerar den, eller "not placed on the earth".
   Den sista raden (på stderr) räknar kartorna och anger installationerna.

![list på en syntetisk installation](../assets/img/list.svg)

Bilden är en körning på en installation byggd av testernas skrivare
(`tests/synth.py`), inte på spelet.

## Var installationerna hittas {#where-the-installs-are-found}

Via Steam; annars `--game <folder>` (kan upprepas, en per installation) eller
miljövariabeln `HEAT3D_IL2_GAME`. En installation är en mapp vars `data`
innehåller `Maps*.gtp`-arkiv.

| Alternativ | Gör |
|---|---|
| `--game FOLDER` | en IL-2-mapp; upprepa den för flera installationer |

Avslutskod: 0 klart, 2 ingen installation hittades.
