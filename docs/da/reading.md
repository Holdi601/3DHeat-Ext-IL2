---
title: Sådan læses filerne
nav_order: 5
lang: "da"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Sådan læses filerne {#how-the-files-are-read}

| Del | Status |
|---|---|
| Arkiver (`data/*.gtp`, Great Battles) | filtabellen (`S16R`, `STRMFAT?`, `DIR!`/`FILE`-poster) og indtastningerne (`STRMFILE`-header, data gemt som de er); hver `Maps*.gtp` i testinstallationen |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, spilgrænserne og `MapNW/NE/SE/SW`; hver én i testinstallationen |
| Højdekort (`height.dat`) | kodeken nedenfor; hver sektor af kortene afkodet fuldt ud, mens den blev udredt, bruger dens bitstrøm præcist (højst den byte-udfyldning, der er tilbage), resten kontrolleret via header. Kontrolleret bit for bit mod de ukomprimerede `distlod.raw`-filer, spillet leverer ved siden af deres `distlod.dat`, og mod et korts eget fjern-LOD-højdekort (korrelation 0,999) |
| Højder | meter = rå x heightMul / 256 - SeaLevel x heightMul. Et korts hav afkodes til præcis den højde, dets hini-kommentarer angiver; et andets kant til dens `bounds_level` |
| Placering | bilineær mellem hini'ens fire hjørner, række 0 nord, kolonne 0 vest. Kontrolleret på et kort mod kendte byer, kyster og have (byhøjder inden for cirka 10 m af de rigtige, havene under havniveau). Hjørnerne er en firkant, ikke spillets egen projektion, så regn med nogle hundrede meters fejl midt på et stort kort. En kortfamilies hini bærer hjørnerne af et andet kort (de spænder over en brøkdel af dets rigtige størrelse); dette opdages, og den familie placeres i stedet ved en landemærketilpasning: byer og flyvepladser fra spillets egne placeringsdatabaser (`*.ldfbin`) mod deres rigtige positioner, rms på et par kilometer (byer mod flyvepladserne, der er opkaldt efter dem, og koordinaterne for de rigtige steder til cirka en kilometer); JSON'en lister hvert landemærke og dets afvigelse |
| Vandmaske (`water.wtr`: fire pyramideniveauer af fliser, hver flise en tabel af 400 m-blokke, hver blok land, fuld eller delvis vand med dens form i en bitstrøm) | containeren læses på hvert kort (ingen byte tilbage på de filer, der er afkodet fuldt ud); formen inde i en delvist vandfyldt blok er **ikke afkodet**. Fulde blokke er vand; i delvist vandfyldte blokke er en prøve vand, hvor vandkortet (`height_w.dat`, samme kodek som højdekortet) ligger over jorden, eller, ved siden af en sø, hvor jorden ikke er højere end søen; landblokke er tørre. Det fjerner den mose, vandkortet alene rapporterer som vand. Floder smallere end outputgitteret kommer ud i stykker |
| Byfodaftryk (dekalmeshene, `textures.tini` lister: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: 25,6 km fliser af flade teksturerede trekanter) | læst på hvert kort; de flader, hvis tekstur er en by, landsby eller industrijord, beholdes. Kontrolleret mod de rigtige byer på nogle få kort (en by på begge bredder af en flod, et sammenløb). Det er fodaftryk: spillet placerer bygningerne under kørsel, og filerne holder ingen bygninger |
| Flyvepladser, broer, bygninger | **ikke læst**: flyvepladser er missionsobjekter, bygninger kommer fra spillets egen placering |
| Skove (`forest_map.wtr`) | dets blokke læses på samme måde, men næsten hver blok er "delvist skov", så uden bitstrømmen er der ingen brugbar skovmaske; ikke tegnet |
| Jordens teksturer | ikke læst |

## Højdekortkodeken {#the-heightmap-codec}

Udredt fra datafilerne alene; ingen spilkode blev læst eller disassembleret.
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

Delvise sektorer ved højre og nedre kant er udfyldt og beskåret. Den samme
kodek gælder for vandkortet og fjern-LOD-højdekortet.

## Landemærketilpasninger {#landmark-fits}

Hvor et korts hjørner ikke kan bruges, tilpasser `landmarks.py` en affin afbildning fra
spillets meter til jorden ved mindste kvadraters metode: spilpositioner fra brugerens egne
filer (missionens `Airfield`-blokke, karrieredatabaserne over placeringer), rigtige positioner fra
tabeller over stedernes offentliggjorte koordinater i koden. JSON'ens
`georeference` bærer matricen, udgangspunktet, hvert landemærke med dets afvigelse
og rms-værdien.
