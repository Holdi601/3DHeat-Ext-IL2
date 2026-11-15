---
title: "Archives sans table des fichiers"
nav_order: 6
lang: "fr"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Un jeu dont les archives n'ont pas de table des fichiers {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea ne conserve aucune table des fichiers lisible dans ses archives (les noms sont
hachés dans un bloc à la fin de chaque archive), et ses fichiers de réglages ne sont pas stockés
lisibles. `list` affiche sa carte avec le jeu `Korea`. Donc :

- sa carte de hauteurs et sa carte d'eau sont trouvées par leur en-tête (la disposition de
  `height.dat`, des secteurs de 128 échantillons ; une très grande grille à pas fin) ;
- elle est posée sur la Terre en ajustant les aérodromes que ses missions placent
  (`data/Missions/**/*.Mission`, lus sur votre ordinateur) aux coordonnées publiées des vrais
  aérodromes (`korea.py`) : écarts de quelques dizaines à quelques centaines de
  mètres. Le JSON liste chaque repère et son écart ;
- heightMul et SeaLevel sont estimés : les navires des missions reposent sur la mer, donc leur
  hauteur au-dessus de la valeur la plus fréquente (la mer) de la carte d'eau donne l'échelle.
  Les hauteurs sont plausibles (la mer sous le niveau de la mer, les villes côtières à quelques
  mètres), sans vérification plus poussée. Le JSON les marque comme estimées.
