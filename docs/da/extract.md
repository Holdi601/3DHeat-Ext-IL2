---
title: Byg baner: extract
nav_order: 3
lang: da
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Byg baner: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Trin for trin {#step-by-step}

Ny til kommandolinjen? Læs [Før du går i gang](before-you-start.md) først.

1. Find kortets navn med [`list`](list.md).
2. Kør `heat3d-il2-level extract <map> -o levels`. Navne må bruge jokertegn,
   i anførselstegn (`"<family>_*"`); `--all` tager hvert kort.
3. Hvis du vil lægge en optagelse på banen uden noget placeringstrin, angiver du dens udgangspunkt:
   `--origin <lat> <lon>` sat til optagelsens `geo` (dens sessions referencepunkt). Uden det er kortets
   midte udgangspunktet, og `.json`'ens `geo` siger, hvilket.
4. Kommandoen udskriver en linje pr. kort, mens den afkoder det, og derefter
   `ok <glb> <triangles> (<frame> frame)` eller `failed <map>: <why>`.
5. Indlæs `<folder>/<map>/<map>.glb` i viewerens Baggrund / bane-panel.

![extract på en syntetisk installation](../assets/img/extract.svg)

I spillets egne meter, uden vandet:

![extract --frame game --no-water](../assets/img/extract-game.svg)

En anden kørsel over kort, der allerede er skrevet:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Valgmuligheder {#options}

| Valgmulighed | Standard | Gør |
|---|---|---|
| `maps` | - | kortnavne, som `list` udskriver dem; jokertegn tilladt |
| `--all` | fra | hvert kort; årstider, der deler et højdekort og et vandkort, skrives én gang |
| `-o`, `--out` | påkrævet | output-mappen; hvert kort havner i `<out>/<map>/` |
| `--game FOLDER` | fundet | en IL-2-mappe (kan gentages) |
| `--max-grid N` | `1024` | højst så mange højdekortprøver pr. side (1024: cirka 2 millioner trekanter); kortet prøves for hver *k*. prøve for at passe |
| `--frame` `enu` eller `game` | `enu` | `enu`: meter øst, højde, nord for `--origin`, ligesom Watcherens Tacview-tabeller; `game`: spillets egne meter (x nord, y op, z øst). Et kort, der ikke kan placeres på jorden, skrives i `game`, uanset hvad der bedes om |
| `--origin LAT LON` | kortets midte | udgangspunktet for `enu`-rammen (en optagelses `geo`) |
| `--no-water` | fra | udelad vandet |
| `--no-towns` | fra | udelad byernes fodaftryk |
| `--skip-existing` | fra | spring kort over, hvis deres `.glb` allerede findes |

Hver valgmulighed, som programmet udskriver den: [Kommandoreference](../cli-reference.md).

Sæt `HEAT3D_DEBUG` for at udskrive hele fejlsporet for et mislykket kort. `.glb`-filen skrives til
`<map>.glb.part` og omdøbes, når den er færdig.

Exit-status: 0 hvert kort skrevet, 1 nogle mislykkedes (de andre skrives stadig),
2 ingen installation eller intet kort matchede.

## Eksempler {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Hvad der er i filerne: [Banefilerne og rammerne](output.md).
