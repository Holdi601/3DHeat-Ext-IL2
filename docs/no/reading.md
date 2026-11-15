---
title: Slik leses filene
nav_order: 5
lang: no
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Slik leses filene {#how-the-files-are-read}

| Del | Status |
|---|---|
| Arkiver (`data/*.gtp`, Great Battles) | filtabellen (`S16R`, `STRMFAT?`, `DIR!`/`FILE`-poster) og oppføringene (`STRMFILE`-hode, data lagret som de er); hver `Maps*.gtp` i testinstallasjonen |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, spillgrensene og `MapNW/NE/SE/SW`; hver én i testinstallasjonen |
| Høydekart (`height.dat`) | kodeken under; hver sektor i kartene ble dekodet fullt ut mens den ble arbeidet ut, og bitstrømmen bruker den nøyaktig (på det meste overskytende fyllbyte), resten kontrollert etter hode. Kontrollert bit for bit mot de ukomprimerte `distlod.raw`-filene spillet sender ved siden av `distlod.dat`, og mot et karts eget fjern-LOD-høydekart (korrelasjon 0,999) |
| Høyder | meter = rå x heightMul / 256 - SeaLevel x heightMul. Et karts hav dekodes til nøyaktig høyden hini-kommentarene gir; et annets kant til dens `bounds_level` |
| Plassering | bilineær mellom hini-ens fire hjørner, rad 0 nord, kolonne 0 vest. Kontrollert på et kart mot kjente byer, kyster og hav (byhøyder innen omtrent 10 m fra de virkelige, havene under havnivå). Hjørnene er en firkant, ikke spillets egen projeksjon, så forvent noen hundre meters feil midt på et stort kart. Ett kartfamiliens hini bærer hjørnene til et annet kart (de spenner over en brøkdel av dets virkelige størrelse); dette oppdages, og den familien plasseres i stedet ved en landemerketilpasning: byer og flyplasser fra spillets egne stedsdatabaser (`*.ldfbin`) mot deres virkelige posisjoner, rot-middelkvadrat på et par kilometer (byer mot flyplassene oppkalt etter dem, og koordinatene til de virkelige stedene til omtrent en kilometer); JSON-filen lister hvert landemerke og dets avvik |
| Vannmaske (`water.wtr`: fire pyramidenivåer av fliser, hver flis en tabell med 400 m blokker, hver blokk land, full eller delvis vann med formen i en bitstrøm) | beholderen leses på hvert kart (ingen byte igjen på filene dekodet fullt ut); formen inne i en delvis vannblokk er **ikke dekodet**. Fulle blokker er vann; i delvis vanndekkede blokker er en prøve vann der vannkartet (`height_w.dat`, samme kodek som høydekartet) er over bakken, eller, ved siden av en innsjø, der bakken ikke er høyere enn innsjøen; landblokker er tørre. Det fjerner myren som vannkartet alene rapporterer som vann. Elver smalere enn utrutenettet blir brutt i biter |
| Byfotavtrykk (dekalmeshene `textures.tini` lister: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: 25,6 km flis med flate teksturerte trekanter) | leses på hvert kart; flatene der teksturen er en by, landsby eller industriell bakke beholdes. Kontrollert mot de virkelige byene på noen få kart (en by på begge bredder av en elv, et sammenløp). De er fotavtrykk: spillet plasserer bygningene under kjøring, og filene holder ingen bygninger |
| Flyplasser, broer, bygninger | **ikke lest**: flyplasser er oppdragsobjekter, bygninger kommer fra spillets egen plassering |
| Skoger (`forest_map.wtr`) | blokkene leses på samme måte, men nesten hver blokk er «delvis skog», så uten bitstrømmen finnes det ingen brukbar skogmaske; ikke tegnet |
| Bakkens teksturer | ikke lest |

## Høydekartkodeken {#the-heightmap-codec}

Utarbeidet fra datafilene alene; ingen spillkode ble lest eller demontert.
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

Delvise sektorer langs høyre og nedre kant er fylt ut og beskåret. Den samme
kodeken gjelder vannkartet og fjern-LOD-høydekartet.

## Landemerketilpasninger {#landmark-fits}

Der et karts hjørner ikke kan brukes, tilpasser `landmarks.py` en affin
avbildning fra spillets meter til jorden ved minste kvadraters metode: spillposisjoner fra brukerens egne
filer (`Airfield`-blokker i oppdrag, karrieredatabasene for steder), virkelige posisjoner fra
tabeller over stedenes publiserte koordinater i koden. JSON-filens
`georeference` bærer matrisen, origo, hvert landemerke med sitt avvik og rot-middelkvadratet.
