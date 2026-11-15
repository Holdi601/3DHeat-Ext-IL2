---
title: "Levels bouwen: extract"
nav_order: 3
lang: "nl"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Levels bouwen: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Stap voor stap {#step-by-step}

Nog nooit met de opdrachtregel gewerkt? Lees eerst [Voordat je begint](before-you-start.md).

1. Zoek de naam van de kaart op met [`list`](list.md).
2. Voer `heat3d-il2-level extract <map> -o levels` uit. Namen mogen jokertekens gebruiken,
   tussen aanhalingstekens (`"<family>_*"`); `--all` neemt elke kaart.
3. Om een opname op het level te zetten zonder plaatsingsstap, geef de oorsprong op:
   `--origin <lat> <lon>` ingesteld op de `geo` van de opname (het referentiepunt van zijn sessie).
   Zonder dit is het midden van de kaart de oorsprong, en de `geo` in de `.json` zegt welke.
4. De opdracht drukt per kaart een regel af terwijl hij die decodeert, daarna
   `ok <glb> <triangles> (<frame> frame)` of `failed <map>: <why>`.
5. Laad `<folder>/<map>/<map>.glb` in het paneel Achtergrond / level van de viewer.

![extract op een synthetische installatie](../assets/img/extract.svg)

In de eigen meters van het spel, zonder het water:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Een tweede run over kaarten die al geschreven zijn:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opties {#options}

| Optie | Standaard | Doet |
|---|---|---|
| `maps` | - | kaartnamen zoals `list` ze afdrukt; jokertekens toegestaan |
| `--all` | uit | elke kaart; seizoenen die een hoogtekaart en watermap delen, worden één keer geschreven |
| `-o`, `--out` | verplicht | de uitvoermap; elke kaart gaat in `<out>/<map>/` |
| `--game FOLDER` | gevonden | een IL-2-map (herhaalbaar) |
| `--max-grid N` | `1024` | maximaal aantal hoogtekaartmonsters per zijde (1024: ongeveer 2 miljoen driehoeken); de kaart wordt elke *k* monsters bemonsterd om te passen |
| `--frame` `enu` of `game` | `enu` | `enu`: meters oostwaarts, hoogte, noordwaarts vanaf `--origin`, zoals de Tacview-tabellen van de Watcher; `game`: de eigen meters van het spel (x noord, y omhoog, z oost). Een kaart die niet op de aarde geplaatst kan worden, wordt altijd in `game` geschreven, wat er ook gevraagd wordt |
| `--origin LAT LON` | het midden van de kaart | de oorsprong van het `enu`-frame (de `geo` van een opname) |
| `--no-water` | uit | laat het water weg |
| `--no-towns` | uit | laat de voetafdrukken van steden weg |
| `--skip-existing` | uit | laat kaarten over waarvan de `.glb` al bestaat |

Elke optie, zoals het programma ze afdrukt: [Commandoreferentie](../cli-reference.md).

Zet `HEAT3D_DEBUG` aan om de volledige traceback van een mislukte kaart af te drukken. De `.glb` wordt
geschreven naar `<map>.glb.part` en hernoemd wanneer hij klaar is.

Exitstatus: 0 elke kaart geschreven, 1 één of meer mislukt (de andere worden wel
geschreven), 2 geen installatie of geen kaart gevonden.

## Voorbeelden {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # één kaart, enu-frame rond het midden
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in de vlakke kaart van een opname met die geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # fijner, meerdere kaarten
heat3d-il2-level extract --all --skip-existing -o levels         # elke kaart, alleen de nieuwe
heat3d-il2-level extract <map> --frame game -o levels            # de eigen meters van het spel, zoals missiebestanden ze hebben
```

Wat er in de bestanden zit: [De levelbestanden en frames](output.md).
