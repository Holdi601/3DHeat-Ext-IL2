---
title: "Hraði, prófanir, skilmálar"
nav_order: 7
lang: is
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Hraði, prófanir, skilmálar {#speed-tests-terms}

## Hraði {#speed}

Afkóðun er hreint Python nema numba sé uppsett (`python -m pip install -e .[fast]`):
meðalstórt kort tekur um 15 s án þess og um sekúndu með því; stærsta
kortið, nokkur hundruð milljón sýni, um 7 s með því (fyrsta
keyrslan þýðir líka). Minnið helst við eina röð geira auk úttaksnetsins.

## Prófanir {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` smíðar skjalasöfn, hæðarkort (kóðara fyrir málið hér að ofan),
`height.hini` skrár og skjalasöfn án skráartöflu í kóða.

## Skilmálarnir {#the-terms}

Leyfissamningur IL-2 Sturmovik: Great Battles og IL-2 Series (1C Game
Studios / 777 Studios) **fannst ekki**: ekki í uppsetningunni (þar sem
`data/Licenses.txt` geymir aðeins leyfi þriðja aðila), ekki á vef útgefandans,
og Steam EULA síðan hlóðst ekki. Athugaðu hann sjálf/ur áður en þú treystir á þetta.
Þetta tól les aðeins skjalasöfnin og breytir þeim aldrei. Borðin sem það skrifar haldast
á þinni vél: **birtu þau aldrei**. Ekkert hér fylgir með neinum leikjagögnum, og
prófanirnar smíða hverja skrá sem þær lesa.

## Leyfi {#licence}

MIT - sjá [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Notar numpy (BSD-3-Clause) og, valkvætt,
numba (BSD-2-Clause). `heat3d_update` er sameiginlegur uppfærsluhugbúnaður 3DHeat-tólanna.
