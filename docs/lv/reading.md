---
title: Kā tiek nolasīti faili
nav_order: 5
lang: lv
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Kā tiek nolasīti faili {#how-the-files-are-read}

| Daļa | Stāvoklis |
|---|---|
| Arhīvi (`data/*.gtp`, Great Battles) | failu tabula (`S16R`, `STRMFAT?`, `DIR!`/`FILE` ieraksti) un ieraksti (`STRMFILE` galvene, dati saglabāti kā tādi); katrs `Maps*.gtp` no testa uzstādījuma |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, spēles robežas un `MapNW/NE/SE/SW`; katrs no testa uzstādījuma |
| Augstuma kartes (`height.dat`) | zemāk aprakstītais kodeks; katrs karšu sektors, kas tika pilnībā dekodēts, izstrādājot to, izmanto savu bitu straumi precīzi (ne vairāk kā atlikušais baitu izlīdzinājums), pārējie pārbaudīti pēc galvenes. Pārbaudīts bit pa bitam pret nesaspiestiem `distlod.raw` failiem, ko spēle piegādā blakus savam `distlod.dat`, un pret kartes pašas tālās LOD augstuma karti (korelācija 0,999) |
| Augstumi | metri = neapstrādāts x heightMul / 256 - SeaLevel x heightMul. Kartes jūra dekodējas tieši tajā augstumā, ko norāda tās hini komentāri; citas robeža - savā `bounds_level` |
| Novietojums | bilineārs starp hini četriem stūriem, 0. rinda ziemeļi, 0. kolonna rietumi. Pārbaudīts kartē pret zināmām pilsētām, krastiem un jūrām (pilsētu augstumi apmēram 10 m robežās no īstajiem, jūras zem jūras līmeņa). Stūri ir četrstūris, nevis spēles pašu projekcija, tāpēc gaidiet dažu simtu metru kļūdu lielas kartes vidū. Vienas kartes ģimenes hini nes citas kartes stūrus (tie aptver tikai daļu no tās īstā izmēra); to atklāj, un šī ģimene tiek novietota ar orientieru pieskaņojumu: spēles pašas atrašanās vietu datubāžu (`*.ldfbin`) pilsētas un lidlauki pret to īstajām pozīcijām, kvadrātiskā vidējā kļūda dažus kilometrus (pilsētas pret tām nosaukto lidlauku, un īsto vietu koordinātes līdz apmēram kilometram). JSON uzskaita katru orientieri un tā atlikumu |
| Ūdens maska (`water.wtr`: četri piramīdas līmeņi ar flīzēm, katra flīze ir 400 m bloku tabula, katrs bloks ir sauszeme, pilns vai daļēji ūdens ar savu formu bitu straumē) | konteineris tiek nolasīts katrā kartē (pilnībā dekodētajos failos nepaliek neviens baits); formu daļēji ūdens blokā **nedekodē**. Pilni bloki ir ūdens; daļēji ūdens blokos paraugs ir ūdens, kur ūdens karte (`height_w.dat`, tas pats kodeks kā augstuma kartei) ir augstāka par zemi, vai, blakus ezeram, kur zeme nav augstāka par ezeru; sauszemes bloki ir sausi. Tas noņem purvu, ko viena ūdens karte atzīmē kā ūdeni. Upes, kas ir šaurākas par izvades režģi, parādās saplēstas gabalos |
| Pilsētu laukumi (dekālu tīkli, ko uzskaita `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh` u.c.: 25,6 km flīzes ar plakaniem tekstūrētiem trijstūriem) | tiek nolasīti katrā kartē; tiek paturītas virsmas, kuru tekstūra ir pilsēta, ciems vai rūpnieciska zeme. Pārbaudīts pret īstajām pilsētām dažās kartēs (pilsēta abos upes krastos, sateka). Tie ir laukumi: spēle ēkas novieto darbības laikā, un failos ēku nav |
| Lidlauki, tilti, ēkas | **nav nolasīti**: lidlauki ir misiju objekti, ēkas nāk no spēles pašas novietojuma |
| Meži (`forest_map.wtr`) | to bloki tiek nolasīti tādā pašā veidā, bet gandrīz katrs bloks ir "daļēji mežs", tāpēc bez bitu straumes nav izmantojamas meža maskas; netiek zīmēts |
| Zemes tekstūras | nav nolasītas |

## Augstuma kartes kodeks {#the-heightmap-codec}

Izprasts tikai no datu failiem; netika lasīts vai izjaukts neviens spēles kods.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            no faila sākuma, pa rindām, augšējā rinda pirmā
sector: u16 count (baiti, kas seko), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        pēc tam bitu straume, lasīta no MSB uz priekšu:
  PRE   2 * (log2(sectorSize) - 5) biti, līdz šim vienmēr 0
  LIT   pirmais paraugs: zīme (1), n (LW biti), lielums (n + 1 biti)
  tad, līdz sektors ir pilns:
    0 LIT       next = previous + LIT
    1 RUN LIT   iepriekšējais paraugs atkārtojas RUN reizes (k: 3 biti, m: k + 1 biti, RUN = m + 1),
                tad (ja sektors nav pilns) next = previous + LIT
  vērtības ir 16 biti: lasiet pēc moduļa 65536
```

Daļējie sektori pie labās un apakšējās malas tiek papildināti un apgriezti. Tas pats kodeks attiecas uz ūdens karti un tālās LOD augstuma karti.

## Orientieru pieskaņojumi {#landmark-fits}

Kur kartes stūrus nevar izmantot, `landmarks.py` pieskaņo afīno pārveidi no spēles metriem uz zemi ar mazāko kvadrātu metodi: spēles pozīcijas no lietotāja pašu failiem (misiju `Airfield` bloki, karjeras atrašanās vietu datubāzes), īstās pozīcijas no tabulām ar vietu publicētām koordinātēm kodā. JSON `georeference` satur matricu, sākumpunktu, katru orientieri ar tā atlikumu un kvadrātisko vidējo kļūdu.
