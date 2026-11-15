---
title: "Að finna kort: list"
nav_order: 2
lang: is
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Að finna kort: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Hefurðu aldrei notað skipanalínu? Lestu fyrst [Áður en þú byrjar](before-you-start.md).

1. Settu upp einu sinni: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, opnaðu
   skipanalínu í þeirri möppu og keyrðu `python -m pip install -e .` (Python 3.10
   eða nýrra; það kemur með numpy; `python -m pip install -e .[fast]` bætir við numba).
2. Keyrðu `heat3d-il2-level list`.
3. Hvert kort prentar eina línu, aðskilda með tabi: nafn þess (nafnið sem `extract`
   tekur), leikinn (`Great Battles`, eða `Korea` fyrir [seinni leikinn](archives-without-table.md)), hæðarkortið sem það les, og
   hvar það liggur á jörðinni - breiddar-/lengdargráðukassi þess úr hornum
   kortsins, eða kennileitafittunin sem staðsetur það, eða „not placed on the earth“.
   Síðasta línan (á stderr) telur kortin og nefnir uppsetningarnar.

![list á gerviuppsetningu](../assets/img/list.svg)

Myndin er keyrsla á uppsetningu smíðaðri með skrifurum prófananna
(`tests/synth.py`), ekki á leiknum.

## Hvar uppsetningarnar finnast {#where-the-installs-are-found}

Gegnum Steam; annars `--game <folder>` (má endurtaka, ein fyrir hverja uppsetningu) eða
umhverfisbreytan `HEAT3D_IL2_GAME`. Uppsetning er mappa þar sem `data`
geymir `Maps*.gtp` skjalasöfn.

| Valkostur | Gerir |
|---|---|
| `--game FOLDER` | IL-2 mappa; endurtaktu hana fyrir fleiri uppsetningar |

Útgöngustaða: 0 búið, 2 engin uppsetning fannst.
