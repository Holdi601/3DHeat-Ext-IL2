---
title: "Bygga nivåer: extract"
nav_order: 3
lang: sv
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Bygga nivåer: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Steg för steg {#step-by-step}

Har du aldrig använt kommandoraden förut? Läs [Innan du börjar](before-you-start.md) först.

1. Hitta kartans namn med [`list`](list.md).
2. Kör `heat3d-il2-level extract <map> -o levels`. Namnen får använda jokertecken, inom citattecken (`"<family>_*"`); `--all` tar varje karta.
3. För att lägga en inspelning på nivån utan något placeringssteg, ange dess ursprung:
   `--origin <lat> <lon>` satt till inspelningens `geo` (dess sessions referenspunkt). Utan den är kartans mitt ursprunget, och `.json`:ens `geo` säger vilket.
4. Kommandot skriver en rad per karta när det avkodar den, sedan
   `ok <glb> <triangles> (<frame> frame)` eller `failed <map>: <why>`.
5. Läs in `<folder>/<map>/<map>.glb` i visarens nivåpanel.

![extract på en syntetisk installation](../assets/img/extract.svg)

I spelets egna meter, utan vattnet:

![extract --frame game --no-water](../assets/img/extract-game.svg)

En andra körning över kartor som redan skrivits:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Alternativ {#options}

| Alternativ | Standard | Gör |
|---|---|---|
| `maps` | - | kartnamn så som `list` skriver ut dem; jokertecken tillåtna |
| `--all` | av | varje karta; säsonger som delar en höjdkarta och vattenkarta skrivs en gång |
| `-o`, `--out` | krävs | utmappen; varje karta hamnar i `<out>/<map>/` |
| `--game FOLDER` | hittas | en IL-2-mapp (kan upprepas) |
| `--max-grid N` | `1024` | högst så många höjdprov per sida (1024: ungefär 2 miljoner trianglar); kartan provtas var *k*:e prov för att passa |
| `--frame` `enu` eller `game` | `enu` | `enu`: meter öster, höjd över havet, norr om `--origin`, som Watcher:s Tacview-tabeller; `game`: spelets egna meter (x norrut, y uppåt, z österut). En karta som inte kan placeras på jorden skrivs i `game` oavsett vad som begärs |
| `--origin LAT LON` | kartans mitt | ursprunget för `enu`-ramen (en inspelnings `geo`) |
| `--no-water` | av | lämna bort vattnet |
| `--no-towns` | av | lämna bort stadsavtrycken |
| `--skip-existing` | av | lämna kartor vars `.glb` redan finns |

Alla alternativ, så som programmet skriver ut dem: [Kommandoreferens](../cli-reference.md).

Sätt `HEAT3D_DEBUG` för att skriva ut hela spårningen för en karta som misslyckades. `.glb`-filen skrivs till `<map>.glb.part` och byter namn när den är klar.

Avslutskod: 0 varje karta skriven, 1 någon misslyckades (de andra skrivs ändå), 2 ingen installation eller ingen karta matchade.

## Exempel {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # en karta, enu-ram runt dess mitt
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # i den platta kartan för en inspelning med den geon
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finare, flera kartor
heat3d-il2-level extract --all --skip-existing -o levels         # varje karta, bara de nya
heat3d-il2-level extract <map> --frame game -o levels            # spelets egna meter, så som uppdragsfiler har dem
```

Vad som finns i filerna: [Nivåfilerna och ramarna](output.md).
