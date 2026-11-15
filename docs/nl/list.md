---
title: "Kaarten zoeken: list"
nav_order: 2
lang: nl
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Kaarten zoeken: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          hetzelfde, zonder te installeren
```

Nog nooit met de opdrachtregel gewerkt? Lees eerst [Voordat je begint](before-you-start.md).

1. Installeer eenmalig: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, open
   een terminal in die map en voer `python -m pip install -e .` uit (Python 3.10
   of later; het haalt numpy mee; `python -m pip install -e .[fast]` voegt numba toe).
2. Voer `heat3d-il2-level list` uit.
3. Elke kaart drukt één regel af, met tabs ertussen: zijn naam (de naam die `extract`
   gebruikt), het spel (`Great Battles`, of `Korea` voor [het tweede spel](archives-without-table.md)), de hoogtekaart die hij leest, en
   waar hij op aarde ligt - zijn vak in breedte-/lengtegraad uit de hoeken van de kaart,
   of de oriëntatiepuntenpassing die hem plaatst, of "not placed on the earth".
   De laatste regel (op stderr) telt de kaarten en noemt de installaties.

![list op een synthetische installatie](../assets/img/list.svg)

De afbeelding is een run op een installatie die is gebouwd met de schrijvers van de tests
(`tests/synth.py`), niet op het spel zelf.

## Waar de installaties worden gevonden {#where-the-installs-are-found}

Via Steam; anders `--game <folder>` (herhaalbaar, één per installatie) of de
omgevingsvariabele `HEAT3D_IL2_GAME`. Een installatie is een map waarvan `data`
`Maps*.gtp`-archieven bevat.

| Optie | Doet |
|---|---|
| `--game FOLDER` | een IL-2-map; herhaal hem voor meerdere installaties |

Exitstatus: 0 klaar, 2 geen installatie gevonden.
