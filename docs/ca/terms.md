---
title: Velocitat, proves, condicions
nav_order: 7
lang: ca
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Velocitat, proves, condicions {#speed-tests-terms}

## Velocitat {#speed}

La descodificació és Python pur tret que estigui instal·lat numba (`python -m pip install -e .[fast]`):
un mapa de mida mitjana triga uns 15 s sense ell i un segon aproximadament amb ell; el
mapa més gran, diversos centenars de milions de mostres, uns 7 s amb ell (la primera
execució també compila). La memòria es manté en una fila de sectors més la quadrícula de sortida.

## Proves {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` construeix en codi arxius, mapes d'alçades (un codificador del còdec de dalt),
fitxers `height.hini` i arxius sense taula de fitxers.

## Les condicions {#the-terms}

El contracte de llicència d'IL-2 Sturmovik: Great Battles i IL-2 Series (1C Game
Studios / 777 Studios) **no s'ha trobat**: ni a la instal·lació (el fitxer
`data/Licenses.txt` només conté llicències de tercers), ni al lloc de l'editor, i la pàgina
de l'EULA de Steam no es va carregar. Comprovi-la vostè mateix abans de confiar en això.
Aquesta eina només llegeix els arxius i mai els canvia. Els nivells que escriu es queden a la
vostra màquina: **no els publiqui mai**. Aquí no s'envia cap dada del joc, i les
proves construeixen tots els fitxers que llegeixen.

## Llicència {#licence}

MIT: vegi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Utilitza numpy (BSD-3-Clause) i, opcionalment,
numba (BSD-2-Clause). `heat3d_update` és l'actualitzador compartit de les eines de 3DHeat.
