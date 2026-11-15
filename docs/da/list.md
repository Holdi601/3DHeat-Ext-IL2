---
title: "Find kort: list"
nav_order: 2
lang: da
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Find kort: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Ny til kommandolinjen? Læs [Før du går i gang](before-you-start.md) først.

1. Installer én gang: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, åbn
   en terminal i den mappe, og kør `python -m pip install -e .` (Python 3.10
   eller nyere; det henter numpy med sig; `python -m pip install -e .[fast]` tilføjer numba).
2. Kør `heat3d-il2-level list`.
3. Hvert kort udskriver én linje, tabulator-adskilt: dets navn (det navn `extract`
   tager), spillet (`Great Battles`, eller `Korea` for [det andet spil](archives-without-table.md)), højdekortet det læser, og
   hvor det ligger på jorden - dets breddegrad/længdegrad-boks ud fra kortets
   hjørner, eller den landemærketilpasning, der placerer det, eller "not placed on the earth" (ikke placeret på jorden).
   Den sidste linje (på stderr) tæller kortene og navngiver installationerne.

![list på en syntetisk installation](../assets/img/list.svg)

Billedet er en kørsel på en installation bygget af testenes skrivere
(`tests/synth.py`), ikke på spillet.

## Hvor installationerne findes {#where-the-installs-are-found}

Via Steam; ellers `--game <folder>` (kan gentages, én pr. installation) eller
miljøvariablen `HEAT3D_IL2_GAME`. En installation er en mappe, hvis `data`
indeholder `Maps*.gtp`-arkiver.

| Valgmulighed | Gør |
|---|---|
| `--game FOLDER` | en IL-2-mappe; gentag den for flere installationer |

Exit-status: 0 færdig, 2 ingen installation fundet.
