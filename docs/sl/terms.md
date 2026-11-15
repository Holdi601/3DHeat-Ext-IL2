---
title: "Hitrost, testi, pogoji"
nav_order: 7
lang: sl
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Hitrost, testi, pogoji {#speed-tests-terms}

## Hitrost {#speed}

Dekodiranje je čisti Python, razen če je nameščen numba (`python -m pip install -e .[fast]`): srednje velik
zemljevid potrebuje približno 15 s brez nje in približno sekundo z njo; največji zemljevid, nekaj sto milijonov
vzorcev, približno 7 s z njo (prvi zagon tudi prevaja). Poraba pomnilnika ostane pri eni vrstici odsekov plus
izhodni mreži.

## Testi {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` v kodi zgradi arhive, višinske karte (kodirnik za zgoraj opisani kodek), datoteke `height.hini`
in arhive brez tabele datotek.

## Pogoji {#the-terms}

Licenčne pogodbe za IL-2 Sturmovik: Great Battles in IL-2 Series (1C Game Studios / 777 Studios) **nisem našel**:
ni je v namestitvi (katere `data/Licenses.txt` vsebuje samo licence tretjih oseb), ni je na spletnem mestu
založnika, stran Steam EULA pa se ni naložila. Preveri jo sam, preden se zaneseš nanjo. To orodje samo bere arhive
in jih nikoli ne spremeni. Ravni, ki jih zapiše, ostanejo na tvojem računalniku: **nikoli jih ne objavljaj**.
Nič tu ne prinaša podatkov igre, testi pa zgradijo vsako datoteko, ki jo berejo.

## Licenca {#licence}

MIT - glej [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Uporablja numpy
(BSD-3-Clause) in, neobvezno, numba (BSD-2-Clause). `heat3d_update` je skupni posodabljalnik orodij 3DHeat.
