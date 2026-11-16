---
title: "Hraði, prófanir, skilmálar"
nav_order: 7
lang: "is"
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

Þetta verkfæri les skjalasöfnin í þinni eigin uppsetningu á IL-2 Sturmovik: Great Battles á tölvunni þinni og breytir þeim aldrei.

Ekkert úr leiknum fylgir með eða er dreift áfram: engar leikjaskrár, enginn leikjakóði, engin DLL-söfn; prófanirnar búa sjálfar til hverja skrá sem þær lesa. Borðin sem það skrifar verða eftir á tölvunni þinni.

3DHeat IL-2 tengist ekki 1C Game Studios / 777 Studios og er ekki stutt af þeim. IL-2 Sturmovik og tengd heiti og vörumerki tilheyra eigendum sínum.

Rétthafar: stofnið verkbeiðni á [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - við svörum fljótt og fjarlægjum hvað sem er að beiðni.

## Leyfi {#licence}

MIT - sjá [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Notar numpy (BSD-3-Clause) og, valkvætt,
numba (BSD-2-Clause). `heat3d_update` er sameiginlegur uppfærsluhugbúnaður 3DHeat-verkfæranna.
