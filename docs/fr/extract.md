---
title: "Construire les niveaux : extract"
nav_order: 3
lang: "fr"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Construire les niveaux : `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<carte> ... | --all) -o <dossier> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Pas à pas {#step-by-step}

Vous débutez avec la ligne de commande ? Lisez d'abord [Avant de commencer](before-you-start.md).

1. Trouvez le nom de la carte avec [`list`](list.md).
2. Lancez `heat3d-il2-level extract <carte> -o levels`. Les noms peuvent utiliser des caractères génériques,
   entre guillemets (`"<famille>_*"`) ; `--all` prend chaque carte.
3. Pour poser un enregistrement sur le niveau sans étape de placement, donnez son origine :
   `--origin <lat> <lon>` avec le `geo` de l'enregistrement (son point de référence de session). Sans cela, le centre
   de la carte sert d'origine, et le `geo` du `.json` indique laquelle.
4. La commande affiche une ligne par carte au fur et à mesure de son décodage, puis
   `ok <glb> <triangles> (repère <frame>)` ou `failed <carte>: <raison>`.
5. Chargez `<dossier>/<carte>/<carte>.glb` dans le panneau Arrière-plan / niveau de la visionneuse.

![extract sur une installation synthétique](../assets/img/extract.svg)

En mètres propres au jeu, sans l'eau :

![extract --frame game --no-water](../assets/img/extract-game.svg)

Une seconde exécution sur des cartes déjà écrites :

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Options {#options}

| Option | Par défaut | Effet |
|---|---|---|
| `cartes` | - | noms de cartes tels que `list` les affiche ; caractères génériques permis |
| `--all` | désactivé | chaque carte ; les saisons qui partagent une carte de hauteurs et une carte d'eau ne sont écrites qu'une fois |
| `-o`, `--out` | obligatoire | le dossier de sortie ; chaque carte va dans `<out>/<carte>/` |
| `--game FOLDER` | trouvé | un dossier IL-2 (répétable) |
| `--max-grid N` | `1024` | nombre maximal d'échantillons de la carte de hauteurs par côté (1024 : environ 2 millions de triangles) ; la carte est échantillonnée tous les *k* échantillons pour tenir |
| `--frame` `enu` ou `game` | `enu` | `enu` : mètres vers l'est, altitude, et vers le nord, par rapport à `--origin`, comme les tableaux Tacview du Watcher ; `game` : les mètres propres au jeu (x nord, y haut, z est). Une carte qui ne peut pas être posée sur la Terre est écrite en `game` quoi qu'on demande |
| `--origin LAT LON` | le centre de la carte | l'origine du repère `enu` (le `geo` d'un enregistrement) |
| `--no-water` | désactivé | omettre l'eau |
| `--no-towns` | désactivé | omettre les emprises des villes |
| `--skip-existing` | désactivé | laisser de côté les cartes dont le `.glb` existe déjà |

Chaque option, telle que le programme l'affiche : [Référence des commandes](../cli-reference.md).

Définissez `HEAT3D_DEBUG` pour afficher la trace complète d'une carte en échec. Le `.glb` est
écrit dans `<carte>.glb.part`, puis renommé une fois terminé.

Code de sortie : 0 toutes les cartes écrites ; 1 au moins une en échec (les autres sont tout de même
écrites) ; 2 aucune installation ou aucune carte trouvée.

## Exemples {#examples}

```bash
heat3d-il2-level extract <carte> -o levels                         # une carte, repère enu autour de son centre
heat3d-il2-level extract <carte> --origin <lat> <lon> -o levels    # dans la carte plate d'un enregistrement avec ce geo
heat3d-il2-level extract "<famille>_*" --max-grid 2048 -o levels   # plus fin, plusieurs cartes
heat3d-il2-level extract --all --skip-existing -o levels           # chaque carte, seulement les nouvelles
heat3d-il2-level extract <carte> --frame game -o levels            # les mètres propres au jeu, comme dans les fichiers de mission
```

Ce qui se trouve dans les fichiers : [Les fichiers de niveau et les repères](output.md).
