---
title: Fart, tester, vilkår
nav_order: 7
lang: no
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Fart, tester, vilkår {#speed-tests-terms}

## Fart {#speed}

Dekoding er ren Python med mindre numba er installert (`python -m pip install -e .[fast]`):
et middels stort kart tar omtrent 15 s uten den og omtrent et sekund med den; det
største kartet, flere hundre millioner prøver, omtrent 7 s med den (den første
kjøringen kompilerer også). Minnet holder seg til én rad med sektorer pluss utgangsrutenettet.

## Tester {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` bygger arkiver, høydekart (en koder for kodeken over),
`height.hini`-filer og arkiver uten filtabell i kode.

## Vilkårene {#the-terms}

Lisensavtalen for IL-2 Sturmovik: Great Battles og IL-2 Series (1C Game
Studios / 777 Studios) ble **ikke funnet**: ikke i installasjonen (hvis
`data/Licenses.txt` bare holder tredjepartslisenser), ikke på utgiverens nettsted,
og Steam-EULA-siden lastet ikke. Sjekk den selv før du stoler på dette.
Dette verktøyet leser bare arkivene og endrer dem aldri. Nivåene det skriver blir
på din egen maskin: **publiser dem aldri**. Ingenting her leverer spilldata, og
testene bygger alle filene de leser.

## Lisens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Bruker numpy (BSD-3-Clause) og, valgfritt,
numba (BSD-2-Clause). `heat3d_update` er 3DHeat-verktøyenes felles oppdaterer.
