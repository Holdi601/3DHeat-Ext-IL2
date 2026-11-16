---
title: "Hitrost, testi, pogoji"
nav_order: 7
lang: "sl"
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

To orodje bere arhive tvoje lastne namestitve IL-2 Sturmovik: Great Battles na tvojem računalniku in jih nikoli ne spremeni.

Nič iz igre se ne priloži ali naprej razširja: nobenih datotek igre, nobene kode igre, nobenih DLL; testi sami zgradijo vsako datoteko, ki jo berejo. Ravni, ki jih zapiše, ostanejo na tvojem računalniku.

3DHeat IL-2 ni povezan s 1C Game Studios / 777 Studios niti ga ta ne podpira. IL-2 Sturmovik ter povezana imena in blagovne znamke pripadajo svojim lastnikom.

Imetniki pravic: odprite zahtevek na [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - odgovorimo hitro in na zahtevo odstranimo karkoli.

## Licenca {#licence}

MIT - glej [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Uporablja numpy
(BSD-3-Clause) in, neobvezno, numba (BSD-2-Clause). `heat3d_update` je skupni posodabljalnik orodij 3DHeat.
