---
title: "Shpejtësia, testet, kushtet"
nav_order: 7
lang: "sq"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Shpejtësia, testet, kushtet {#speed-tests-terms}

## Shpejtësia {#speed}

Dekodimi është Python i pastër nëse numba nuk është instaluar (`python -m pip install -e .[fast]`):
një hartë mesatare zgjat rreth 15 s pa të dhe rreth një sekondë me të; harta më e
madhe, disa qindra milionë mostra, rreth 7 s me të (ekzekutimi i parë kompajlon
edhe). Memoria mbetet në një rresht sektorësh plus rrjetën e daljes.

## Testet {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` ndërton arkiva, heightmap-e (një koduesh për kodekun më sipër),
skedarë `height.hini` dhe arkiva pa tabelë skedarësh në kod.

## Kushtet {#the-terms}

Ky mjet lexon arkivat e instalimit tënd të IL-2 Sturmovik: Great Battles në kompjuterin tënd dhe nuk i ndryshon kurrë.

Asgjë nga loja nuk shpërndahet as nuk rishpërndahet: asnjë skedar loje, asnjë kod loje, asnjë DLL; testet e ndërtojnë vetë çdo skedar që lexojnë. Nivelet që shkruan mbeten në kompjuterin tënd.

3DHeat IL-2 nuk është i lidhur me 1C Game Studios / 777 Studios dhe nuk miratohet prej saj. IL-2 Sturmovik dhe emrat e markat tregtare përkatëse u përkasin pronarëve të tyre.

Mbajtës të drejtash: hapni një çështje në [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - përgjigjemi shpejt dhe heqim çdo gjë me kërkesë.

## Licenca {#licence}

MIT - shih [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Përdor numpy (BSD-3-Clause) dhe, opsionalisht,
numba (BSD-2-Clause). `heat3d_update` është përditësuesi i përbashkët i mjeteve 3DHeat.
