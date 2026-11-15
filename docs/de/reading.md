---
title: "Wie die Dateien gelesen werden"
nav_order: 5
lang: de
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Wie die Dateien gelesen werden {#how-the-files-are-read}

| Teil | Stand |
|---|---|
| Archive (`data/*.gtp`, Great Battles) | die Dateitabelle (`S16R`, `STRMFAT?`, `DIR!`-/`FILE`-Einträge) und die Einträge (Kopfteil `STRMFILE`, Daten unverändert gespeichert); jedes `Maps*.gtp` der Testinstallation |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, die Spielgrenzen und `MapNW/NE/SE/SW`; jede einzelne der Testinstallation |
| Höhenkarten (`height.dat`) | der Codec unten. Jeder Sektor der Karten wurde beim Herausarbeiten vollständig dekodiert und nutzt seinen Bitstrom genau (höchstens das übrige Byte-Auffüllen), der Rest wird am Kopfteil geprüft. Bit für Bit geprüft gegen die unkomprimierten `distlod.raw`-Dateien, die das Spiel neben ihren `distlod.dat` mitliefert, und gegen die eigene Höhenkarte einer Karte für entfernte Detailstufen (Korrelation 0,999) |
| Höhen | Meter = Rohwert x heightMul / 256 - SeaLevel x heightMul. Das Meer einer Karte dekodiert genau auf die Höhe, die die Kommentare ihrer hini angeben; die Grenze einer anderen auf ihr `bounds_level` |
| Platzierung | bilinear zwischen den vier Ecken der hini, Zeile 0 Norden, Spalte 0 Westen. An einer Karte geprüft gegen bekannte Städte, Küsten und Meere (Stadthöhen auf etwa 10 m genau, die Meere unter dem Meeresspiegel). Die Ecken bilden ein Viereck, nicht die eigene Projektion des Spiels; in der Mitte einer großen Karte ist mit einigen hundert Metern Fehler zu rechnen. Die hini einer Kartenfamilie trägt die Ecken einer anderen Karte (sie umspannen nur einen Bruchteil ihrer echten Größe); das wird erkannt, und diese Familie wird stattdessen über eine Anpassung an Orientierungspunkte platziert: Städte und Flugplätze aus den Ortsdatenbanken des Spiels (`*.ldfbin`) gegen ihre echten Positionen, RMS von ein paar Kilometern (Städte gegen die Flugplätze, die nach ihnen benannt sind, und Koordinaten der echten Orte auf etwa einen Kilometer genau); die JSON-Datei listet jeden Orientierungspunkt und seine Abweichung auf |
| Wassermaske (`water.wtr`: vier Pyramidenstufen aus Kacheln, jede Kachel eine Tabelle aus 400-m-Blöcken, jeder Block Land, ganz oder teilweise Wasser, mit seiner Form in einem Bitstrom) | der Container wird auf jeder Karte gelesen (bei den vollständig dekodierten Dateien bleibt kein Byte übrig). Die Form innerhalb eines teilweise wasserführenden Blocks wird **nicht dekodiert**. Volle Blöcke sind Wasser; in teilweise wasserführenden Blöcken ist ein Sample Wasser, wo die Wasserkarte (`height_w.dat`, gleicher Codec wie die Höhenkarte) über dem Boden liegt, oder – neben einem See – wo der Boden nicht höher liegt als der See; Landblöcke sind trocken. Das entfernt das Sumpfland, das die Wasserkarte allein als Wasser meldet. Flüsse, die schmaler sind als das Ausgaberaster, kommen in Stücken heraus |
| Stadtflächen (die Dekal-Netze, die `textures.tini` auflistet: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: Kacheln zu 25,6 km mit flachen, texturierten Dreiecken) | auf jeder Karte gelesen; die Flächen, deren Textur eine Stadt, ein Dorf oder industrieller Boden ist, bleiben. An den echten Städten einiger Karten geprüft (eine Stadt auf beiden Ufern eines Flusses, eine Flussmündung). Es sind Grundrisse: das Spiel setzt die Gebäude zur Laufzeit, die Dateien enthalten keine Gebäude |
| Flugplätze, Brücken, Gebäude | **nicht gelesen**: Flugplätze sind Missionsobjekte, Gebäude kommen aus der eigenen Platzierung des Spiels |
| Wälder (`forest_map.wtr`) | ihre Blöcke werden genauso gelesen, aber fast jeder Block ist „teilweise Wald“, daher gibt es ohne den Bitstrom keine brauchbare Waldmaske; nicht gezeichnet |
| Die Texturen des Bodens | nicht gelesen |

## Der Höhenkarten-Codec {#the-heightmap-codec}

Aus den Datendateien allein herausgearbeitet; es wurde kein Spielcode gelesen oder zerlegt. Little-Endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            ab Dateianfang, zeilenweise, oberste Zeile zuerst
sector: u16 count (Bytes, die folgen), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        dann ein Bitstrom, MSB zuerst gelesen:
  PRE   2 * (log2(sectorSize) - 5) Bits, bisher immer 0
  LIT   das erste Sample: Vorzeichen (1), n (LW Bits), Betrag (n + 1 Bits)
  dann, bis der Sektor voll ist:
    0 LIT       nächster = vorheriger + LIT
    1 RUN LIT   das vorherige Sample wiederholt sich RUN-mal (k: 3 Bits, m: k + 1 Bits, RUN = m + 1),
                dann (wenn der Sektor nicht voll ist) nächster = vorheriger + LIT
  Werte sind 16-Bit: modulo 65536 lesen
```

Randsektoren rechts und unten werden aufgefüllt und beschnitten. Derselbe Codec gilt für die Wasserkarte
und die Höhenkarte für entfernte Detailstufen.

## Anpassung an Orientierungspunkte {#landmark-fits}

Wo die Ecken einer Karte nicht verwendbar sind, passt `landmarks.py` eine affine Abbildung von den Metern
des Spiels auf die Erde an, nach der Methode der kleinsten Quadrate: Spielpositionen aus den eigenen
Dateien des Nutzers (`Airfield`-Blöcke der Missionen, die Ortsdatenbanken der Karriere), echte Positionen
aus Tabellen mit den veröffentlichten Koordinaten der Orte im Code. Der Eintrag `georeference` der
JSON-Datei enthält die Matrix, den Ursprung, jeden Orientierungspunkt mit seiner Abweichung und das RMS.
