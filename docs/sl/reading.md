---
title: "Kako se datoteke berejo"
nav_order: 5
lang: "sl"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Kako se datoteke berejo {#how-the-files-are-read}

| Del | Stanje |
|---|---|
| Arhivi (`data/*.gtp`, Great Battles) | tabela datotek (zapisi `S16R`, `STRMFAT?`, `DIR!`/`FILE`) in vnosi (glava `STRMFILE`, podatki shranjeni kot so); vsaka `Maps*.gtp` preizkusne namestitve |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, meje igranja in `MapNW/NE/SE/SW`; vsaka datoteka preizkusne namestitve |
| Višinske karte (`height.dat`) | kodek spodaj; vsak odsek zemljevidov, dekodiran v celoti med delom na njem, uporablja svoj tok bitov natančno (največ preostanek bajtnega polnjenja), ostalo preverjeno po glavi. Bit-natančno preverjeno proti nestisnjenim datotekam `distlod.raw`, ki jih igra dostavi poleg njihovih `distlod.dat`, in proti višinski karti oddaljenega nivoja podrobnosti zemljevida (korelacija 0,999) |
| Višine | metri = surovi x heightMul / 256 - SeaLevel x heightMul. Morje zemljevida se dekodira točno v višino, ki jo navajajo komentarji njegovega hini; meja drugega v njegov `bounds_level` |
| Postavitev | bilinearno med štirimi vogali hini, vrstica 0 sever, stolpec 0 zahod. Preverjeno na zemljevidu proti znanim mestom, obalam in morjem (višine mest v okviru približno 10 m od pravih, morja pod morsko gladino). Vogali so štirikotnik, ne projekcija igre, zato pričakuj nekaj sto metrov napake v sredini velikega zemljevida. Hini ene družine zemljevidov nosi vogale drugega zemljevida (razpenjajo delček njegove prave velikosti); to se zazna, zato se ta družina postavi z prilagajanjem z orientiri: mesta in letališča iz lastnih baz lokacij igre (`*.ldfbin`) proti njihovim pravim položajem, koren povprečne kvadratne napake nekaj kilometrov (mesta proti letališčem, po njih imenovanim, in koordinate pravih krajev na približno kilometer). JSON navaja vsak orientir in njegovo odstopanje |
| Maska vode (`water.wtr`: štiri piramidne ravni ploščic, vsaka ploščica je tabela blokov po 400 m, vsak blok je kopno, polno ali delno voda z obliko v toku bitov) | vsebnik se prebere na vsakem zemljevidu (brez zaostalega bajta na datotekah, dekodiranih v celoti); oblika znotraj delno vodnega bloka **ni dekodirana**. Polni bloki so voda; v delno vodnih blokih je vzorec voda, kjer je karta vode (`height_w.dat`, isti kodek kot višinska karta) nad tlemi, ali ob jezeru, kjer tla niso višja od jezera; kopenski bloki so suhi. Tako se odstrani močvirje, ki ga karta vode sama prijavi kot vodo. Reke, ožje od izhodne mreže, se pokažejo razlomljene na kose |
| Odtisi mest (mreže odtisov `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh` ...: ploščice po 25,6 km ravnih teksturiranih trikotnikov) | prebrani na vsakem zemljevidu; ohranjene so ploskve, katerih tekstura je mesto, vas ali industrijsko zemljišče. Preverjeno proti pravim mestom na nekaj zemljevidih (mesto na obeh bregovih reke, sotočje). So odtisi: igra stavbe postavi med tekom, datoteke pa stavb ne vsebujejo |
| Letališča, mostovi, stavbe | **niso prebrani**: letališča so predmeti misij, stavbe pridejo iz igrine lastne postavitve |
| Gozdovi (`forest_map.wtr`) | njegovi bloki se berejo enako, vendar je skoraj vsak blok »delno gozd«, zato brez toka bitov ni uporabne maske gozda; ni narisan |
| Teksture terena | niso prebrane |

## Kodek višinske karte {#the-heightmap-codec}

Ugotovljen samo iz podatkovnih datotek; nobena koda igre ni bila prebrana ali razstavljena.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            od začetka datoteke, po vrsticah, najprej zgornja vrstica
sector: u16 count (bajti, ki sledijo), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        nato tok bitov, prebran od MSB naprej:
  PRE   2 * (log2(sectorSize) - 5) bitov, zaenkrat vedno 0
  LIT   prvi vzorec: predznak (1), n (LW bitov), velikost (n + 1 bitov)
  nato, dokler odsek ni poln:
    0 LIT       naslednji = prejšnji + LIT
    1 RUN LIT   prejšnji vzorec se ponovi RUN-krat (k: 3 biti, m: k + 1 bitov, RUN = m + 1),
                nato (razen če je odsek poln) naslednji = prejšnji + LIT
  vrednosti so 16-bitne: beremo jih po modulu 65536
```

Delni odseki na desnem in spodnjem robu so zapolnjeni in obrezani. Isti kodek velja za karto vode in višinsko
karto oddaljenega nivoja podrobnosti.

## Prilagajanje z orientiri {#landmark-fits}

Kjer vogalov zemljevida ni mogoče uporabiti, `landmarks.py` prilagodi afino preslikavo iz igrinih metrov na
Zemljo po metodi najmanjših kvadratov: igrine položaje iz lastnih datotek uporabnika (bloki `Airfield` v
datotekah misij, baze lokacij kariere), prave položaje pa iz tabel objavljenih koordinat krajev v kodi. JSON
v `georeference` hrani matriko, izhodišče, vsak orientir z njegovim odstopanjem in koren povprečne kvadratne
napake.
