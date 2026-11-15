---
title: "Hoe de bestanden worden gelezen"
nav_order: 5
lang: "nl"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Hoe de bestanden worden gelezen {#how-the-files-are-read}

| Onderdeel | Status |
|---|---|
| Archieven (`data/*.gtp`, Great Battles) | de bestandstabel (`S16R`, `STRMFAT?`, `DIR!`/`FILE`-records) en de items (`STRMFILE`-kop, gegevens zoals ze zijn opgeslagen); elk `Maps*.gtp` van de testinstallatie |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, de speelgrenzen en `MapNW/NE/SE/SW`; elk van de testinstallatie |
| Hoogtekaarten (`height.dat`) | de codec hieronder; elke sector van de kaarten is volledig gedecodeerd terwijl hij werd uitgewerkt, en gebruikt zijn bitstroom exact (hooguit de overgebleven bytevulling), de rest is gecontroleerd op de kop. Bit voor bit gecontroleerd tegen de ongecomprimeerde `distlod.raw`-bestanden die het spel naast hun `distlod.dat` meelevert, en tegen de verre-LOD-hoogtekaart van een kaart zelf (correlatie 0,999) |
| Hoogten | meters = ruwe x heightMul / 256 - SeaLevel x heightMul. De zee van een kaart decodeert exact naar de hoogte die de opmerkingen in zijn hini geven; de rand van een andere naar zijn `bounds_level` |
| Plaatsing | bilineair tussen de vier hoeken van de hini, rij 0 noord, kolom 0 west. Gecontroleerd op een kaart tegen bekende steden, kusten en zeeën (hoogten van steden binnen ongeveer 10 m van de echte, de zeeën onder zeeniveau). De hoeken vormen een vierhoek, geen eigen projectie van het spel, dus reken op enkele honderden meters fout in het midden van een grote kaart. De hini van één kaartfamilie bevat de hoeken van een andere kaart (ze overspannen een deel van hun echte grootte); dit wordt herkend, en die familie wordt dan geplaatst met een oriëntatiepuntenpassing: steden en vliegvelden uit de eigen locatiedatabases van het spel (`*.ldfbin`) tegen hun echte posities, rms van een paar kilometer (steden tegen de vliegvelden die naar hen genoemd zijn, en coördinaten van de echte plaatsen tot ongeveer een kilometer); de JSON somt elk oriëntatiepunt en zijn afwijking op |
| Watermasker (`water.wtr`: vier piramideniveaus van tegels, elke tegel een tabel van blokken van 400 m, elk blok land, vol of deels water met zijn vorm in een bitstroom) | de container wordt op elke kaart gelezen (geen byte over bij de volledig gedecodeerde bestanden); de vorm binnen een deels waterblok wordt **niet gedecodeerd**. Volle blokken zijn water; in deels-waterblokken is een monster water waar de watermap (`height_w.dat`, dezelfde codec als de hoogtekaart) boven de grond ligt, of, naast een meer, waar de grond niet hoger is dan het meer; landblokken zijn droog. Daarmee verdwijnt het moeras dat de watermap alleen als water rapporteert. Rivieren die smaller zijn dan het uitvoerraster, komen in stukken uit elkaar |
| Voetafdrukken van steden (de decalmeshes die `textures.tini` vermeldt: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: tegels van 25,6 km met vlakke getextureerde driehoeken) | op elke kaart gelezen; de vlakken waarvan de textuur een stad, dorp of industrieterrein is, worden bewaard. Gecontroleerd tegen de echte steden op enkele kaarten (een stad aan beide oevers van een rivier, een samenvloeiing). Het zijn voetafdrukken: het spel plaatst de gebouwen tijdens het spelen, en de bestanden bevatten geen gebouwen |
| Vliegvelden, bruggen, gebouwen | **niet gelezen**: vliegvelden zijn missieobjecten, gebouwen komen van de eigen plaatsing van het spel |
| Bossen (`forest_map.wtr`) | de blokken worden op dezelfde manier gelezen, maar bijna elk blok is "deels bos", dus zonder de bitstroom is er geen bruikbaar bosmasker; niet getekend |
| De textuur van de grond | niet gelezen |

## De hoogtekaartcodec {#the-heightmap-codec}

Uitgewerkt uit de gegevensbestanden alleen; er is geen spelcode gelezen of gedisassembleerd.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            vanaf het begin van het bestand, rij voor rij, bovenste rij eerst
sector: u16 count (bytes die volgen), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        daarna een bitstroom, MSB eerst gelezen:
  PRE   2 * (log2(sectorSize) - 5) bits, tot nu toe altijd 0
  LIT   het eerste monster: teken (1), n (LW bits), grootte (n + 1 bits)
  daarna tot de sector vol is:
    0 LIT       volgende = vorige + LIT
    1 RUN LIT   het vorige monster herhaalt zich RUN keer (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                daarna (tenzij de sector vol is) volgende = vorige + LIT
  waarden zijn 16-bit: lees ze modulo 65536
```

Gedeeltelijke sectoren aan de rechter- en onderrand worden opgevuld en bijgesneden. Dezelfde
codec geldt voor de watermap en de verre-LOD-hoogtekaart.

## Oriëntatiepuntenpassingen {#landmark-fits}

Waar de hoeken van een kaart niet bruikbaar zijn, past `landmarks.py` een affiene
afbeelding van de meters van het spel naar de aarde, met de kleinste kwadraten: posities in het spel uit de eigen
bestanden van de gebruiker (`Airfield`-blokken in missies, de databases met carrièrelocaties),
echte posities uit tabellen met de gepubliceerde coördinaten van de plaatsen in de code. De
`georeference` van de JSON bevat de matrix, de oorsprong, elk oriëntatiepunt met zijn afwijking
en de rms.
