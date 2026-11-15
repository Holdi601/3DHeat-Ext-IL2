---
title: "Kenttien rakentaminen: extract"
nav_order: 3
lang: "fi"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Kenttien rakentaminen: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Vaihe vaiheelta {#step-by-step}

Uusi komentorivin kanssa? Lue ensin [Ennen aloittamista](before-you-start.md).

1. Selvitä kartan nimi komennolla [`list`](list.md).
2. Suorita `heat3d-il2-level extract <map> -o levels`. Nimissä voi käyttää jokerimerkkejä
   lainausmerkeissä (`"<family>_*"`); `--all` ottaa jokaisen kartan.
3. Jotta tallenne saadaan kentälle ilman sijoittelua, anna sen origo: `--origin <lat> <lon>`,
   asetettuna tallenteen `geo`-arvoon (sen istunnon viitepisteeseen). Ilman sitä kartan keskikohta on
   origo, ja `.json`-tiedoston `geo` kertoo, mikä se on.
4. Komento tulostaa rivin kartaa kohden sen dekoodauksen aikana, sitten
   `ok <glb> <triangles> (<frame> frame)` tai `failed <map>: <why>`.
5. Lataa `<folder>/<map>/<map>.glb` katselimen Tausta / kenttä -paneeliin.

![extract synteettisessä asennuksessa](../assets/img/extract.svg)

Pelin omissa metreissä ilman vettä:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Toinen ajo jo kirjoitetuille kartoille:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Asetukset {#options}

| Asetus | Oletus | Tekee |
|---|---|---|
| `maps` | - | kartan nimet kuten `list` ne tulostaa; jokerimerkit sallittu |
| `--all` | pois | jokainen kartta; vuodenajat, jotka jakavat saman korkeuskartan ja vesikartan, kirjoitetaan kerran |
| `-o`, `--out` | pakollinen | tulostekansio; jokainen kartta menee kansioon `<out>/<map>/` |
| `--game FOLDER` | löytyy | IL-2-kansio (toistettavissa) |
| `--max-grid N` | `1024` | korkeuskartan näytteitä enintään sivulla (1024: noin 2 miljoonaa kolmiota); karttaa otetaan näytteitä joka *k*:nnnestä näytteestä, jotta se mahtuu |
| `--frame` `enu` tai `game` | `enu` | `enu`: metriä itään, korkeus ja pohjoinen `--origin`-pisteestä, kuten Watcherin Tacview-taulukot; `game`: pelin omat metrit (x pohjoiseen, y ylös, z itään). Kartta, jota ei voi sijoittaa maapallolle, kirjoitetaan `game`-kehykseen mitä tahansa pyydetäänkin |
| `--origin LAT LON` | kartan keskikohta | `enu`-kehyksen origo (tallenteen `geo`) |
| `--no-water` | pois | jätä vesi pois |
| `--no-towns` | pois | jätä kaupunkien pohjapiirrokset pois |
| `--skip-existing` | pois | jätä kartat, joiden `.glb` on jo olemassa |

Jokainen asetus sellaisena kuin ohjelma ne tulostaa: [Komentoviite](../cli-reference.md).

Aseta `HEAT3D_DEBUG`, jotta epäonnistuneen kartan koko jäljitys tulostuu. `.glb` kirjoitetaan
tiedostoon `<map>.glb.part` ja nimetään uudelleen, kun se on valmis.

Poistumistila: 0 jokainen kartta kirjoitettu; 1 jokin epäonnistui (muut kirjoitetaan silti);
2 asennusta tai karttaa ei löytynyt.

## Esimerkit {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # yksi kartta, enu-kehys keskikohdan ympärillä
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # tasaisessa kartassa tallenteelle, jonka geo on tuo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # hienompi, useita karttoja
heat3d-il2-level extract --all --skip-existing -o levels         # jokainen kartta, vain uudet
heat3d-il2-level extract <map> --frame game -o levels            # pelin omat metrit, kuten tehtäväntiedostoissa
```

Mitä tiedostoissa on: [Kenttätiedostot ja kehykset](output.md).
