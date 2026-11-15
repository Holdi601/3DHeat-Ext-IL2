---
title: "Găsirea hărților: list"
nav_order: 2
lang: "ro"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Găsirea hărților: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Nu ați mai lucrat în linia de comandă? Citiți mai întâi [Înainte de a începe](before-you-start.md).

1. Instalați o singură dată: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, deschideți
   un terminal în acel dosar și rulați `python -m pip install -e .` (Python 3.10 sau mai nou; aduce
   numpy; pentru numba, `python -m pip install -e .[fast]`).
2. Rulați `heat3d-il2-level list`.
3. Fiecare hartă afișează o linie, cu valori separate prin tab: numele său (numele pe care îl primește
   `extract`), jocul (`Great Battles`, sau `Korea` pentru [al doilea joc](archives-without-table.md)), harta
   de înălțimi pe care o citește și locul unde se află pe pământ - caseta sa latitudine/longitudine din
   colțurile hărții, sau potrivirea după repere care o plasează, sau „not placed on the earth” (neplasată pe pământ).
   Ultima linie (la ieșirea de eroare) numără hărțile și numește instalările.

![list pe o instalare sintetică](../assets/img/list.svg)

Imaginea este o rulare pe o instalare construită de teste (`tests/synth.py`), nu pe joc.

## Unde se găsesc instalările {#where-the-installs-are-found}

Prin Steam; altfel `--game <folder>` (care se poate repeta, câte unul pentru fiecare instalare) sau
variabila de mediu `HEAT3D_IL2_GAME`. O instalare este un dosar al cărui `data` conține arhive `Maps*.gtp`.

| Opțiune | Ce face |
|---|---|
| `--game FOLDER` | un dosar IL-2; repetați-l pentru mai multe instalări |

Codul de stare: 0 gata; 2 nu s-a găsit nicio instalare.
