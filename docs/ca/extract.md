---
title: "Construir nivells: extract"
nav_order: 3
lang: ca
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Construir nivells: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<mapa> ... | --all) -o <carpeta> [--game CARPETA ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Pas a pas {#step-by-step}

Si ets nou amb la línia d'ordres, llegeix primer [Abans de començar](before-you-start.md).

1. Troba el nom del mapa amb [`list`](list.md).
2. Executa `heat3d-il2-level extract <mapa> -o levels`. Els noms poden usar comodins,
   entre cometes (`"<família>_*"`); `--all` pren cada mapa.
3. Per posar una gravació sobre el nivell sense cap pas de col·locació, indica el seu origen:
   `--origin <lat> <lon>` amb el `geo` de la gravació (el punt de referència de la seva sessió).
   Sense això, el centre del mapa és l'origen, i el `geo` del `.json` indica quin és.
4. L'ordre imprimeix una línia per mapa a mesura que el descodifica, i després
   `ok <glb> <triangles> (<marc> frame)` o `failed <mapa>: <per què>`.
5. Carrega `<carpeta>/<mapa>/<mapa>.glb` al panell Fons / nivell del visualitzador.

![extract sobre una instal·lació sintètica](../assets/img/extract.svg)

En els metres propis del joc, sense l'aigua:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Una segona execució sobre mapes ja escrits:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opcions {#options}

| Opció | Per defecte | Què fa |
|---|---|---|
| `maps` | - | noms de mapa tal com els imprimeix `list`; es permeten comodins |
| `--all` | desactivada | cada mapa; les temporades que comparteixen un mapa d'alçades i un mapa d'aigua s'escriuen una sola vegada |
| `-o`, `--out` | obligatòria | la carpeta de sortida; cada mapa va a `<sortida>/<mapa>/` |
| `--game CARPETA` | trobada | una carpeta d'IL-2 (es pot repetir) |
| `--max-grid N` | `1024` | com a màxim, les mostres del mapa d'alçades per costat (1024: uns 2 milions de triangles); el mapa es mostreja cada *k* mostres per encaixar-hi |
| `--frame` `enu` o `game` | `enu` | `enu`: metres a l'est, altitud, i nord respecte de `--origin`, com les taules Tacview del Watcher; `game`: els metres propis del joc (x nord, y amunt, z est). Un mapa que no es pot col·locar a la Terra s'escriu en `game` sigui el que sigui el que es demani |
| `--origin LAT LON` | el centre del mapa | l'origen del marc `enu` (el `geo` d'una gravació) |
| `--no-water` | desactivada | deixar fora l'aigua |
| `--no-towns` | desactivada | deixar fora les petjades dels pobles |
| `--skip-existing` | desactivada | deixar els mapes que ja tenen el seu `.glb` |

Totes les opcions, tal com les imprimeix el programa: [Referència de l'ordre](../cli-reference.md).

Defineix `HEAT3D_DEBUG` per imprimir el rastreig complet d'un mapa que ha fallat. El `.glb` s'escriu a
`<mapa>.glb.part` i es reanomena quan està acabat.

Estat de sortida: 0 cada mapa escrit; 1 algun ha fallat (els altres s'escriuen igualment);
2 cap instal·lació o cap mapa coincident.

## Exemples {#examples}

```bash
heat3d-il2-level extract <mapa> -o levels                         # un mapa, marc enu al voltant del seu centre
heat3d-il2-level extract <mapa> --origin <lat> <lon> -o levels    # en el mapa pla d'una gravació amb aquest geo
heat3d-il2-level extract "<família>_*" --max-grid 2048 -o levels  # més fi, diversos mapes
heat3d-il2-level extract --all --skip-existing -o levels         # cada mapa, només els nous
heat3d-il2-level extract <mapa> --frame game -o levels            # els metres propis del joc, tal com els tenen els fitxers de missió
```

Què hi ha als fitxers: [Els fitxers del nivell i els marcs](output.md).
