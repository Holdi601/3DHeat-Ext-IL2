---
title: "Nopeus, testit, ehdot"
nav_order: 7
lang: fi
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Nopeus, testit, ehdot {#speed-tests-terms}

## Nopeus {#speed}

Dekoodaus on puhdasta Pythonia, ellei numba ole asennettu (`python -m pip install -e .[fast]`):
keskikokoinen kartta vie ilman sitä noin 15 s ja sen kanssa noin sekunnin; suurin kartta, useita satoja
miljoonia näytteitä, noin 7 s sen kanssa (ensimmäinen ajo myös kääntää koodin). Muisti pysyy yhdessä
sektoririvissä ja tulostusruudukossa.

## Testit {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` rakentaa koodissa arkistot, korkeuskartat (yllä olevan koodekin kooderi),
`height.hini`-tiedostot ja arkistot ilman tiedostotaulukkoa.

## Ehdot {#the-terms}

IL-2 Sturmovik: Great Battles -pelin ja IL-2 Series -pelin (1C Game Studios / 777 Studios) lisenssisopimusta
**ei löytynyt**: ei asennuksesta (jonka `data/Licenses.txt` kantaa vain kolmansien osapuolten lisenssejä),
ei julkaisijan sivulta, eikä Steamin EULA-sivu latautunut. Tarkista se itse ennen kuin luotat tähän.
Tämä työkalu vain lukee arkistot eikä koskaan muuta niitä. Kentät, joita se kirjoittaa, pysyvät
koneellasi: **älä koskaan julkaise niitä**. Mikään tässä ei toimita pelin dataa, ja testit rakentavat
jokaisen tiedoston, jonka ne lukevat.

## Lisenssi {#licence}

MIT – katso [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Käyttää numpy-kirjastoa
(BSD-3-Clause) ja valinnaisesti numba-kirjastoa (BSD-2-Clause). `heat3d_update` on 3DHeat-työkalujen yhteinen päivitin.
