---
title: Veloċità, testijiet, termini
nav_order: 7
lang: "mt"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Veloċità, testijiet, termini {#speed-tests-terms}

## Veloċità {#speed}

Id-dekodifikar huwa Python pur sakemm numba ma jkunx installat (`python -m pip install -e .[fast]`):
mappa ta' daqs medju tieħu madwar 15 s mingħajru u madwar sekonda miegħu; l-
akbar mappa, diversi mijiet ta' miljuni ta' kampjuni, madwar 7 s miegħu (l-ewwel
użu jikkompila wkoll). Il-memorja tibqa' fuq ringiela waħda ta' setturi flimkien mal-grilja tal-output.

## Testijiet {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` jibni arkivji, heightmaps (encoder għall-codec ta' hawn fuq),
fajls `height.hini` u arkivji mingħajr tabella tal-fajls fil-kodiċi.

## It-termini {#the-terms}

Il-ftehim tal-liċenzja ta' IL-2 Sturmovik: Great Battles u IL-2 Series (1C Game
Studios / 777 Studios) **ma nstabx**: mhux fl-installazzjoni (li `data/Licenses.txt`
tagħha fih biss liċenzji ta' terzi), mhux fuq is-sit tal-pubblikatur,
u l-paġna tal-EULA ta' Steam ma tgħabbietx. Iċċekkja int qabel ma tafda fuq dan.
Din l-għodda taqra biss l-arkivji u qatt ma tibdilhom. Il-livelli li tikteb jibqgħu
fuq il-magna tiegħek: **qatt ma tippubblikahom**. Xejn hawn ma jaqsam dejta tal-logħba, u
t-testijiet jibnu kull fajl li jaqraw.

## Liċenzja {#licence}

MIT - ara [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Juża numpy (BSD-3-Clause) u, b'mod fakultattiv,
numba (BSD-2-Clause). `heat3d_update` huwa l-updater maqsum tal-għodod ta' 3DHeat.
