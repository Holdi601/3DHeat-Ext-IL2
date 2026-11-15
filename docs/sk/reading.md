---
title: "Ako sa čítajú súbory"
nav_order: 5
lang: "sk"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Ako sa čítajú súbory {#how-the-files-are-read}

| Časť | Stav |
|---|---|
| Archívy (`data/*.gtp`, Great Battles) | tabuľka súborov (záznamy `S16R`, `STRMFAT?`, `DIR!`/`FILE`) a položky (hlavička `STRMFILE`, dáta uložené tak, ako sú); každý `Maps*.gtp` testovacej inštalácie |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, hracie hranice a `MapNW/NE/SE/SW`; každý z testovacej inštalácie |
| Výškové mapy (`height.dat`) | kodek nižšie; každý sektor mapy, dekódovaný celý pri zisťovaní, používa svoj bitový prúd presne (najviac zvyšnú bajtovú výplň), zvyšok sa overil podľa hlavičky. Overené bit po bite voči nekomprimovaným súborom `distlod.raw`, ktoré hra dodáva vedľa svojich `distlod.dat`, a voči vzdialenej výškovej mape LOD samotnej mapy (korelácia 0,999) |
| Výšky | metre = surové x heightMul / 256 - SeaLevel x heightMul. More mapy sa dekóduje presne na výšku, ktorú uvádzajú komentáre jej hini; hranica inej na jej `bounds_level` |
| Umiestnenie | bilineárne medzi štyrmi rohmi hini, riadok 0 na sever, stĺpec 0 na západ. Overené na mape voči známym mestám, pobrežiam a moriam (výšky miest do približne 10 m od skutočných, moria pod hladinou mora). Rohy sú štvoruholník, nie vlastná projekcia hry, takže v strede veľkej mapy čakajte niekoľko stoviek metrov chyby. Hini jednej rodiny máp nesie rohy inej mapy (rozpätie zaberá zlomok jej skutočnej veľkosti); to sa zistí a táto rodina sa namiesto toho umiestni prispôsobením orientačným bodom: mestá a letiská z vlastných databáz miest hry (`*.ldfbin`) voči ich skutočným polohám, stredná kvadratická odchýlka niekoľko kilometrov (mestá voči letiskám, ktoré sú po nich pomenované, a súradnice skutočných miest na približne kilometer); JSON vypisuje každý orientačný bod a jeho odchýlku |
| Maska vody (`water.wtr`: štyri úrovne pyramídy dlaždíc, každá dlaždica je tabuľka blokov po 400 m, každý blok je pevnina, úplne alebo čiastočne voda s tvarom v bitovom prúde) | kontajner sa číta na každej mape (žiadny zvyšný bajt pri súboroch dekódovaných celých); tvar vnútri čiastočne vodného bloku sa **nedekóduje**. Úplné bloky sú voda; v čiastočne vodných blokoch je vzorka voda tam, kde mapa vody (`height_w.dat`, rovnaký kodek ako výšková mapa) leží nad zemou, alebo, pri jazere, kde zem nie je vyššia než jazero; blok pevniny je suchý. To odstráni močiar, ktorý mapa vody sama hlási ako vodu. Rieky užšie než výstupná mriežka vychádzajú rozbité na kúsky |
| Stopy miest (siete nálepiek, ktoré zoznamuje `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: dlaždice 25,6 km plochých texturovaných trojuholníkov) | čítajú sa na každej mape; ponechajú sa plochy, ktorých textúra je mesto, dedina alebo priemyselná zem. Overené voči skutočným mestám na niekoľkých mapách (mesto na oboch brehoch rieky, sútok). Sú to stopy: hra umiestňuje budovy za behu a súbory budovy neobsahujú |
| Letiská, mosty, budovy | **nečítajú sa**: letiská sú objekty misií, budovy pochádzajú z umiestnenia samotnej hry |
| Lesy (`forest_map.wtr`) | ich bloky sa čítajú rovnako, ale takmer každý blok je „čiastočne les“, takže bez bitového prúdu neexistuje použiteľná maska lesa; nekreslí sa |
| Textúry zeme | nečítajú sa |

## Kodek výškovej mapy {#the-heightmap-codec}

Zistené len z dátových súborov; nečítal sa ani nerozoberal sa žiadny kód hry.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            od začiatku súboru, po riadkoch, horný riadok prvý
sector: u16 count (bajty, ktoré nasledujú), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        potom bitový prúd čítaný od najvyššieho bitu (MSB):
  PRE   2 * (log2(sectorSize) - 5) bitov, zatiaľ vždy 0
  LIT   prvá vzorka: znamienko (1), n (LW bitov), veľkosť (n + 1 bitov)
  potom, kým sektor nie je plný:
    0 LIT       ďalšia = predchádzajúca + LIT
    1 RUN LIT   predchádzajúca vzorka sa opakuje RUN-krát (k: 3 bity, m: k + 1 bitov, RUN = m + 1),
                potom (ak sektor nie je plný) ďalšia = predchádzajúca + LIT
  hodnoty sú 16-bitové: čítajú sa modulo 65536
```

Čiastočné sektory na pravom a dolnom okraji sa doplnia a orežú. Rovnaký
kodek platí pre mapu vody a vzdialenú výškovú mapu LOD.

## Prispôsobenie orientačným bodom {#landmark-fits}

Tam, kde sa rohy mapy nedajú použiť, `landmarks.py` prispôsobí afínne zobrazenie
z metrov hry na zem metódou najmenších štvorcov: polohy v hre z vlastných súborov
používateľa (bloky `Airfield` v misiách, databázy lokalít kariéry), skutočné polohy z tabuliek
zverejnených súradníc miest v kóde. Blok `georeference` v JSON nesie maticu, začiatok, každý orientačný bod s jeho odchýlkou a strednú kvadratickú odchýlku.
