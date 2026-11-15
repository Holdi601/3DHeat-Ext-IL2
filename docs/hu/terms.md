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

Az IL-2 Sturmovik: Great Battles és az IL-2 Series (1C Game Studios / 777 Studios) licencszerződését
**nem találtuk meg**: nincs a telepítésben (amelynek `data/Licenses.txt` fájlja csak harmadik féltől
származó licenceket tartalmaz), nincs a kiadó oldalán, és a Steam EULA oldala nem töltődött be. Ellenőrizd
te, mielőtt erre támaszkodnál. Ez az eszköz csak olvassa az archívumokat, és sosem módosítja őket. Az általad
írt pályák a te gépeden maradnak: **soha ne tedd közzé őket**. Ez a csomag nem szállít játékadatot, a tesztek
pedig minden olvasott fájlt maguk építenek.

## Licenc {#licence}

MIT – lásd a [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE) fájlt. Használja a numpy-t
(BSD-3-Clause), és opcionálisan a numba-t (BSD-2-Clause). A `heat3d_update` a 3DHeat eszközök közös frissítője.
