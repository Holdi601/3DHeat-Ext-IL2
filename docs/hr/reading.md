---
title: Kako se datoteke čitaju
nav_order: 5
lang: "hr"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Kako se datoteke čitaju {#how-the-files-are-read}

| Dio | Status |
|---|---|
| Arhivi (`data/*.gtp`, Great Battles) | tablica datoteka (zapisi `S16R`, `STRMFAT?`, `DIR!`/`FILE`) i unosi (zaglavlje `STRMFILE`, podaci spremljeni kakvi jesu); svaki `Maps*.gtp` testne instalacije |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, granice igre i `MapNW/NE/SE/SW`; svaki od testne instalacije |
| Visinske mape (`height.dat`) | kodek u nastavku; svaki sektor karata dekodiran u cijelosti dok se radilo na njemu koristi svoj bitni niz točno (najviše zaostali bajtni padding), ostalo provjereno po zaglavlju. Provjereno bit-po-bit naspram nekomprimiranih datoteka `distlod.raw` koje igra isporučuje uz `distlod.dat`, i naspram visinske mape daljinskog LOD-a jedne karte (korelacija 0,999) |
| Visine | metri = sirovo x heightMul / 256 - SeaLevel x heightMul. More jedne karte dekodira se točno u visinu koju navode komentari njezina hini-ja; rub druge u njezin `bounds_level` |
| Smještaj | bilinearno između četiri kuta hini-ja, redak 0 sjever, stupac 0 zapad. Provjereno na karti naspram poznatih gradova, obala i mora (visine gradova unutar oko 10 m od stvarnih, mora ispod razine mora). Kutovi su četverokut, a ne vlastita projekcija igre, pa očekujte stotine metara pogreške u sredini velike karte. Hini jedne obitelji karata nosi kutove druge karte (raspon im je djelić njezine stvarne veličine); to se otkriva, pa se ta obitelj umjesto toga smješta prilagodbom prema orijentirima: gradovi i zračne luke iz vlastitih baza lokacija igre (`*.ldfbin`) naspram njihovih stvarnih položaja, srednje kvadratno odstupanje od nekoliko kilometara (gradovi naspram zračnih luka nazvanih po njima, a koordinate stvarnih mjesta do oko kilometra); JSON navodi svaki orijentir i njegovo odstupanje |
| Maska vode (`water.wtr`: četiri piramidalne razine pločica, svaka pločica je tablica blokova od 400 m, svaki blok je kopno, puni ili djelomično vodeni s oblikom u bitnom nizu) | spremnik se čita na svakoj karti (nijedan bajt ne ostaje na datotekama dekodiranim u cijelosti); oblik unutar djelomično vodenog bloka **nije dekodiran**. Puni blokovi su voda; u djelomično vodenim blokovima uzorak je voda tamo gdje je karta vode (`height_w.dat`, isti kodek kao visinska mapa) iznad tla ili, uz jezero, gdje tlo nije više od razine jezera; blokovi kopna su suhi. Time se uklanja močvara koju sama karta vode prijavljuje kao vodu. Rijeke uže od izlazne mreže ispadaju razbijene na komade |
| Tlocrti gradova (mreže dekala koje `textures.tini` navodi: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: pločice od 25,6 km ravnih teksturiranih trokuta) | čita se na svakoj karti; zadržavaju se plohe čija je tekstura grad, selo ili industrijsko tlo. Provjereno naspram stvarnih gradova na nekoliko karata (grad na obje obale rijeke, ušće). To su tlocrti: igra zgrade postavlja u vremenu izvođenja, a datoteke ne sadrže zgrade |
| Zračne luke, mostovi, zgrade | **ne čita se**: zračne luke su objekti misija, zgrade dolaze iz igrinog vlastitog postavljanja |
| Šume (`forest_map.wtr`) | njezini blokovi čitaju se na isti način, ali gotovo svaki blok je "djelomično šuma", pa bez bitnog niza nema upotrebljive maske šuma; ne crta se |
| Teksture tla | ne čitaju se |

## Kodek visinske mape {#the-heightmap-codec}

Izveden isključivo iz podatkovnih datoteka; nije pročitan ni rastavljen kod igre.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            od početka datoteke, po redcima, prvi gornji red
sector: u16 count (bajtovi koji slijede), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        zatim bitni niz čitan od najvišeg bita:
  PRE   2 * (log2(sectorSize) - 5) bitova, do sada uvijek 0
  LIT   prvi uzorak: predznak (1), n (LW bitova), iznos (n + 1 bitova)
  zatim do punog sektora:
    0 LIT       sljedeći = prethodni + LIT
    1 RUN LIT   prethodni uzorak se ponavlja RUN puta (k: 3 bita, m: k + 1 bitova, RUN = m + 1),
                zatim (osim ako sektor nije pun) sljedeći = prethodni + LIT
  vrijednosti su 16-bitne: čitaju se modulo 65536
```

Djelomični sektori na desnom i donjem rubu popunjavaju se i obrezuju. Isti kodek vrijedi
za kartu vode i za visinsku mapu daljinskog LOD-a.

## Prilagodbe prema orijentirima {#landmark-fits}

Tamo gdje kutovi karte ne mogu poslužiti, `landmarks.py` prilagođava afino preslikavanje iz metara igre na Zemlju metodom najmanjih kvadrata: položaji u igri iz vlastitih datoteka korisnika (bloka `Airfield` u misijama, baze lokacija karijere), stvarni položaji iz tablica objavljenih koordinata mjesta u kodu. `georeference` u JSON-u nosi matricu, ishodište, svaki orijentir s njegovim odstupanjem i srednje kvadratno odstupanje.
