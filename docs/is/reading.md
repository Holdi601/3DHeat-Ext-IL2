---
title: "Hvernig skrárnar eru lesnar"
nav_order: 5
lang: "is"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Hvernig skrárnar eru lesnar {#how-the-files-are-read}

| Hluti | Staða |
|---|---|
| Skjalasöfn (`data/*.gtp`, Great Battles) | skráartaflan (`S16R`, `STRMFAT?`, `DIR!`/`FILE` færslur) og færslurnar (`STRMFILE` haus, gögn geymd óbreytt); sérhvert `Maps*.gtp` í prófunaruppsetningunni |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, leikmörkin og `MapNW/NE/SE/SW`; allt í prófunaruppsetningunni |
| Hæðarkort (`height.dat`) | málið hér að neðan; sérhver geiri kortanna sem afkóðuð voru í heild meðan unnið var að því notar bitastraum sinn nákvæmlega (í mesta lagi bætafyllingin eftir), restin athuguð eftir haus. Athugað bita fyrir bita gegn óþjöppuðu `distlod.raw` skránum sem leikurinn sendir með við hlið `distlod.dat`, og gegn eigin hæðarkorti korts fyrir fjarlæg smáatriðastig (fylgni 0,999) |
| Hæðir | metrar = hrátt x heightMul / 256 - SeaLevel x heightMul. Sjór korts afkóðast í nákvæmlega þá hæð sem athugasemdir hini þess gefa; brún annars í `bounds_level` þess |
| Staðsetning | tvílínuleg milli fjögurra horna hini, röð 0 norður, dálkur 0 vestur. Athugað á korti gegn þekktum bæjum, ströndum og sjó (hæðir bæja innan um 10 m frá raunverulegum, sjórinn undir sjávarmáli). Hornin eru ferhyrningur, ekki eigin vörpun leiksins, svo búast má við nokkur hundruð metra skekkju í miðju stórs korts. Hini einnar kortafjölskyldu ber horn annars korts (þau spanna brot af raunverulegri stærð þess); þetta er greint, og sú fjölskylda er þess í stað staðsett með kennileitafittun: bæir og flugvellir úr eigin staðsetningagagnagrunnum leiksins (`*.ldfbin`) gegn raunverulegum staðsetningum þeirra, rms upp á nokkra kílómetra (bæir gegn flugvöllum nefndum eftir þeim, og hnit raunverulegra staða upp á um kílómetra); JSON-skráin telur upp hvert kennileiti og afgangsskekkju þess |
| Vatnsgríma (`water.wtr`: fjögur pýramídastig flísa, hver flís tafla af 400 m blokkum, hver blokk land, full eða að hluta vatn með lögun sína í bitastraumi) | gámurinn er lesinn á hverju korti (ekkert bæti afgangs í skránum sem afkóðaðar voru í heild); lögunin inni í blokk sem er að hluta vatn er **ekki afkóðuð**. Fullar blokkir eru vatn; í blokkum að hluta vatn er sýni vatn þar sem vatnskortið (`height_w.dat`, sama mál og hæðarkortið) er yfir landinu, eða, við vatn, þar sem landið er ekki hærra en vatnið; landblokkir eru þurrar. Þetta fjarlægir mýrina sem vatnskortið eitt og sér tilkynnir sem vatn. Ár mjórri en úttaksnetið koma út brotnar í búta |
| Fótspor bæja (decal-netin sem `textures.tini` telur upp: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: 25,6 km flísar af flötum áferðarþríhyrningum) | lesin á hverju korti; fletirnir þar sem áferðin er bær, þorp eða iðnaðarland eru geymdir. Athugað gegn raunverulegum bæjum á nokkrum kortum (bær á báðum bökkum ár, ármót). Þetta eru fótspor: leikurinn setur byggingarnar á keyrslutíma, og skrárnar geyma engar byggingar |
| Flugvellir, brýr, byggingar | **ekki lesið**: flugvellir eru verkefnishlutir, byggingar koma úr eigin staðsetningu leiksins |
| Skógar (`forest_map.wtr`) | blokkir hennar lesnar eins, en nærri hver blokk er „að hluta skógur“, svo án bitastraumsins er enginn nothæfur skógargríma; ekki teiknað |
| Áferðir landsins | ekki lesið |

## Hæðarkortsmálið {#the-heightmap-codec}

Unnið út frá gagnaskránum einum; enginn leikjakóði var lesinn eða tekinn sundur.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            from the start of the file, row-major, top row first
sector: u16 count (bytes that follow), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        then a bitstream read MSB first:
  PRE   2 * (log2(sectorSize) - 5) bits, always 0 so far
  LIT   the first sample: sign (1), n (LW bits), magnitude (n + 1 bits)
  then until the sector is full:
    0 LIT       next = previous + LIT
    1 RUN LIT   the previous sample repeats RUN times (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                then (unless the sector is full) next = previous + LIT
  values are 16-bit: read them modulo 65536
```

Hlutageirar á hægri og neðri brúnum eru fylltir og skornir. Sama
mál geymir vatnskortið og hæðarkortið fyrir fjarlæg smáatriðastig.

## Kennileitafittun {#landmark-fits}

Þar sem ekki er hægt að nota horn korts fittar `landmarks.py` affín vörpun frá
metrum leiksins á jörðina með minnstu kvaðrötum: staðsetningar í leiknum úr eigin
skrám notandans (`Airfield` blokkir verkefna, staðsetningagagnagrunnar ferilsins), raunverulegar staðsetningar
úr töflum yfir birt hnit staðanna í kóðanum. `georeference` í JSON-skránni ber
fylkið, upphafspunktinn, hvert kennileiti með afgangsskekkju sinni
og rms.
