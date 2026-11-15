---
title: "Finne kart: list"
nav_order: 2
lang: "no"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Finne kart: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          det samme, uten å installere
```

Ny til kommandolinjen? Les [Før du starter](before-you-start.md) først.

1. Installer én gang: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, åpne
   en terminal i den mappen og kjør `python -m pip install -e .` (Python 3.10
   eller nyere; det henter numpy; `python -m pip install -e .[fast]` legger til numba).
2. Kjør `heat3d-il2-level list`.
3. Hvert kart skriver ut én linje, tabulatorskilt: navnet (navnet `extract`
   tar), spillet (`Great Battles`, eller `Korea` for [det andre spillet](archives-without-table.md)), høydekartet det leser, og
   hvor det ligger på jorden - breddegrad/lengdegrad-boksen fra kartets
   hjørner, eller landemerketilpasningen som plasserer det, eller «not placed on the earth».
   Den siste linjen (på stderr) teller kartene og nevner installasjonene.

![list på en syntetisk installasjon](../assets/img/list.svg)

Bildet er en kjøring på en installasjon bygget av testenes skrivere
(`tests/synth.py`), ikke på spillet.

## Hvor installasjonene finnes {#where-the-installs-are-found}

Via Steam; ellers `--game <folder>` (kan gjentas, én per installasjon) eller
miljøvariabelen `HEAT3D_IL2_GAME`. En installasjon er en mappe der `data`
holder `Maps*.gtp`-arkiver.

| Alternativ | Gjør |
|---|---|
| `--game FOLDER` | en IL-2-mappe; gjenta den for flere installasjoner |

Avslutningsstatus: 0 ferdig, 2 ingen installasjon funnet.
