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

Dëst Tool liest d'Archiver vun denger eegener Installatioun vun IL-2 Sturmovik: Great Battles op dengem Computer an ännert se ni.

Näischt aus dem Spill gëtt matgeliwwert oder weiderginn: keng Spilldateien, kee Spillcode, keng DLLen; d'Tester bauen all Datei, déi se liesen, selwer. D'Levelen, déi et schreift, bleiwen op dengem Rechner.

3DHeat IL-2 ass net mat 1C Game Studios / 777 Studios verbonnen an net vun hinne gutt geheescht. IL-2 Sturmovik an déi verbonnen Nimm a Marken gehéieren hiren Eegentümer.

Rechteinhaber: maacht en Issue op [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) op - mir äntweren séier an huelen op Ufro alles erof.

## Lizenz {#licence}

MIT - kuckt [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Benotzt numpy (BSD-3-Clause) an, optionell,
numba (BSD-2-Clause). `heat3d_update` ass dem Updater, deen d'3DHeat-Tools deelen.
