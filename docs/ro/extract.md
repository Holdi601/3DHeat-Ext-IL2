---
title: "Construirea nivelurilor: extract"
nav_order: 3
lang: ro
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Construirea nivelurilor: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Pas cu pas {#step-by-step}

Nu ați mai lucrat în linia de comandă? Citiți mai întâi [Înainte de a începe](before-you-start.md).

1. Aflați numele hărții cu [`list`](list.md).
2. Rulați `heat3d-il2-level extract <map> -o levels`. Numele pot folosi metacaractere, între ghilimele
   (`"<family>_*"`); `--all` ia fiecare hartă.
3. Ca să puneți o înregistrare pe nivel fără pas de plasare, dați originea acesteia: `--origin <lat> <lon>`
   cu valoarea `geo` a înregistrării (punctul de referință al sesiunii sale). Fără ea, centrul hărții
   devine originea, iar `geo` din `.json` spune care este.
4. Comanda afișează câte o linie pentru fiecare hartă pe măsură ce o decodează, apoi
   `ok <glb> <triangles> (<frame> frame)` sau `failed <map>: <why>`.
5. Încărcați `<folder>/<map>/<map>.glb` în panoul Fundal / nivel al vizualizatorului.

![extract pe o instalare sintetică](../assets/img/extract.svg)

În metrii proprii ai jocului, fără apă:

![extract --frame game --no-water](../assets/img/extract-game.svg)

O a doua rulare peste hărțile deja scrise:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opțiuni {#options}

| Opțiune | Implicit | Ce face |
|---|---|---|
| `maps` | - | numele hărților, cum le afișează `list`; metacaractere permise |
| `--all` | dezactivată | fiecare hartă; sezoanele care au aceeași hartă de înălțimi și aceeași hartă de apă se scriu o singură dată |
| `-o`, `--out` | obligatorie | dosarul de ieșire; fiecare hartă intră în `<out>/<map>/` |
| `--game FOLDER` | găsit | un dosar IL-2 (care se poate repeta) |
| `--max-grid N` | `1024` | cel mult atâția eșantioane de hartă de înălțimi pe o latură (1024: circa 2 milioane de triunghiuri); harta este eșantionată din *k* în *k* eșantioane ca să încapă |
| `--frame` `enu` sau `game` | `enu` | `enu`: metri est, altitudine, nord față de `--origin`, ca tabelele Tacview ale Watcher; `game`: metrii proprii ai jocului (x nord, y înălțime, z est). O hartă care nu poate fi plasată pe pământ se scrie în `game`, orice s-ar cere |
| `--origin LAT LON` | centrul hărții | originea sistemului `enu` (`geo` al unei înregistrări) |
| `--no-water` | dezactivată | lasă apa afară |
| `--no-towns` | dezactivată | lasă afară amprentele orașelor |
| `--skip-existing` | dezactivată | lasă hărțile al căror `.glb` există deja |

Fiecare opțiune, așa cum o afișează programul: [Referința comenzilor](../cli-reference.md).

Setați `HEAT3D_DEBUG` ca să se afișeze traseul complet al unei hărți care a eșuat. Fișierul `.glb`
se scrie în `<map>.glb.part` și se redenumește când este gata.

Codul de stare: 0 fiecare hartă scrisă; 1 vreuna a eșuat (celelalte se scriu oricum); 2 nu s-a găsit
nicio instalare sau nicio hartă nu a corespuns.

## Exemple {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Ce este în fișiere: [Fișierele nivelului și sistemele de coordonate](output.md).
