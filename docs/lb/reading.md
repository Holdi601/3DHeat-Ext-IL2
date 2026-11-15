---
title: "Wéi d'Dateie gelies ginn"
nav_order: 5
lang: lb
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Wéi d'Dateie gelies ginn {#how-the-files-are-read}

| Deel | Status |
|---|---|
| Archiver (`data/*.gtp`, Great Battles) | d'Dateitabell (`S16R`, `STRMFAT?`, `DIR!`/`FILE`-Records) an d'Entréeën (`STRMFILE`-Header, Daten esou gespäichert wéi se sinn); all `Maps*.gtp` vun der Test-Installatioun |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, d'Spillgrenzen an `MapNW/NE/SE/SW`; all eenzel vun der Test-Installatioun |
| Heightmaps (`height.dat`) | de Codec hei ënnen; all Sektor vun de Mappen, déi beim Erausfanne voll dekodéiert goufen, benotzt säi Bitstream genau (héchstens de Byte-Padding bleift iwwreg), de Rescht iwwer den Header gepréift. Bit fir Bit gepréift géint déi onkomprimiert `distlod.raw`-Dateien, déi d'Spill niewent hirem `distlod.dat` mat liwwert, a géint déi eege Distant-LOD-Heightmap vun enger Map (Korrelatioun 0,999) |
| Héichten | Meter = raw x heightMul / 256 - SeaLevel x heightMul. D'Mier vun enger Map dekodéiert op genau d'Héicht, déi seng hini-Kommentarer ginn; de Rand vun enger anerer op säi `bounds_level` |
| Placement | bilinear tëscht den véier Ecke vum hini, Rei 0 Norden, Kolonn 0 Westen. Bei enger Map géint bekannt Stied, Küsten a Mierer gepréift (d'Héichte vun de Stied bannent ongeféier 10 m vun de richtegen, d'Mierer ënner Mieresniveau). D'Ecke sinn e Véiereck, net dem Spill seng eege Projektioun, also rechent mat e puer honnert Meter Feeler an der Mëtt vun enger grousser Map. Dem hini vun enger Mappefamill hir Ecke si déi vun enger anerer Map (si spannen e Bruchdeel vun hirer richteger Gréisst); dat gëtt erkannt, an dës Famill gëtt amplaz mat engem Landmark-Fit placéiert: Stied a Fluchhäfen aus de Location-Datebanke vum Spill (`*.ldfbin`) géint hir richteg Positiounen, rms vun e puer Kilometer (Stied géint d'Fluchhäfen, déi no hinnen benannt sinn, a Koordinate vun de richtege Plaze bis ongeféier e Kilometer); de JSON lëscht all Landmark a säi Residuum |
| Waasser-Mask (`water.wtr`: véier Pyramidenniveaue vu Kacheleen, all Kachel eng Tabell vun 400-m-Blöcken, all Block Land, voll oder deelweis Waasser mat senger Form an engem Bitstream) | de Container gëtt bei all Map gelies (kee Byte bleift iwwreg bei de voll dekodéierten Dateien); d'Form bannent engem deelweis-Waasser-Block gëtt **net dekodéiert**. Voll Blöck sinn Waasser; a Blöck mat deelweis Waasser ass en Echantillon Waasser, wou d'Waasserkaart (`height_w.dat`, selwechte Codec wéi d'Heightmap) iwwer dem Buedem ass, oder, niewent engem Séi, wou de Buedem net méi héich ass wéi de Séi; Landblöck sinn dréchen. Dat hëlt de Sumpf ewech, dee bei der Waasserkaart eleng als Waasser gemellt gëtt. Flëss, méi schmuel wéi d'Ausgabegitter, kommen a Stécker gebrach eraus |
| Stad-Foussofdrëck (d'Decal-Meshen, déi `textures.tini` lëscht: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: 25,6-km-Kachele vu flaachen textureierten Dräiecker) | bei all Map gelies; d'Fläche, deenen hir Textur eng Stad, en Duerf oder en Industrie-Buedem ass, bleiwen. Bei e puer Mappen géint déi richteg Stied gepréift (eng Stad op béide Ufer vun engem Fluss, e Confluence). Et sinn Foussofdrëck: d'Spill placéiert d'Gebaier zur Laafzäit, an d'Dateie halen keng Gebaier |
| Fluchhäfen, Bréck, Gebaier | **net gelies**: Fluchhäfen sinn Missiounsobjeten, Gebaier kommen aus dem Placement vum Spill selwer |
| Bëscher (`forest_map.wtr`) | seng Blöck ginn op déiselwecht Aart gelies, awer bal all Block ass "deelweis Bësch", also gëtt et ouni de Bitstream keng benotzbar Bëschmask; net gezeechent |
| D'Texture vum Buedem | net gelies |

## De Heightmap-Codec {#the-heightmap-codec}

Eleng aus den Datendateien erausgefonnt; et gouf kee Spillcode gelies oder disassembléiert.
Little-Endian:

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

Deelweis Sektore um rechte an ënneschte Rand ginn opgefëllt a ofgeschnidden. Dee selwechte
Codec hält d'Waasserkaart an d'Distant-LOD-Heightmap.

## Landmark-Fits {#landmark-fits}

Wou d'Ecke vun enger Map net benotzt kënne ginn, fit `landmarks.py` eng affin Ofbildung vun de
Meter vum Spill op d'Äerd no de klengste Quadrater: Spillpositioune aus de
Dateie vum Benotzer (Missiouns-`Airfield`-Blöck, d'Career-Location-Datebanken), richteg Positiounen
aus Tabelle vun de publizéierte Koordinate vun de Plazen am Code. Dem JSON säi
`georeference` dréit d'Matrix, den Urspronk, all Landmark mat sengem Residuum
an den rms.
