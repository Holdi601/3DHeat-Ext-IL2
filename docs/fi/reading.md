---
title: "Miten tiedostot luetaan"
nav_order: 5
lang: "fi"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Miten tiedostot luetaan {#how-the-files-are-read}

| Osa | Tila |
|---|---|
| Arkistot (`data/*.gtp`, Great Battles) | tiedostotaulukko (`S16R`, `STRMFAT?`, `DIR!`/`FILE`-tietueet) ja merkinnät (`STRMFILE`-otsikko, data tallennettuna sellaisenaan); jokainen testiasennuksen `Maps*.gtp` |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, pelirajat ja `MapNW/NE/SE/SW`; jokainen testiasennuksen |
| Korkeuskartat (`height.dat`) | alla oleva koodekki; jokainen kartan sektori, joka dekoodattiin kokonaan koodekin selvittämisen aikana, käyttää bittivirtaansa tarkasti (enintään jäljelle jäävä tavutäyte), loput tarkistettu otsikon perusteella. Tarkistettu bitti bitiltä pakkaamattomia `distlod.raw`-tiedostoja vastaan, joita peli toimittaa `distlod.dat`-tiedostojensa vieressä, ja kartan oman kaukaisen LOD-korkeuskartan kanssa (korrelaatio 0,999) |
| Korkeudet | metriä = raaka x heightMul / 256 - SeaLevel x heightMul. Kartan meri dekoodautuu täsmälleen korkeudeksi, jonka sen hini-kommentit antavat; toisen kartan reuna sen `bounds_level`-arvoon |
| Sijoittelu | bilineaarinen hinin neljän kulman välillä, rivi 0 pohjoinen, sarake 0 länsi. Tarkistettu kartalla tunnettuja kaupunkeja, rannikoita ja merta vastaan (kaupunkien korkeudet noin 10 m:n tarkkuudella todellisista, meret merenpinnan alapuolella). Kulmat muodostavat nelikulmion, eivät pelin omaa projektiota, joten odota suuressa kartassa satojen metrien virhettä keskellä. Yhden karttaperheen hini kantaa toisen kartan kulmat (ne kattavat murto-osan sen todellisesta koosta); tämä havaitaan, ja se perhe sijoitetaan sen sijaan maamerkkisovituksella: pelin omien sijaintitietokantojen (`*.ldfbin`) kaupungit ja lentokentät vastaan niiden todellisilla sijainneilla, neliöllinen keskiarvo parin kilometrin tarkkuudella (kaupungit lentokenttiä vastaan, joita ne kantavat nimeä, ja todellisten paikkojen koordinaatit noin kilometrin tarkkuudella); JSON luettelee jokaisen maamerkin ja sen jäännöksen |
| Vesikartta (`water.wtr`: neljä pyramiditasoa laattoja, jokainen laatta taulukko 400 m:n lohkoista, jokainen lohko maa, täysin tai osittain vettä sen muodolla bittivirrassa) | säiliö luetaan jokaisella kartalla (kokonaan dekoodatuissa tiedostoissa ei jää yhtäkään tavua); osittain vetisen lohkon sisäistä muotoa **ei dekoodata**. Täydet lohkot ovat vettä; osittain vetisissä lohkoissa näyte on vettä, kun vesikartta (`height_w.dat`, sama koodekki kuin korkeuskartassa) on maanpinnan yläpuolella, tai järven vieressä, kun maa ei ole järveä korkeammalla; maalohkot ovat kuivia. Tämä poistaa suon, jonka pelkkä vesikartta ilmoittaa vedeksi. Ulostulon ruudukkoa kapeammat joet tulevat ulos rikkoutuneina paloina |
| Kaupunkien pohjapiirrokset (pinta-kuvioverkot, jotka `textures.tini` luettelee: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh` ym.: 25,6 km:n laattoja tasaisia teksturoituja kolmioita) | luetaan jokaisella kartalla; pidetään ne pinnat, joiden tekstuuri on kaupunki, kylä tai teollisuusmaa. Tarkistettu todellisia kaupunkeja vastaan muutamalla kartalla (kaupunki joen molemmilla rannoilla, yhtymäkohta). Ne ovat pohjapiirroksia: peli sijoittaa rakennukset ajon aikana, eikä tiedostoissa ole rakennuksia |
| Lentokentät, sillat, rakennukset | **ei luettu**: lentokentät ovat tehtäväobjekteja, rakennukset tulevat pelin omasta sijoittelusta |
| Metsät (`forest_map.wtr`) | sen lohkot luetaan samalla tavalla, mutta lähes jokainen lohko on "partly forest", joten ilman bittivirtaa ei ole käyttökelpoista metsämaskia; ei piirretä |
| Maaston tekstuurit | ei luettu |

## Korkeuskartan koodekki {#the-heightmap-codec}

Selvitetty pelkistä datatiedostoista; mitään pelikoodia ei luettu eikä purettu.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            tiedoston alusta, rivi kerrallaan, ylin rivi ensin
sector: u16 count (seuraavien tavujen määrä), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        sitten bittivirta, luettuna MSB ensin:
  PRE   2 * (log2(sectorSize) - 5) bittiä, tähän asti aina 0
  LIT   ensimmäinen näyte: merkki (1), n (LW bittiä), suuruus (n + 1 bittiä)
  sitten kunnes sektori on täynnä:
    0 LIT       seuraava = edellinen + LIT
    1 RUN LIT   edellinen näyte toistuu RUN kertaa (k: 3 bittiä, m: k + 1 bittiä, RUN = m + 1),
                sitten (ellei sektori ole täynnä) seuraava = edellinen + LIT
  arvot ovat 16-bittisiä: luetaan modulo 65536
```

Oikean ja alareunan osittaiset sektorit täytetään ja leikataan. Sama koodekki kantaa
vesikartan ja kaukaisen LOD-korkeuskartan.

## Maamerkkisovitukset {#landmark-fits}

Kun kartan kulmia ei voi käyttää, `landmarks.py` sovittaa affiinisen kuvauksen pelin metreistä
maapallolle pienimmän neliösumman menetelmällä: pelin sijainnit käyttäjän omista tiedostoista (tehtävien
`Airfield`-lohkot, uran sijaintitietokannat), todelliset sijainnit paikkojen julkaistuista koordinaateista,
jotka ovat taulukoina koodissa. JSON-tiedoston `georeference` kantaa matriisin, origon, jokaisen maamerkin
jäännöksineen ja neliöllisen keskiarvon.
