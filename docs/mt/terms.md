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

Din l-għodda taqra l-arkivji tal-installazzjoni tiegħek ta' IL-2 Sturmovik: Great Battles fuq il-kompjuter tiegħek u qatt ma tibdilhom.

Xejn mil-logħba ma jintbagħat jew jitqassam mill-ġdid: l-ebda fajl tal-logħba, l-ebda kodiċi tal-logħba, l-ebda DLL; it-testijiet jibnu huma stess kull fajl li jaqraw. Il-livelli li jikteb jibqgħu fuq il-magna tiegħek.

3DHeat IL-2 mhuwiex affiljat ma' 1C Game Studios / 777 Studios u mhuwiex approvat minnhom. IL-2 Sturmovik u l-ismijiet u t-trademarks relatati jappartjenu lis-sidien tagħhom.

Detenturi tad-drittijiet: iftħu kwistjoni fuq [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - inwieġbu malajr u nneħħu kull ħaġa fuq talba.

## Liċenzja {#licence}

MIT - ara [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Juża numpy (BSD-3-Clause) u, b'mod fakultattiv,
numba (BSD-2-Clause). `heat3d_update` huwa l-updater maqsum tal-għodod ta' 3DHeat.
