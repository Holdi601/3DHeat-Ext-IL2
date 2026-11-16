---
title: "Sebesség, tesztek, feltételek"
nav_order: 7
lang: "hu"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Sebesség, tesztek, feltételek {#speed-tests-terms}

## Sebesség {#speed}

A dekódolás tiszta Python, hacsak nincs telepítve a numba (`python -m pip install -e .[fast]`):
egy közepes térkép numba nélkül körülbelül 15 s, numba-val körülbelül egy másodperc; a legnagyobb
térkép, több száz millió mintával, numba-val körülbelül 7 s (az első futás le is fordítja). A memória
egy szektorsornál és a kimeneti rácsnál marad.

## Tesztek {#tests}

```bash
python -m pytest -q
```

A `tests/synth.py` kódban építi meg az archívumokat, a magassági térképeket (az általunk fent leírt
kódoló kódolóját), a `height.hini` fájlokat, és a fájltáblázat nélküli archívumokat.

## A feltételek {#the-terms}

Ez az eszköz a saját IL-2 Sturmovik: Great Battles-telepítésed archívumait olvassa a számítógépeden, és soha nem módosítja őket.

A játékból semmi nem kerül kiadásra vagy továbbterjesztésre: sem játékfájl, sem játékkód, sem DLL; a tesztek maguk állítják elő minden fájlt, amelyet olvasnak. Az általa írt pályák a gépeden maradnak.

A(z) 3DHeat IL-2 nem áll kapcsolatban a(z) 1C Game Studios / 777 Studios céggel, és az nem is támogatja. A(z) IL-2 Sturmovik és a kapcsolódó nevek és védjegyek a tulajdonosaikat illetik.

Jogtulajdonosok: nyissatok bejelentést itt: [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - gyorsan válaszolunk, és kérésre bármit eltávolítunk.

## Licenc {#licence}

MIT – lásd a [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE) fájlt. Használja a numpy-t
(BSD-3-Clause), és opcionálisan a numba-t (BSD-2-Clause). A `heat3d_update` a 3DHeat eszközök közös frissítője.
