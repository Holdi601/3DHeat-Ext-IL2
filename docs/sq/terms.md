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

Marrëveshja e licencës së IL-2 Sturmovik: Great Battles dhe IL-2 Series (1C Game
Studios / 777 Studios) **nuk u gjet**: jo në instalim (`data/Licenses.txt` e të cilit
mban vetëm licenca të palëve të treta), jo në faqen e botuesit, dhe faqja e EULA të Steam
nuk u ngarkua. Kontrolloje vetë para se të mbështetesh te kjo.
Ky mjet vetëm i lexon arkivat dhe kurrë nuk i ndryshon. Nivelet që shkruan mbeten
në kompjuterin tënd: **mos i publiko kurrë**. Asgjë këtu nuk shpërndan të dhëna loje, dhe
testet ndërtojnë çdo skedar që lexojnë.

## Licenca {#licence}

MIT - shih [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Përdor numpy (BSD-3-Clause) dhe, opsionalisht,
numba (BSD-2-Clause). `heat3d_update` është përditësuesi i përbashkët i mjeteve 3DHeat.
