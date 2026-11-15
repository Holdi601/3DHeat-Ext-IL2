---
title: "Comment les fichiers sont lus"
nav_order: 5
lang: fr
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Comment les fichiers sont lus {#how-the-files-are-read}

| Partie | État |
|---|---|
| Archives (`data/*.gtp`, Great Battles) | la table des fichiers (enregistrements `S16R`, `STRMFAT?`, `DIR!`/`FILE`) et les entrées (en-tête `STRMFILE`, données stockées telles quelles) ; chaque `Maps*.gtp` de l'installation de test |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, les limites de jeu et `MapNW/NE/SE/SW` ; chacun de l'installation de test |
| Cartes de hauteurs (`height.dat`) | le codec ci-dessous ; chaque secteur des cartes décodé en entier pendant le travail utilise exactement son flux de bits (au plus le remplissage d'octets restant), le reste vérifié par l'en-tête. Vérifié bit à bit contre les fichiers `distlod.raw` non compressés que le jeu livre à côté de leur `distlod.dat`, et contre la carte de hauteurs de détail lointain d'une carte (corrélation 0,999) |
| Hauteurs | mètres = brut x heightMul / 256 - SeaLevel x heightMul. La mer d'une carte se décode exactement à la hauteur indiquée par les commentaires de son hini ; la bordure d'une autre à son `bounds_level` |
| Placement | bilinéaire entre les quatre coins du hini, ligne 0 au nord, colonne 0 à l'ouest. Vérifié sur une carte contre des villes, côtes et mers connues (hauteurs des villes à environ 10 m des vraies, les mers sous le niveau de la mer). Les coins forment un quadrilatère, non la projection propre au jeu : attendez-vous à quelques centaines de mètres d'erreur au milieu d'une grande carte. Le hini d'une famille de cartes porte les coins d'une autre carte (ils couvrent une fraction de sa taille réelle) ; cela est détecté, et cette famille est placée à la place par un ajustement par repères : villes et aérodromes des bases de positions propres au jeu (`*.ldfbin`) comparés à leurs positions réelles, écart quadratique moyen de deux kilomètres environ (villes comparées aux aérodromes qui portent leur nom, et coordonnées des lieux réels à un kilomètre près) ; le JSON liste chaque repère et son écart |
| Masque d'eau (`water.wtr` : quatre niveaux de pyramide de tuiles, chaque tuile une table de blocs de 400 m, chaque bloc terre, plein ou partiellement en eau avec sa forme dans un flux de bits) | le conteneur est lu sur chaque carte (aucun octet restant sur les fichiers décodés en entier) ; la forme à l'intérieur d'un bloc partiellement en eau n'est **pas décodée**. Les blocs pleins sont de l'eau ; dans les blocs partiellement en eau, un échantillon est de l'eau là où la carte d'eau (`height_w.dat`, même codec que la carte de hauteurs) est au-dessus du sol, ou, à côté d'un lac, là où le sol n'est pas plus haut que le lac ; les blocs terrestres sont secs. Cela supprime le marais que la seule carte d'eau signale comme eau. Les rivières plus étroites que la grille de sortie apparaissent brisées en morceaux |
| Emprises des villes (les mailles de décalque que liste `textures.tini` : `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ... : des tuiles de 25,6 km de triangles plats texturés) | lues sur chaque carte ; les faces dont la texture est une ville, un village ou un sol industriel sont gardées. Vérifié contre les vraies villes sur quelques cartes (une ville sur les deux rives d'une rivière, un confluent). Ce sont des emprises : le jeu place les bâtiments à l'exécution, et les fichiers ne contiennent pas de bâtiments |
| Aérodromes, ponts, bâtiments | **non lus** : les aérodromes sont des objets de mission, les bâtiments viennent du placement propre au jeu |
| Forêts (`forest_map.wtr`) | ses blocs se lisent de la même façon, mais presque chaque bloc est « partiellement en forêt », donc sans le flux de bits il n'y a pas de masque de forêt utilisable ; non dessinées |
| Les textures du sol | non lues |

## Le codec des cartes de hauteurs {#the-heightmap-codec}

Établi à partir des seuls fichiers de données ; aucun code du jeu n'a été lu ni désassemblé.
Little-endian :

```text
u32 largeur, u32 hauteur, u32 secteursX, u32 secteursY, u32 tailleSecteur, f32 tailleCase
u32 décalage[secteursX * secteursY]        depuis le début du fichier, ligne par ligne, la ligne du haut d'abord
secteur : u16 nombre (octets qui suivent), u16 mode ((log2 tailleSecteur) << 4 | LW, LW = 4),
          puis un flux de bits lu MSB d'abord :
  PRE   2 * (log2(tailleSecteur) - 5) bits, toujours 0 jusqu'ici
  LIT   le premier échantillon : signe (1), n (LW bits), amplitude (n + 1 bits)
  puis jusqu'à ce que le secteur soit plein :
    0 LIT       suivant = précédent + LIT
    1 RUN LIT   l'échantillon précédent se répète RUN fois (k : 3 bits, m : k + 1 bits, RUN = m + 1),
                puis (sauf si le secteur est plein) suivant = précédent + LIT
  les valeurs sont sur 16 bits : lues modulo 65536
```

Les secteurs partiels aux bords droit et bas sont complétés puis rognés. Le même
codec vaut pour la carte d'eau et pour la carte de hauteurs de détail lointain.

## Ajustements par repères {#landmark-fits}

Lorsque les coins d'une carte ne peuvent pas servir, `landmarks.py` ajuste une transformation affine
des mètres du jeu vers la Terre par moindres carrés : positions dans le jeu issues de vos propres
fichiers (blocs `Airfield` des missions, bases de positions de la carrière), positions réelles issues de
tableaux des coordonnées publiées des lieux, dans le code. Le `georeference` du JSON contient la
matrice, l'origine, chaque repère avec son écart, et l'écart quadratique moyen.
