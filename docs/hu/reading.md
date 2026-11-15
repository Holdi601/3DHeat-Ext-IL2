---
title: "Hogyan olvasódnak be a fájlok"
nav_order: 5
lang: "hu"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Hogyan olvasódnak be a fájlok {#how-the-files-are-read}

| Rész | Állapot |
|---|---|
| Archívumok (`data/*.gtp`, Great Battles) | a fájltáblázat (`S16R`, `STRMFAT?`, `DIR!`/`FILE` rekordok) és a bejegyzések (`STRMFILE` fejléc, az adat úgy, ahogy van tárolva); minden `Maps*.gtp` a tesztelt telepítésen |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, a játékhatárok és a `MapNW/NE/SE/SW`; mind a tesztelt telepítésen |
| Magassági térképek (`height.dat`) | az alábbi kódoló; minden térkép minden szektora teljesen dekódolva, miközben kitalálták, pontosan kihasználva a bitfolyamát (legfeljebb a bájtkitöltés marad), a többi a fejléc alapján ellenőrizve. Bitre pontosan ellenőrizve a tömörítetlen `distlod.raw` fájlokkal, amelyeket a játék a `distlod.dat` mellé szállít, és a térkép saját távoli LOD magassági térképével (korreláció 0,999) |
| Magasságok | méter = nyers x heightMul / 256 - SeaLevel x heightMul. Egy térkép tengere pontosan azt a magasságot adja, amelyet a hini megjegyzései adnak; egy másiké a `bounds_level` szerinti szegélye |
| Elhelyezés | lineáris interpoláció a hini négy sarka között, 0. sor észak, 0. oszlop nyugat. Egy térképen ismert városokhoz, partvonalakhoz és tengerekhez ellenőrizve (a városok magassága a valódiakhoz képest körülbelül 10 m-en belül, a tengerek a tengerszint alatt). A sarkok négyszöget alkotnak, nem a játék saját vetítését, így egy nagy térkép közepén néhány száz méteres hibára számítson. Az egyik térkéscsalád hini-je egy másik térkép sarkait tartalmazza (a valódi méretük töredékét fogják át); ezt észleljük, és azt a családot inkább egy tájékozódó illesztéssel helyezzük el: a játék saját helyadatbázisaiban (`*.ldfbin`) szereplő városok és repülőterek a valódi pozícióikhoz illesztve, néhány km-es rms-szel (a városok a róluk elnevezett repülőterekhez, és a valódi helyek koordinátái körülbelül egy km-en belül). A JSON minden tájékozódó pontot és annak maradék hibáját felsorolja |
| Víz-maszk (`water.wtr`: négy piramisszint csempékből, minden csempe 400 m-es blokkok táblázata, minden blokk szárazföld, teljesen víz vagy részben víz, alakzatát bitfolyamban) | a tároló minden térképen olvasódik (a teljesen dekódolt fájlokon nem marad bájt); a részben vizes blokk belső alakzata **nincs dekódolva**. A teljes blokkok víz; a részben vizes blokkokban egy minta víz, ahol a víztérkép (`height_w.dat`, ugyanaz a kódoló, mint a magassági térképé) a talaj fölött van, vagy egy tó mellett, ahol a talaj nem magasabb a tónál; a szárazföldi blokkok szárazak. Ez eltávolítja a mocsarat, amelyet a víztérkép önmagában vízként jelentene. A kimeneti rácsnál keskenyebb folyók darabokra törve jönnek ki |
| Városok alaprajzai (a `textures.tini` által felsorolt dekál-hálók: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh` stb.: 25,6 km-es csempék lapos, textúrázott háromszögekből) | minden térképen olvasva; a megtartott lapok azok, amelyek textúrája város, falu vagy ipari terület. Néhány térképen a valódi városokkal ellenőrizve (egy város a folyó két partján, egy összefolyás). Alaprajzok: a játék az épületeket futás közben helyezi el, a fájlok nem tartalmaznak épületeket |
| Repülőterek, hidak, épületek | **nem olvasódnak**: a repülőterek küldetésobjektumok, az épületeket a játék saját elhelyezése adja |
| Erdők (`forest_map.wtr`) | a blokkjai ugyanúgy olvasódnak, de szinte minden blokk „részben erdő”, így a bitfolyam nélkül nincs használható erdő-maszk; nem rajzolódik |
| A talaj textúrái | nem olvasódnak |

## A magassági térkép kódolója {#the-heightmap-codec}

Csak az adatfájlokból dolgozták ki; játékkódot nem olvastak és nem fordítottak vissza.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            a fájl elejétől, sorfolytonosan, felső sorral kezdve
szektor: u16 count (a következő bájtok száma), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        majd egy bitfolyam, MSB-vel először:
  PRE   2 * (log2(sectorSize) - 5) bit, eddig mindig 0
  LIT   az első minta: előjel (1), n (LW bit), nagyság (n + 1 bit)
  majd amíg a szektor tele nem lesz:
    0 LIT       a következő = előző + LIT
    1 RUN LIT   az előző minta RUN-szor ismétlődik (k: 3 bit, m: k + 1 bit, RUN = m + 1),
                majd (hacsak a szektor nincs tele) a következő = előző + LIT
  az értékek 16 bitesek: modulo 65536 olvassuk őket
```

A jobb és alsó szélen lévő részleges szektorok kitöltöttek és levágottak. Ugyanez a kódoló
érvényes a víztérképre és a távoli LOD magassági térképre is.

## Tájékozódó illesztések {#landmark-fits}

Ahol a térkép sarkai nem használhatók, a `landmarks.py` a játék méreteiből a földre egy affin
leképezést illeszt legkisebb négyzetek módszerével: a játék pozíciói a felhasználó saját fájljaiból
(küldetések `Airfield` blokkjai, a karrier helyadatbázisai), a valódi pozíciók a helyek közzétett
koordinátáinak táblázataiból, amelyek a kódban vannak. A JSON `georeference` mezője tartalmazza a
mátrixot, a kiindulópontot, minden tájékozódó pontot a maradék hibájával, és az rms-t.
