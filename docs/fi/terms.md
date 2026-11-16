---
title: "Nopeus, testit, ehdot"
nav_order: 7
lang: "fi"
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

Tämä työkalu lukee oman IL-2 Sturmovik: Great Battles -asennuksesi arkistoja tietokoneellasi eikä koskaan muuta niitä.

Pelistä ei toimiteta eikä jaeta mitään: ei pelitiedostoja, ei pelin koodia, ei DLL-tiedostoja; testit rakentavat itse jokaisen lukemansa tiedoston. Sen kirjoittamat tasot pysyvät koneellasi.

3DHeat IL-2 ei ole sidoksissa yhtiöön 1C Game Studios / 777 Studios, eikä se ole sen hyväksymä. IL-2 Sturmovik ja siihen liittyvät nimet ja tavaramerkit kuuluvat omistajilleen.

Oikeudenhaltijat: avatkaa issue osoitteessa [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - vastaamme nopeasti ja poistamme pyynnöstä mitä tahansa.

## Lisenssi {#licence}

MIT – katso [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Käyttää numpy-kirjastoa
(BSD-3-Clause) ja valinnaisesti numba-kirjastoa (BSD-2-Clause). `heat3d_update` on 3DHeat-työkalujen yhteinen päivitin.
