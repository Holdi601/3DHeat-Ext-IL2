---
title: "Bygge baner: extract"
nav_order: 3
lang: no
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Bygge baner: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Steg for steg {#step-by-step}

Ny til kommandolinjen? Les [Før du begynner](before-you-start.md) først.

1. Finn kartets navn med [`list`](list.md).
2. Kjør `heat3d-il2-level extract <map> -o levels`. Navn kan bruke jokertegn,
   i anførselstegn (`"<family>_*"`); `--all` tar hvert kart.
3. For å legge en opptak på banen uten plasseringssteg, oppgi dens origo:
   `--origin <lat> <lon>` satt til opptakets `geo` (øktens referansepunkt). Uten den er kartets
   senter origo, og `.json`-filens `geo` sier hvilket.
4. Kommandoen skriver en linje per kart mens den avkoder det, deretter
   `ok <glb> <triangles> (<frame> frame)` eller `failed <map>: <why>`.
5. Last inn `<folder>/<map>/<map>.glb` i visningsprogrammets Bane-panel.

![extract på en syntetisk installasjon](../assets/img/extract.svg)

I spillets egne meter, uten vannet:

![extract --frame game --no-water](../assets/img/extract-game.svg)

En andre kjøring over kart som allerede er skrevet:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Alternativer {#options}

| Alternativ | Standard | Gjør |
|---|---|---|
| `maps` | - | kartnavn slik `list` skriver dem; jokertegn tillatt |
| `--all` | av | hvert kart; sesonger som deler et høydekart og vannkart skrives én gang |
| `-o`, `--out` | påkrevd | utmappen; hvert kart havner i `<out>/<map>/` |
| `--game FOLDER` | funnet | en IL-2-mappe (kan gjentas) |
| `--max-grid N` | `1024` | høydekartprøver per side på det meste (1024: omtrent 2 millioner trekanter); kartet prøves hver *k*-te prøve for å passe |
| `--frame` `enu` eller `game` | `enu` | `enu`: meter øst, høyde, nord fra `--origin`, som Watcherens Tacview-tabeller; `game`: spillets egne meter (x nord, y opp, z øst). Et kart som ikke kan plasseres på jorden skrives i `game` uansett hva som er bedt om |
| `--origin LAT LON` | kartets senter | origo for `enu`-rammen (et opptaks `geo`) |
| `--no-water` | av | utelat vannet |
| `--no-towns` | av | utelat byenes fotavtrykk |
| `--skip-existing` | av | hopp over kart der `.glb` allerede finnes |

Alle alternativene, slik programmet skriver dem ut: [Kommandoreferanse](../cli-reference.md).

Sett `HEAT3D_DEBUG` for å skrive ut hele sporingen av et mislykket kart. `.glb`-filen skrives til
`<map>.glb.part` og gis nytt navn når den er ferdig.

Avslutningsstatus: 0 hvert kart skrevet, 1 noen mislyktes (de andre skrives likevel),
2 ingen installasjon eller intet kart passet.

## Eksempler {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Hva som er i filene: [Banefilene og rammene](output.md).
