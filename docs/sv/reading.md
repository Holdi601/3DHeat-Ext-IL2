---
title: Så läses filerna
nav_order: 5
lang: "sv"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Så läses filerna {#how-the-files-are-read}

| Del | Status |
|---|---|
| Arkiv (`data/*.gtp`, Great Battles) | filtabellen (`S16R`, `STRMFAT?`, `DIR!`/`FILE`-poster) och posterna (`STRMFILE`-huvudet, data lagrad som den är); varje `Maps*.gtp` i testinstallationen |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, spelgränserna och `MapNW/NE/SE/SW`; varje fil i testinstallationen |
| Höjdkartor (`height.dat`) | kodeken nedan; varje sektor av kartorna avkodad helt medan den togs fram använder sin bitström exakt (högst den byte-utfyllnad som blir över), resten kontrollerad via huvudet. Kontrollerad bit för bit mot de okomprimerade `distlod.raw`-filerna som spelet levererar bredvid sina `distlod.dat`, och mot en kartas egen höjdkarta för fjärrdetaljnivån (korrelation 0,999) |
| Höjder | meter = rått x heightMul / 256 - SeaLevel x heightMul. En kartas hav avkodas till exakt den höjd hini:ns kommentarer anger; en annans kant till dess `bounds_level` |
| Placering | bilinjärt mellan hini:ns fyra hörn, rad 0 norr, kolumn 0 väster. Kontrollerad på en karta mot kända städer, kuster och hav (stadshöjder inom ungefär 10 m från de verkliga, haven under havsnivån). Hörnen bildar en fyrhörning, inte spelets egen projektion, så räkna med några hundra meters fel i mitten av en stor karta. En kartfamiljs hini bär hörnen för en annan karta (de spänner över en bråkdel av dess verkliga storlek); detta upptäcks, och den familjen placeras i stället med en landmärkesanpassning: städer och flygfält från spelets egna platsdatabaser (`*.ldfbin`) mot deras verkliga positioner, medelkvadratfel på ett par kilometer (städer mot flygfälten som är uppkallade efter dem, och koordinaterna för de verkliga platserna till ungefär en kilometer); JSON-filen listar varje landmärke och dess avvikelse |
| Vattenmask (`water.wtr`: fyra pyramidnivåer av kakel, där varje kakel är en tabell av 400 m block, och varje block är land, helt vatten eller delvis vatten med sin form i en bitström) | containern läses på varje karta (ingen byte blir över på filerna som avkodats helt); formen inuti ett delvis vattenblock **avkodas inte**. Helt vatten-block är vatten; i delvis vatten-block är ett prov vatten där vattenkartan (`height_w.dat`, samma kodek som höjdkartan) ligger över marken, eller, bredvid en sjö, där marken inte är högre än sjön; landblock är torra. Det tar bort det sankmark som vattenkartan ensam rapporterar som vatten. Floder smalare än utdatarutnätet blir sönderbrutna i bitar |
| Stadsavtryck (dekalmeshar som `textures.tini` listar: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: 25,6 km kakel av platta texturerade trianglar) | läses på varje karta; de ytor vars textur är stad, by eller industrimark behålls. Kontrollerat mot de verkliga städerna på några kartor (en stad på båda sidor om en flod, ett sammanflöde). De är avtryck: spelet placerar byggnaderna vid körning, och filerna innehåller inga byggnader |
| Flygfält, broar, byggnader | **läses inte**: flygfält är uppdragsobjekt, byggnader kommer från spelets egen placering |
| Skogar (`forest_map.wtr`) | dess block läses på samma sätt, men nästan varje block är "delvis skog", så utan bitströmmen finns ingen användbar skogsmask; ritas inte |
| Markens texturer | läses inte |

## Höjdkartans kodek {#the-heightmap-codec}

Tagen fram enbart från datafilerna; ingen spelkod lästes eller disassemblerades.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            från filens början, radvis, översta raden först
sector: u16 count (bytes som följer), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        sedan en bitström läst MSB först:
  PRE   2 * (log2(sectorSize) - 5) bitar, hittills alltid 0
  LIT   det första provet: tecken (1), n (LW bitar), belopp (n + 1 bitar)
  sedan tills sektorn är full:
    0 LIT       nästa = föregående + LIT
    1 RUN LIT   det föregående provet upprepas RUN gånger (k: 3 bitar, m: k + 1 bitar, RUN = m + 1),
                sedan (om sektorn inte är full) nästa = föregående + LIT
  värdena är 16-bitars: läs dem modulo 65536
```

Delsektorer vid de högra och nedre kanterna utfylls och beskärs. Samma kodek gäller
vattenkartan och höjdkartan för fjärrdetaljnivån.

## Landmärkesanpassningar {#landmark-fits}

Där en kartas hörn inte kan användas, anpassar `landmarks.py` en affin avbildning från
spelets meter till jorden med minsta kvadrater: spelpositioner från användarens egna
filer (uppdragens `Airfield`-block, karriärens platsdatabaser), verkliga positioner från
tabeller över platsernas publicerade koordinater i koden. JSON-filens `georeference` bär
matrisen, ursprunget, varje landmärke med sin avvikelse och medelkvadratfelet.
