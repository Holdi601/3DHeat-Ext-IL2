---
title: "Vitesse, tests, conditions"
nav_order: 7
lang: "fr"
source: terms.md
source_hash: "3baa9f57ade6"
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

Cet outil lit les archives de votre propre installation d'IL-2 Sturmovik: Great Battles, sur votre ordinateur, et ne les modifie jamais.

Rien du jeu n'est livré ni redistribué : aucun fichier du jeu, aucun code du jeu, aucune DLL ; les tests construisent eux-mêmes chaque fichier qu'ils lisent. Les niveaux qu'il écrit restent sur votre machine.

3DHeat IL-2 n'est ni affilié à 1C Game Studios / 777 Studios ni approuvé par celui-ci. IL-2 Sturmovik ainsi que les noms et marques associés appartiennent à leurs propriétaires.

Ayants droit : ouvrez un ticket sur [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - nous répondons rapidement et retirons tout élément sur demande.

## Licence {#licence}

MIT - voir [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Utilise numpy (BSD-3-Clause) et, en option,
numba (BSD-2-Clause). `heat3d_ext_il2.update` est l'outil de mise à jour commun des outils 3DHeat.
