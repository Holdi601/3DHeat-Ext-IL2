---
title: "Rýchlosť, testy, podmienky"
nav_order: 7
lang: sk
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Rýchlosť, testy, podmienky {#speed-tests-terms}

## Rýchlosť {#speed}

Dekódovanie je čistý Python, pokiaľ nie je nainštalované numba (`python -m pip install -e .[fast]`):
stredne veľká mapa trvá bez neho asi 15 s a s ním asi sekundu; najväčšia mapa, niekoľko stoviek miliónov vzoriek, asi 7 s s ním (prvý beh sa tiež kompiluje). Pamäť zostáva na jeden riadok sektorov plus výstupnú mriežku.

## Testy {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` vytvára v kóde archívy, výškové mapy (kodér pre kodek vyššie),
súbory `height.hini` a archívy bez tabuľky súborov.

## Podmienky {#the-terms}

Licenčná zmluva hry IL-2 Sturmovik: Great Battles a IL-2 Series (1C Game
Studios / 777 Studios) sa **nenašla**: nie v inštalácii (jej
`data/Licenses.txt` obsahuje len licencie tretích strán), nie na stránke vydavateľa
a stránka EULA na Steame sa nenačítala. Pred tým, ako sa na to spoľahnete, ju overte sami.
Tento nástroj iba číta archívy a nikdy ich nemení. Úrovne, ktoré zapisuje, ostávajú
na vašom počítači: **nikdy ich nezverejňujte**. Nič tu neobsahuje herné dáta a testy vytvárajú každý súbor, ktorý čítajú.

## Licencia {#licence}

MIT – pozri [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Používa numpy (BSD-3-Clause) a voliteľne
numba (BSD-2-Clause). `heat3d_update` je spoločný aktualizátor nástrojov 3DHeat.
