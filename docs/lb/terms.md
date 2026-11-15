---
title: "Geschwindegkeet, Tester, Bedingungen"
nav_order: 7
lang: "lb"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Geschwindegkeet, Tester, Bedingungen {#speed-tests-terms}

## Geschwindegkeet {#speed}

D'Dekodéieren ass reng Python, ausser numba ass installéiert (`python -m pip install -e .[fast]`):
eng mëttelgrouss Map brauch ongeféier 15 s ouni et an ongeféier eng Sekonn domat; déi
gréisst Map, e puer honnert Millioune Echantillone, ongeféier 7 s domat (den éischte
Lauf kompiléiert och). D'Gedächtnis bleift bei enger Rei vu Sektoren plus dem Ausgabegitter.

## Tester {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` baut Archiver, Heightmaps (en Encoder fir de Codec hei uewen),
`height.hini`-Dateien an Archiver ouni Dateitabell am Code.

## D'Bedingungen {#the-terms}

D'Lizenzofkommes vun IL-2 Sturmovik: Great Battles an IL-2 Series (1C Game
Studios / 777 Studios) gouf **net fonnt**: net an der Installatioun (deem säin
`data/Licenses.txt` nëmmen Drëttlizenze hält), net um Site vum Verleeër,
an d'Steam-EULA-Säit huet sech net gelueden. Préift et selwer, ier Dir Iech drop verléisst.
Dëst Tool liest nëmmen d'Archiver a veränneert se ni. D'Levelen, déi et schreift, bleiwen
op Ärem Rechner: **ni publizéieren**. Hei gëtt keng Spilldaten matgeliwwert, an d'
Tester bauen all Datei, déi si liesen.

## Lizenz {#licence}

MIT - kuckt [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Benotzt numpy (BSD-3-Clause) an, optionell,
numba (BSD-2-Clause). `heat3d_update` ass dem Updater, deen d'3DHeat-Tools deelen.
