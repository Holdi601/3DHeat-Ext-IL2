---
title: "Jak se soubory čtou"
nav_order: 5
lang: cs
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Jak se soubory čtou {#how-the-files-are-read}

| Část | Stav |
|---|---|
| Archivy (`data/*.gtp`, Great Battles) | tabulka souborů (záznamy `S16R`, `STRMFAT?`, `DIR!`/`FILE`) a položky (hlavička `STRMFILE`, data uložená tak, jak jsou); každý `Maps*.gtp` testovací instalace |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, limity hry a `MapNW/NE/SE/SW`; každý soubor testovací instalace |
| Výškové mapy (`height.dat`) | kodek níže; každý sektor map dekódovaný celý při jeho odvozování používá svůj bitový proud přesně (nejvýše zbytkové bajtové doplnění), zbytek se ověřil podle hlavičky. Ověřeno bit po bitu proti nekomprimovaným souborům `distlod.raw`, které hra dodává vedle `distlod.dat`, a proti vlastní vzdálené výškové mapě LOD mapy (korelace 0,999) |
| Výšky | metry = surové x heightMul / 256 - SeaLevel x heightMul. Moře mapy se dekóduje přesně na výšku, kterou uvádějí komentáře jejího hini; hranice jiné na její `bounds_level` |
| Umístění | bilineárně mezi čtyřmi rohy hini, řádek 0 na sever, sloupec 0 na západ. Ověřeno na mapě proti známým městům, pobřežím a mořím (výšky měst zhruba do 10 m od skutečných, moře pod hladinou). Rohy tvoří čtyřúhelník, nikoli vlastní projekci hry, takže u velké mapy počítejte s chybou několika set metrů uprostřed. Hini jedné rodiny map nese rohy jiné mapy (rozpínají zlomek její skutečné velikosti); to se zjistí a tato rodina se místo toho umístí přizpůsobením orientačním bodům: města a letiště z databází míst hry (`*.ldfbin`) proti jejich skutečným polohám, střední kvadratická odchylka několik kilometrů (města proti letištím pojmenovaným po nich a souřadnice skutečných míst na přibližně kilometr). JSON vypisuje každý orientační bod a jeho odchylku |
| Maska vody (`water.wtr`: čtyři úrovně pyramidy dlaždic, každá dlaždice je tabulka bloků po 400 m, každý blok je souš, plný nebo částečně vodní s tvarem v bitovém proudu) | kontejner se čte na každé mapě (žádný zbylý bajt u souborů dekódovaných celých); tvar uvnitř částečně vodního bloku se **nedekóduje**. Plné bloky jsou voda; v částečně vodních blocích je vzorek vodou, kde je mapa vody (`height_w.dat`, stejný kodek jako výšková mapa) nad terénem, nebo vedle jezera tam, kde terén není výše než jezero; bloky souše jsou suché. Tím se odstraní močál, který samotná mapa vody hlásí jako vodu. Řeky užší než výstupní mřížka vycházejí rozpadlé na kusy |
| Půdorysy měst (texturované plochy dekalů, které uvádí `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: dlaždice 25,6 km plochých texturovaných trojúhelníků) | čtou se na každé mapě; ponechají se plochy, jejichž textura je město, vesnice nebo průmyslová plocha. Ověřeno proti skutečným městům na několika mapách (město na obou březích řeky, soutok). Jsou to půdorysy: budovy hra umísťuje za běhu a soubory žádné budovy neobsahují |
| Letiště, mosty, budovy | **nečtou se**: letiště jsou objekty misí, budovy pocházejí z vlastního umísťování hry |
| Lesy (`forest_map.wtr`) | jeho bloky se čtou stejně, ale téměř každý blok je „částečně les“, takže bez bitového proudu není použitelná maska lesů; nekreslí se |
| Textury terénu | nečtou se |

## Kodek výškové mapy {#the-heightmap-codec}

Odvozeno pouze z datových souborů; nebyl čten ani rozebírán herní kód.
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

Částečné sektory na pravém a dolním okraji se doplní a oříznou. Stejný
kodek platí pro mapu vody a pro vzdálenou výškovou mapu LOD.

## Přizpůsobení orientačním bodům {#landmark-fits}

Tam, kde nelze použít rohy mapy, `landmarks.py` přizpůsobí afinní zobrazení z metrů hry
na Zemi metodou nejmenších čtverců: polohy ve hře z vlastních souborů uživatele (bloky `Airfield`
v misích, databáze míst kariéry), skutečné polohy z tabulek zveřejněných souřadnic míst
v kódu. Pole `georeference` v JSONu nese matici, počátek, každý orientační bod s jeho
odchylkou a střední kvadratickou odchylku.
