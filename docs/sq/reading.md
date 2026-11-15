---
title: "Si lexohen skedarët"
nav_order: 5
lang: "sq"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Si lexohen skedarët {#how-the-files-are-read}

| Pjesa | Gjendja |
|---|---|
| Arkivat (`data/*.gtp`, Great Battles) | tabela e skedarëve (`S16R`, `STRMFAT?`, regjistrimet `DIR!`/`FILE`) dhe hyrjet (koka `STRMFILE`, të dhënat të ruajtura siç janë); çdo `Maps*.gtp` i instalimit të provës |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, kufijtë e lojës dhe `MapNW/NE/SE/SW`; çdo një i instalimit të provës |
| Heightmap-et (`height.dat`) | kodeku më poshtë; çdo sektor i hartave të dekoduara plotësisht gjatë zbulimit të tij e përdor rrjedhën e biteve saktësisht (më së shumti mbetet plotësimi i bajteve), pjesa tjetër e kontrolluar sipas kokës. Kontrolluar bit për bit kundrejt skedarëve të pangjeshur `distlod.raw` që i jep loja pranë `distlod.dat` të tyre, dhe kundrejt heightmap-it të largët LOD të një harte (korrelacion 0.999) |
| Lartësitë | metra = raw x heightMul / 256 - SeaLevel x heightMul. Deti i një harte dekodohet saktësisht në lartësinë që japin komentet e hini-t të saj; kufiri i një tjetre në `bounds_level` të saj |
| Vendosja | bilineare mes katër qosheve të hini-t, rreshti 0 veri, kolona 0 perëndim. Kontrolluar në një hartë kundrejt qyteteve, brigjeve dhe deteve të njohura (lartësitë e qyteteve brenda rreth 10 m nga të vërtetat, deti nën nivelin e detit). Qoshet janë një katërkëndësh, jo projeksioni i vetë lojës, pra prit disa qindra metra gabim në mes të një harte të madhe. Hini i një familjeje hartash mban qoshet e një harte tjetër (ato përfshijnë një pjesë të madhësisë së saj të vërtetë); kjo zbulohet, dhe ajo familje vendoset në vend me një përshtatje pikash referimi: qytetet dhe aeroportet e bazave të të dhënave të vendndodhjes të vetë lojës (`*.ldfbin`) kundrejt pozicioneve të tyre të vërteta, rms prej disa kilometrash (qytetet kundrejt aeroporteve të emërtuara sipas tyre, dhe koordinata të vendeve të vërteta me saktësi rreth një kilometri); JSON liston çdo pikë referimi dhe mbetjen e saj |
| Maska e ujit (`water.wtr`: katër nivele piramide pllakash, çdo pllakë një tabelë blloqesh 400 m, çdo bllok tokë, plot ose pjesërisht ujë me formën e tij në një rrjedhë bitesh) | kontejneri lexohet në çdo hartë (asnjë bajt i mbetur te skedarët e dekoduar plotësisht); forma brenda një blloku pjesërisht me ujë **nuk dekodohet**. Blloqet plot janë ujë; në blloqet pjesërisht me ujë një mostër është ujë aty ku harta e ujit (`height_w.dat`, i njëjti kodek si heightmap) është mbi tokën, ose, pranë një liqeni, aty ku toka nuk është më e lartë se liqeni; blloqet e tokës janë të thata. Kjo heq kënetën që harta e ujit vetëm e raporton si ujë. Lumenjtë më të ngushtë se rrjeta e daljes dalin të thyer në copa |
| Gjurmët e qyteteve (rrjetat decal që i liston `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: pllaka 25.6 km me trekëndësha të sheshtë të teksturuar) | lexohen në çdo hartë; faqet tekstura e të cilave është qytet, fshat ose tokë industriale mbahen. Kontrolluar kundrejt qyteteve të vërteta në disa harta (një qytet në të dy brigjet e një lumi, një bashkim lumenjsh). Janë gjurmë: loja i vendos ndërtesat gjatë ekzekutimit, dhe skedarët nuk mbajnë ndërtesa |
| Aeroportet, urat, ndërtesat | **nuk lexohen**: aeroportet janë objekte misioni, ndërtesat vijnë nga vendosja e vetë lojës |
| Pyjet (`forest_map.wtr`) | blloqet e tij lexohen njësoj, por pothuaj çdo bllok është "pjesërisht pyll", kështu që pa rrjedhën e biteve nuk ka maskë pylli të përdorshme; nuk vizatohet |
| Teksturat e tokës | nuk lexohen |

## Kodeku i heightmap {#the-heightmap-codec}

Nxjerrë nga skedarët e të dhënave vetëm; asnjë kod loje nuk u lexua ose çmontua.
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

Sektorët e pjesshëm në skajet e djathtë dhe të poshtëm plotësohen dhe priten. I njëjti
kodek mban hartën e ujit dhe heightmap-in e largët LOD.

## Përshtatjet me pika referimi {#landmark-fits}

Aty ku qoshet e një harte nuk mund të përdoren, `landmarks.py` përshtat një hartë afine nga
metrat e lojës në tokë me katrorët më të vegjël: pozicionet e lojës nga skedarët e vetë
përdoruesit (blloqet `Airfield` të misioneve, bazat e të dhënave të vendndodhjeve të karrierës), pozicionet e vërteta
nga tabela të koordinatave të botuara të vendeve në kod. `georeference` i JSON mban
matricën, origjinën, çdo pikë referimi me mbetjen e saj
dhe rms.
