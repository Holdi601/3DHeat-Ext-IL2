---
title: "Trouver les cartes : list"
nav_order: 2
lang: "fr"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Trouver les cartes : `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          la même chose, sans installer
```

Vous débutez avec la ligne de commande ? Lisez d'abord [Avant de commencer](before-you-start.md).

1. Installez une fois : `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, ouvrez
   un terminal dans ce dossier et lancez `python -m pip install -e .` (Python 3.10
   ou plus récent ; cela installe numpy ; `python -m pip install -e .[fast]` ajoute numba).
2. Lancez `heat3d-il2-level list`.
3. Chaque carte affiche une ligne, séparée par des tabulations : son nom (le nom que prend `extract`),
   le jeu (`Great Battles`, ou `Korea` pour [le second jeu](archives-without-table.md)), la carte de hauteurs qu'elle lit, et
   sa position sur la Terre - sa boîte latitude/longitude d'après les coins de la carte, ou l'ajustement
   par repères qui la place, ou « not placed on the earth » (non posée sur la Terre). La dernière ligne (sur la sortie d'erreur)
   compte les cartes et nomme les installations.

![list sur une installation synthétique](../assets/img/list.svg)

L'image est une exécution sur une installation construite par les écrivains de tests
(`tests/synth.py`), et non sur le jeu.

## Où les installations sont trouvées {#where-the-installs-are-found}

Par Steam ; sinon `--game <dossier>` (répétable, une par installation) ou la variable d'environnement
`HEAT3D_IL2_GAME`. Une installation est un dossier dont le sous-dossier `data`
contient des archives `Maps*.gtp`.

| Option | Effet |
|---|---|
| `--game FOLDER` | un dossier IL-2 ; répétez-la pour plusieurs installations |

Code de sortie : 0 terminé, 2 aucune installation trouvée.
