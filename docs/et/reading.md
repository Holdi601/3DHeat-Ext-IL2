---
title: "Kuidas faile loetakse"
nav_order: 5
lang: et
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Kuidas faile loetakse {#how-the-files-are-read}

| Osa | Staatus |
|---|---|
| Arhiivid (`data/*.gtp`, Great Battles) | failitabel (`S16R`, `STRMFAT?`, `DIR!`/`FILE` kirjed) ja kirjed (`STRMFILE` päis, andmed salvestatud nii, nagu on); iga `Maps*.gtp` testinstallil |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, mängupiirid ja `MapNW/NE/SE/SW`; iga testinstalli oma |
| Kõrgustikukaardid (`height.dat`) | allpool olev kodek; iga kaardi sektor dekodeeriti täielikult selle väljaselgitamisel, kasutab oma bitivoogu täpselt (kõige rohkem üle jäänud baidi täite), ülejäänud kontrolliti päise järgi. Kontrollitud bitikaupa mängu kaasas olevate tavaliste `distlod.raw` failidega, mis on nende `distlod.dat` kõrval, ja kaardi enda kaugel-LOD kõrgustikukaardiga (korrelatsioon 0,999) |
| Kõrgused | meetrit = toor x heightMul / 256 - SeaLevel x heightMul. Kaardi meri dekodeerub täpselt sinna kõrgusele, mille tema hini kommentaarid annavad; teise kaardi piir oma `bounds_level`-ile |
| Paigutus | bilineaarne hini nelja nurga vahel, rida 0 põhi, veerg 0 lääs. Kontrollitud kaardil tuntud linnade, rannajoonte ja merede vastu (linnade kõrgused umbes 10 m täpsusega tegelikest, mered allpool merepinda). Nurgad on nelinurk, mitte mängu enda projektsioon, nii et suurel kaardil oodata keskel mõnesaja meetri viga. Ühe kaardiperekonna hini kannab teise kaardi nurki (need katavad murdosa tema tegelikust suurusest); see tuvastatakse, ja see perekond paigutatakse hoopis maamärkide sobitusega: mängu enda asukohaandmebaaside (`*.ldfbin`) linnad ja lennuväljad tegelike asukohtade vastu, ruutkeskmine viga paar kilomeetrit (linnad nimega lennuväljade vastu ja tegelike kohtade koordinaadid umbes kilomeetri täpsusega). JSON loetleb iga maamärgi ja selle jäägi |
| Veemask (`water.wtr`: neli püramiidi taset plaate, iga plaat on 400 m plokkide tabel, iga plokk on maa, täis või osaliselt vesi oma kujuga bitivoos) | konteiner loetakse igal kaardil (täielikult dekodeeritud failidel ei jää ühtegi baiti üle); osaliselt vee plokis olevat kuju **ei dekodeerita**. Täis plokid on vesi; osaliselt vee plokkides on proov vesi seal, kus veekaart (`height_w.dat`, sama kodek kui kõrgustikukaardil) on maapinnast kõrgemal, või järve kõrval seal, kus maapind ei ole järvest kõrgem; maaplokid on kuivad. See eemaldab soo, mida pelk veekaart näitab veena. Väiksemad jõed kui väljundi ruudustik tulevad katki tükkideks |
| Linnade jalajäljed (dekaali võrgud, mida `textures.tini` loetleb: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh` jt: 25,6 km plaadid lamedatest tekstureeritud kolmnurkadest) | loetakse igal kaardil; säilitatakse tahud, mille tekstuur on linn, küla või tööstusmaa. Kontrollitud mõnel kaardil tegelike linnade vastu (linn mõlemal jõekaldal, suudmealal). Need on jalajäljed: mäng paigutab hooned töö ajal, failid hooneid ei sisalda |
| Lennuväljad, sillad, hooned | **ei loeta**: lennuväljad on missiooni objektid, hooned tulevad mängu enda paigutusest |
| Metsad (`forest_map.wtr`) | selle plokid loetakse samamoodi, aga peaaegu iga plokk on "osaliselt mets", nii et ilma bitivooga ei ole kasutatavat metsamaski; ei joonistata |
| Maapinna tekstuurid | ei loeta |

## Kõrgustikukaardi kodek {#the-heightmap-codec}

Välja selgitatud ainult andmefailidest; mängu koodi ei loetud ega demonteeritud.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            faili algusest, rea kaupa, ülemine rida enne
sector: u16 count (järgnevad baidid), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        seejärel bitivoog loetuna MSB esimesena:
  PRE   2 * (log2(sectorSize) - 5) bitti, seni alati 0
  LIT   esimene proov: märk (1), n (LW bitti), suurus (n + 1 bitti)
  seejärel kuni sektor on täis:
    0 LIT       järgmine = eelmine + LIT
    1 RUN LIT   eelmine proov kordub RUN korda (k: 3 bitti, m: k + 1 bitti, RUN = m + 1),
                seejärel (kui sektor pole täis) järgmine = eelmine + LIT
  väärtused on 16-bitised: loe neid modulo 65536
```

Servade osalised sektorid paremal ja all on täidetud ja lõigatud. Sama kodek hoiab
veekaarti ja kaugel-LOD kõrgustikukaarti.

## Maamärkide sobitused {#landmark-fits}

Kui kaardi nurki ei saa kasutada, sobitab `landmarks.py` mängu meetritest maakera
afiinse kaardistuse vähimruutude meetodil: mängu asukohad kasutaja enda failidest
(missiooni `Airfield` plokid, karjääri asukohaandmebaasid), tegelikud asukohad kohtade avaldatud
koordinaatide tabelitest koodis. JSON-i `georeference` kannab maatriksit, algpunkti, iga
maamärki koos jäägiga ja ruutkeskmist.
