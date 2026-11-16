---
title: "Vitesse, tests, conditions"
nav_order: 7
lang: "fr"
source: terms.md
source_hash: "09281b2a1fe2"
nav_exclude: true
search_exclude: true
---
# Vitesse, tests, conditions {#speed-tests-terms}

## Vitesse {#speed}

Le décodage est en Python pur, sauf si numba est installé (`python -m pip install -e .[fast]`) :
une carte de taille moyenne prend environ 15 s sans lui et environ une seconde avec lui ; la plus
grande carte, plusieurs centaines de millions d'échantillons, environ 7 s avec lui (la première
exécution compile aussi). La mémoire reste à une rangée de secteurs plus la grille de sortie.

## Tests {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` construit en code des archives, des cartes de hauteurs (un encodeur du codec ci-dessus),
des fichiers `height.hini` et des archives sans table des fichiers.

## Les conditions {#the-terms}

Le contrat de licence d'IL-2 Sturmovik: Great Battles et d'IL-2 Series (1C Game
Studios / 777 Studios) n'a **pas été trouvé** : ni dans l'installation (dont
`data/Licenses.txt` ne contient que des licences tierces), ni sur le site de l'éditeur,
et la page du CLUF de Steam ne s'est pas chargée. Vérifiez-le vous-même avant de vous y fier.
Cet outil ne fait que lire les archives et ne les modifie jamais. Les niveaux qu'il écrit restent
sur votre ordinateur : **ne les publiez jamais**. Rien ici ne livre de données de jeu, et les
tests construisent chaque fichier qu'ils lisent.

## Licence {#licence}

MIT - voir [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Utilise numpy (BSD-3-Clause) et, en option,
numba (BSD-2-Clause). `heat3d_ext_il2.update` est l'outil de mise à jour commun des outils 3DHeat.
