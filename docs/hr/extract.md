---
title: "Izrada razina: extract"
nav_order: 3
lang: "hr"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Izrada razina: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Korak po korak {#step-by-step}

Ne znate ništa o naredbenom retku? Prvo pročitajte [Prije nego što počnete](before-you-start.md).

1. Pronađite ime karte pomoću [`list`](list.md).
2. Pokrenite `heat3d-il2-level extract <map> -o levels`. Imena smiju koristiti zamjenske znakove,
   u navodnicima (`"<family>_*"`); `--all` uzima svaku kartu.
3. Da snimku stavite na razinu bez koraka postavljanja, navedite njezino ishodište:
   `--origin <lat> <lon>` postavljeno na `geo` snimke (referentnu točku njezine sesije). Bez toga je središte karte ishodište, a `geo` u `.json` datoteci kaže koje.
4. Naredba ispisuje redak po karti dok je dekodira, zatim
   `ok <glb> <triangles> (<frame> frame)` ili `failed <map>: <why>`.
5. Učitajte `<folder>/<map>/<map>.glb` u panel Pozadina / razina preglednika.

![extract na sintetičkoj instalaciji](../assets/img/extract.svg)

U metrima same igre, bez vode:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Drugo pokretanje nad kartama koje su već zapisane:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opcije {#options}

| Opcija | Zadano | Što radi |
|---|---|---|
| `maps` | - | imena karata kako ih ispisuje `list`; zamjenski znakovi dopušteni |
| `--all` | isključeno | svaka karta; sezone koje dijele visinsku mapu i kartu vode zapisuju se jednom |
| `-o`, `--out` | obavezno | mapa za izlaz; svaka karta ide u `<out>/<map>/` |
| `--game FOLDER` | pronađeno | mapa IL-2 (može se ponoviti) |
| `--max-grid N` | `1024` | najviše uzoraka visinske mape po stranici (1024: oko 2 milijuna trokuta); karta se uzorkuje svaki *k* uzoraka da stane |
| `--frame` `enu` ili `game` | `enu` | `enu`: metri istočno, nadmorska visina, sjeverno od `--origin`, kao Tacview tablice programa Watcher; `game`: vlastiti metri igre (x sjever, y gore, z istok). Karta koja se ne može smjestiti na Zemlju zapisuje se u `game` bez obzira na to što je traženo |
| `--origin LAT LON` | središte karte | ishodište okvira `enu` (`geo` snimke) |
| `--no-water` | isključeno | izostavi vodu |
| `--no-towns` | isključeno | izostavi tlocrte gradova |
| `--skip-existing` | isključeno | preskoči karte čiji `.glb` već postoji |

Svaka opcija, onako kako je program ispisuje: [Referenca naredbi](../cli-reference.md).

Postavite `HEAT3D_DEBUG` da ispiše cijeli trag greške za neuspjelu kartu. `.glb` se piše u
`<map>.glb.part` i preimenuje kad je gotov.

Izlazni status: 0 sve karte zapisane, 1 neka nije uspjela (ostale se ipak zapišu),
2 nema instalacije ili nijedna karta ne odgovara.

## Primjeri {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # jedna karta, enu okvir oko njezina središta
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # u ravnoj karti snimke s tim geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finije, više karata
heat3d-il2-level extract --all --skip-existing -o levels         # svaka karta, samo nove
heat3d-il2-level extract <map> --frame game -o levels            # vlastiti metri igre, kako ih imaju datoteke misija
```

Što je u datotekama: [Datoteke razine i okviri](output.md).
