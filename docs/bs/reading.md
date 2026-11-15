---
title: "Kako se datoteke čitaju"
nav_order: 5
lang: bs
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Kako se datoteke čitaju {#how-the-files-are-read}

| Dio | Stanje |
|---|---|
| Arhive (`data/*.gtp`, Great Battles) | tabela datoteka (`S16R`, `STRMFAT?`, zapisi `DIR!`/`FILE`) i unosi (zaglavlje `STRMFILE`, podaci pohranjeni kakvi jesu); svaki `Maps*.gtp` testne instalacije |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, granice igre i `MapNW/NE/SE/SW`; svaki iz testne instalacije |
| Visinske mape (`height.dat`) | kodek ispod; svaki sektor mapa dekodiranih u cijelosti pri otkrivanju koristi svoj tok bitova tačno (najviše ostaje dopuna bajtova), ostalo provjereno po zaglavlju. Provjereno bit po bit prema nekomprimiranim datotekama `distlod.raw` koje igra isporučuje pored njihovog `distlod.dat`, i prema vlastitoj visinskoj mapi udaljenog LOD-a neke mape (korelacija 0,999) |
| Visine | metri = raw x heightMul / 256 - SeaLevel x heightMul. More jedne mape dekodira se tačno na visinu koju daju komentari njenog hini; granica druge na njen `bounds_level` |
| Postavljanje | bilinearno između četiri ugla iz hini, red 0 sjever, kolona 0 zapad. Provjereno na jednoj mapi prema poznatim gradovima, obalama i morima (visine gradova unutar oko 10 m od stvarnih, mora ispod nivoa mora). Uglovi su četverougao, a ne vlastita projekcija igre, pa očekuj nekoliko stotina metara greške u sredini velike mape. Hini jedne porodice mapa nosi uglove druge mape (obuhvataju djelić njene stvarne veličine); ovo se otkriva, a ta porodica se umjesto toga postavlja prilagođavanjem orijentira: gradovi i aerodromi iz vlastitih baza lokacija igre (`*.ldfbin`) prema njihovim stvarnim pozicijama, rms par kilometara (gradovi prema aerodromima nazvanim po njima, a koordinate stvarnih mjesta do oko kilometra); JSON navodi svaki orijentir i njegovo odstupanje |
| Maska vode (`water.wtr`: četiri nivoa piramide pločica, svaka pločica tabela blokova od 400 m, svaki blok kopno, pun ili djelomično voda s oblikom u toku bitova) | spremnik se čita na svakoj mapi (nijedan bajt ne preostaje na datotekama dekodiranim u cijelosti); oblik unutar djelomično vodenog bloka **nije dekodiran**. Puni blokovi su voda; u djelomično vodenim blokovima uzorak je voda gdje je vodena mapa (`height_w.dat`, isti kodek kao visinska mapa) iznad tla, ili, pored jezera, gdje tlo nije više od jezera; blokovi kopna su suhi. Time nestaje močvara koju sama vodena mapa prijavljuje kao vodu. Rijeke uže od izlazne mreže izlaze razbijene na komade |
| Tragovi gradova (decal mreže koje navodi `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: pločice od 25,6 km ravnih teksturiranih trouglova) | čita se na svakoj mapi; zadržavaju se lica čija je tekstura grad, selo ili industrijsko tlo. Provjereno prema stvarnim gradovima na nekoliko mapa (grad na obje obale rijeke, ušće). To su tragovi (footprints): igra postavlja zgrade u toku rada, a datoteke ne sadrže zgrade |
| Aerodromi, mostovi, zgrade | **ne čitaju se**: aerodromi su objekti misije, zgrade dolaze iz vlastitog postavljanja igre |
| Šume (`forest_map.wtr`) | njeni blokovi čitaju se na isti način, ali je gotovo svaki blok "djelomično šuma", pa bez toka bitova nema upotrebljive maske šume; ne crta se |
| Teksture tla | ne čitaju se |

## Kodek visinske mape {#the-heightmap-codec}

Utvrđen samo iz datoteka podataka; nikakav kod igre nije čitan ni rastavljan.
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

Djelomični sektori na desnoj i donjoj ivici se dopunjuju i obrezuju. Isti
kodek vrijedi za vodenu mapu i visinsku mapu udaljenog LOD-a.

## Prilagođavanje orijentirima {#landmark-fits}

Gdje se uglovi mape ne mogu koristiti, `landmarks.py` prilagođava afino preslikavanje iz
metara igre na Zemlju metodom najmanjih kvadrata: pozicije u igri iz korisnikovih vlastitih
datoteka (blokovi `Airfield` misija, baze lokacija karijere), stvarne pozicije
iz tablica objavljenih koordinata mjesta u kodu. `georeference` u JSON-u
nosi matricu, ishodište, svaki orijentir s njegovim odstupanjem
i rms.
