---
title: Fart, tester, vilkår
nav_order: 7
lang: "no"
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

Dette verktøyet leser arkivene i din egen installasjon av IL-2 Sturmovik: Great Battles på datamaskinen din og endrer dem aldri.

Ingenting fra spillet følger med eller videredistribueres: ingen spillfiler, ingen spillkode, ingen DLL-er; testene bygger selv hver fil de leser. Banene den skriver, blir værende på maskinen din.

3DHeat IL-2 er ikke tilknyttet eller godkjent av 1C Game Studios / 777 Studios. IL-2 Sturmovik og tilhørende navn og varemerker tilhører sine eiere.

Rettighetshavere: opprett en sak på [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - vi svarer raskt og fjerner hva som helst på forespørsel.

## Lisens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Bruker numpy (BSD-3-Clause) og, valgfritt,
numba (BSD-2-Clause). `heat3d_update` er 3DHeat-verktøyenes felles oppdaterer.
