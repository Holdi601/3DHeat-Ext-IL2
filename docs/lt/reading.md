---
title: "Kaip skaitomi failai"
nav_order: 5
lang: lt
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Kaip skaitomi failai {#how-the-files-are-read}

| Dalis | Būsena |
|---|---|
| Archyvai (`data/*.gtp`, Great Battles) | failų lentelė (`S16R`, `STRMFAT?`, `DIR!`/`FILE` įrašai) ir įrašai (`STRMFILE` antraštė, duomenys saugomi kaip yra); kiekvienas `Maps*.gtp` bandomame įdiegime |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, žaidimo ribos ir `MapNW/NE/SE/SW`; kiekvienas bandomo įdiegimo |
| Reljefo žemėlapiai (`height.dat`) | toliau aprašytas kodekas; kiekvienas žemėlapių sektorius, iškoduotas visiškai dirbant su juo, tiksliai naudoja savo bitų srautą (daugiausia likęs baitų užpildas), likusieji patikrinti pagal antraštę. Patikrinta bit po bito su nesuspaustais `distlod.raw` failais, kuriuos žaidimas pateikia šalia savo `distlod.dat`, ir su žemėlapio paties tolimo LOD reljefo žemėlapiu (koreliacija 0,999) |
| Aukščiai | metrai = neapdorotas x heightMul / 256 - SeaLevel x heightMul. Žemėlapio jūra iškoduojama į tiksliai tą aukštį, kurį nurodo jo hini komentarai; kito – jo krašto į `bounds_level` |
| Įdėjimas | bilinearinis tarp keturių hini kampų, 0 eilutė – šiaurė, 0 stulpelis – vakarai. Patikrinta vienam žemėlapiui pagal žinomus miestus, pakrantes ir jūras (miestų aukščiai maždaug 10 m tikslumu nuo tikrųjų, jūros žemiau jūros lygio). Kampai sudaro keturkampį, o ne žaidimo paties projekciją, todėl didelio žemėlapio viduryje tikėkitės kelių šimtų metrų paklaidos. Vieno žemėlapių šeimos hini nurodo kito žemėlapio kampus (jie apima tik dalį jo tikro dydžio); tai aptinkama, ir ta šeima įdedama orientyrų pritaikymu: žaidimo pačių vietovių duomenų bazių (`*.ldfbin`) miestai ir oro uostai lyginami su jų tikromis pozicijomis, vidutinė kvadratinė paklaida – keli kilometrai (miestai – su oro uostais, pavadintais jų vardu, o tikrų vietovių koordinatės – iki maždaug kilometro); JSON išvardija kiekvieną orientyrą ir jo paklaidą |
| Vandens kaukė (`water.wtr`: keturi piramidės lygiai iš plytelių, kiekviena plytelė – 400 m blokų lentelė, kiekvienas blokas – sausuma, pilnas arba iš dalies vandens su savo forma bitų sraute) | konteineris skaitomas kiekviename žemėlapyje (visiškai iškoduotuose failuose nelieka nė vieno baito); forma iš dalinai vandens bloko vidaus **neiškoduojama**. Pilni blokai yra vanduo; dalinai vandens blokuose mėginys yra vanduo ten, kur vandens žemėlapis (`height_w.dat`, tas pats kodekas kaip reljefo žemėlapio) yra virš žemės, arba šalia ežero – kur žemė nėra aukštesnė už ežerą; sausumos blokai yra sausi. Tai pašalina pelkę, kurią vien vandens žemėlapis pažymi kaip vandenį. Upės, siauresnės nei išvesties tinklelis, išeina suskaldytos į dalis |
| Miestų plotai (dekalų tinklai, kuriuos išvardija `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh` ir kt.: 25,6 km plytelės iš plokščių tekstūruotų trikampių) | skaitomi kiekviename žemėlapyje; išlaikomi paviršiai, kurių tekstūra yra miestas, kaimas ar pramoninė žemė. Patikrinta su tikrais miestais keliuose žemėlapiuose (miestas abiejuose upės krantuose, santaka). Tai plotai: žaidimas pastatus deda paleidimo metu, o failuose pastatų nėra |
| Oro uostai, tiltai, pastatai | **neskaitomi**: oro uostai yra misijų objektai, pastatai ateina iš žaidimo pačio išdėstymo |
| Miškai (`forest_map.wtr`) | jo blokai skaitomi tuo pačiu būdu, bet beveik kiekvienas blokas yra „iš dalies miškas“, todėl be bitų srauto nėra naudingos miško kaukės; nepiešiama |
| Žemės tekstūros | neskaitomos |

## Reljefo kodekas {#the-heightmap-codec}

Atkurta vien iš duomenų failų; jokio žaidimo kodo neskaityta ir neišardyta.
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

Dalinius sektorius dešiniajame ir apatiniame kraštuose užpildomi ir apkarpomi. Tas pats kodekas
galioja vandens žemėlapiui ir tolimo LOD reljefo žemėlapiui.

## Orientyrų pritaikymai {#landmark-fits}

Ten, kur žemėlapio kampų naudoti negalima, `landmarks.py` pritaiko afininį atvaizdavimą iš žaidimo metrų į Žemę
mažiausių kvadratų metodu: žaidimo pozicijos iš paties vartotojo failų (misijų `Airfield` blokai, karjeros vietovių
duomenų bazės), tikros pozicijos iš lentelių su kode paskelbtomis vietų koordinatėmis. JSON `georeference` saugo matricą,
pradžios tašką, kiekvieną orientyrą su paklaida ir vidutinę kvadratinę paklaidą.
