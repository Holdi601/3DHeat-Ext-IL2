---
title: Velocitat, proves, condicions
nav_order: 7
lang: "ca"
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

Aquesta eina llegeix els arxius de la teva pròpia instal·lació d'IL-2 Sturmovik: Great Battles a l'ordinador i no els modifica mai.

No s'inclou ni es redistribueix res del joc: cap fitxer del joc, cap codi del joc, cap DLL; les proves generen elles mateixes cada fitxer que llegeixen. Els nivells que escriu es queden al teu equip.

3DHeat IL-2 no està afiliat a 1C Game Studios / 777 Studios ni té el seu aval. IL-2 Sturmovik i els noms i marques relacionats pertanyen als seus propietaris.

Titulars de drets: obriu una incidència a [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - responem ràpidament i retirem qualsevol cosa que se'ns demani.

## Llicència {#licence}

MIT: mira [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Utilitza numpy (BSD-3-Clause) i, opcionalment,
numba (BSD-2-Clause). `heat3d_update` és l'actualitzador compartit de les eines de 3DHeat.
