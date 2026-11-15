---
title: "Cum se citesc fișierele"
nav_order: 5
lang: ro
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Cum se citesc fișierele {#how-the-files-are-read}

| Parte | Stare |
|---|---|
| Arhive (`data/*.gtp`, Great Battles) | tabelul de fișiere (înregistrările `S16R`, `STRMFAT?`, `DIR!`/`FILE`) și intrările (antetul `STRMFILE`, datele stocate ca atare); fiecare `Maps*.gtp` al instalării de test |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, limitele zonei de joc și `MapNW/NE/SE/SW`; fiecare din instalarea de test |
| Hărți de înălțimi (`height.dat`) | codecul de mai jos; fiecare sector al hărților decodat integral, folosind fluxul său de biți exact (cel mult umplutura de octeți rămasă), restul verificat după antet. Verificat bit cu bit față de fișierele necomprimate `distlod.raw` pe care jocul le livrează lângă `distlod.dat`, și față de harta de înălțimi LOD îndepărtată a unei hărți (corelație 0,999) |
| Înălțimi | metri = raw x heightMul / 256 - SeaLevel x heightMul. Marea unei hărți se decodează exact la înălțimea pe care o indică comentariile din hini-ul său; marginea alteia, la `bounds_level`-ul său |
| Plasare | biliniară între cele patru colțuri ale hini-ului, rândul 0 la nord, coloana 0 la vest. Verificată pe o hartă față de orașe, coaste și mări cunoscute (înălțimile orașelor la aproximativ 10 m de cele reale, marea sub nivelul mării). Colțurile formează un patrulater, nu proiecția proprie a jocului, deci de așteptat câteva sute de metri de eroare la mijlocul unei hărți mari. Hini-ul unei familii de hărți poartă colțurile altei hărți (ele acoperă o fracțiune din dimensiunea lor reală); aceasta se detectează, iar acea familie este plasată în schimb printr-o potrivire după repere: orașe și aerodromuri din bazele de date de locații ale jocului (`*.ldfbin`) față de pozițiile lor reale, eroare pătratică medie de câțiva kilometri (orașele față de aerodromurile care le poartă numele, iar coordonatele locurilor reale la aproximativ un kilometru); JSON-ul listează fiecare reper și reziduul său |
| Mască de apă (`water.wtr`: patru niveluri de piramidă de plăci, fiecare placă un tabel de blocuri de 400 m, fiecare bloc uscat, plin sau parțial apă cu forma sa într-un flux de biți) | containerul se citește pe fiecare hartă (niciun octet rămas pe fișierele decodate integral); forma din interiorul unui bloc parțial apă **nu este decodată**. Blocurile pline sunt apă; în blocurile parțial apă un eșantion este apă acolo unde harta de apă (`height_w.dat`, același codec ca harta de înălțimi) este deasupra solului sau, lângă un lac, unde solul nu este mai înalt decât lacul; blocurile de uscat sunt uscat. Asta elimină mlaștina pe care harta de apă singură o raportează drept apă. Râurile mai înguste decât grila de ieșire ies rupte în bucăți |
| Amprente de orașe (plasele de decal pe care le listează `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: plăci de 25,6 km de triunghiuri plate texturate) | citite pe fiecare hartă; se păstrează fețele a căror textură este un oraș, un sat sau teren industrial. Verificate față de orașele reale pe câteva hărți (un oraș pe ambele maluri ale unui râu, o confluență). Sunt amprente: jocul așază clădirile în timpul rulării, iar fișierele nu conțin clădiri |
| Aerodromuri, poduri, clădiri | **nu se citesc**: aerodromurile sunt obiecte de misiune, iar clădirile vin din plasarea proprie a jocului |
| Păduri (`forest_map.wtr`) | blocurile sale se citesc la fel, dar aproape fiecare bloc este „parțial pădure”, deci fără fluxul de biți nu există o mască de pădure utilizabilă; nu se desenează |
| Texturile terenului | nu se citesc |

## Codecul hărții de înălțimi {#the-heightmap-codec}

Stabilit doar din fișierele de date; nu a fost citit și nici dezasamblat niciun cod al jocului.
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

Sectoarele parțiale de la marginile din dreapta și de jos sunt completate și tăiate. Același codec
se aplică hărții de apă și hărții de înălțimi LOD îndepărtate.

## Potriviri după repere {#landmark-fits}

Acolo unde colțurile unei hărți nu pot fi folosite, `landmarks.py` potrivește o transformare afină de la
metrii jocului la pământ, prin cele mai mici pătrate: pozițiile din joc din fișierele proprii ale
utilizatorului (blocurile `Airfield` din misiuni, bazele de date ale carierei), pozițiile reale din tabele
cu coordonatele publicate ale locurilor, în cod. `georeference` din JSON poartă matricea, originea, fiecare
reper cu reziduul său și eroarea pătratică medie.
