---
title: "Rýchlosť, testy, podmienky"
nav_order: 7
lang: "sk"
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

Tento nástroj číta archívy vašej vlastnej inštalácie IL-2 Sturmovik: Great Battles na vašom počítači a nikdy ich nemení.

Nič z hry sa nedodáva ani ďalej nešíri: žiadne súbory hry, žiadny kód hry, žiadne knižnice DLL; testy si každý súbor, ktorý čítajú, vytvoria samy. Úrovne, ktoré zapíše, zostávajú na vašom počítači.

3DHeat IL-2 nie je pridružený k 1C Game Studios / 777 Studios ani ním schválený. IL-2 Sturmovik a súvisiace názvy a ochranné známky patria ich vlastníkom.

Držitelia práv: založte hlásenie na [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - odpovedáme rýchlo a na požiadanie čokoľvek odstránime.

## Licencia {#licence}

MIT – pozri [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Používa numpy (BSD-3-Clause) a voliteľne
numba (BSD-2-Clause). `heat3d_update` je spoločný aktualizátor nástrojov 3DHeat.
