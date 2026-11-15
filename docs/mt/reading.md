---
title: Kif jinqraw il-fajls
nav_order: 5
lang: mt
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Kif jinqraw il-fajls {#how-the-files-are-read}

| Parti | Status |
|---|---|
| Arkivji (`data/*.gtp`, Great Battles) | it-tabella tal-fajls (records `S16R`, `STRMFAT?`, `DIR!`/`FILE`) u d-dħul (header `STRMFILE`, dejta maħżuna kif inhi); kull `Maps*.gtp` tal-installazzjoni tat-test |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, il-limiti tal-logħob u `MapNW/NE/SE/SW`; kull wieħed tal-installazzjoni tat-test |
| Heightmaps (`height.dat`) | il-codec hawn taħt; kull settur tal-mapep iddekodifikat bis-sħiħ waqt li kien qed jinħadem juża l-bitstream tiegħu eżatt (l-aktar il-padding tal-bytes li jifdal), il-bqija ikkontrollat bl-header. Ikkontrollat bit-bit kontra l-fajls mhux ikkompressati `distlod.raw` li l-logħba tagħti ħdejn `distlod.dat` tagħhom, u kontra heightmap proprja ta' mappa għal distanzi twal (korrelazzjoni 0.999) |
| Għoli | metri = raw x heightMul / 256 - SeaLevel x heightMul. Il-baħar ta' mappa jiddekodifika eżatt għall-għoli li jagħtu l-kummenti tal-hini tagħha; dak ta' oħra, fil-bordura tagħha, għal `bounds_level` |
| Tqegħid | bilineari bejn l-erba' kantunieri tal-hini, ringiela 0 tramuntana, kolonna 0 punent. Ikkontrollat fuq mappa kontra rħula, kosti u ibħra magħrufa (għoli tar-rħula sa madwar 10 m minn dawk veri, l-ibħra taħt il-livell tal-baħar). Il-kantunieri huma kwadrilaterali, mhux il-projezzjoni proprja tal-logħba, allura stenna xi mijiet ta' metri żball f'nofs mappa kbira. Il-hini ta' familja waħda ta' mapep iġorr il-kantunieri ta' mappa oħra (jkopru frazzjoni tad-daqs veru tagħha); dan jinstab, u dik il-familja titqiegħed minflok b'landmark fit: irħula u ajrudromi tad-databases tal-postijiet proprji tal-logħba (`*.ldfbin`) kontra l-pożizzjonijiet veri tagħhom, rms ta' ftit kilometri (irħula kontra l-ajrudromi msemmija għalihom, u koordinati tal-postijiet veri sa madwar kilometru); il-JSON jelenka kull landmark u r-residwu tiegħu |
| Water mask (`water.wtr`: erba' livelli piramida ta' tiles, kull tile tabella ta' blokki ta' 400 m, kull blokk art, mimli jew parzjalment ilma bil-forma tiegħu f'bit stream) | il-container jinqara fuq kull mappa (ebda byte ma jifdal fuq il-fajls iddekodifikati bis-sħiħ); il-forma ġewwa blokk parzjalment ilma **ma tiddekodifikax**. Blokki mimlija huma ilma; f'blokki parzjalment ilma kampjun huwa ilma fejn il-water map (`height_w.dat`, l-istess codec bħall-heightmap) hija 'l fuq mill-art, jew, ħdejn lag, fejn l-art mhix ogħla mill-lag; blokki ta' art huma niexfa. Dan ineħħi l-marsa li l-water map waħedha tirrapporta bħala ilma. Xmajjar idejqin mill-grilja tal-output joħorġu maqsumin f'biċċiet |
| Footprints tal-irħula (il-meshes decal li `textures.tini` jelenka: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: tiles ta' 25.6 km ta' trijangoli ċatti bit-texture) | moqrija fuq kull mappa; il-wiċċijiet li t-texture tagħhom hija raħal, rħula jew art industrijali jinżammu. Ikkontrollati kontra rħula veri fuq ftit mapep (raħal fuq iż-żewġ naħat ta' xmara, konfluwenza). Huma footprints: il-logħba tqiegħed il-bini waqt it-tħaddim, u l-fajls ma jżommu ebda bini |
| Ajrudromi, pontijiet, bini | **ma jinqarawx**: l-ajrudromi huma oġġetti tal-missjoni, il-bini jiġi mit-tqegħid proprju tal-logħba |
| Foresti (`forest_map.wtr`) | il-blokki tagħha jinqraw bl-istess mod, imma kważi kull blokk huwa "parzjalment foresta", allura mingħajr il-bit stream ma hemm ebda mask tal-foresta użabbli; mhux imfassla |
| It-texturi tal-art | ma jinqarawx |

## Il-codec tal-heightmap {#the-heightmap-codec}

Ħadem mill-fajls tad-dejta biss; ebda kodiċi tal-logħba ma nqara jew ġie diżassemblat.
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

Setturi parzjali fuq it-truf tal-lemin u t'isfel huma mimlija u maqtugħa. L-istess
codec iżomm il-water map u l-heightmap tad-distanzi twal.

## Landmark fits {#landmark-fits}

Fejn il-kantunieri ta' mappa ma jistgħux jintużaw, `landmarks.py` iqiegħed mappa affine mill-
metri tal-logħba għall-art bil-least squares: pożizzjonijiet tal-logħba mill-fajls proprji tal-utent
(blokki `Airfield` tal-missjonijiet, id-databases tal-postijiet tal-karriera), pożizzjonijiet veri
minn tabelli tal-koordinati ppubblikati tal-postijiet fil-kodiċi. Il-`georeference` tal-JSON
iġorr il-matriċi, l-oriġini, kull landmark bir-residwu tiegħu
u r-rms.
