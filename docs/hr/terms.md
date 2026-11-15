---
title: Brzina, testovi, uvjeti
nav_order: 7
lang: "hr"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Brzina, testovi, uvjeti {#speed-tests-terms}

## Brzina {#speed}

Dekodiranje je čisti Python osim ako nije instalirana numba (`python -m pip install -e .[fast]`):
srednje velika karta traje oko 15 s bez nje i oko sekunde s njom; najveća karta, nekoliko stotina milijuna uzoraka, oko 7 s s njom (prvo pokretanje također prevodi kod). Memorija ostaje na jednom retku sektora plus izlaznoj mreži.

## Testovi {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` u kodu gradi arhive, visinske mape (koder za kodek iznad), datoteke `height.hini` i arhive bez tablice datoteka.

## Uvjeti {#the-terms}

Ugovor o licenci za IL-2 Sturmovik: Great Battles i IL-2 Series (1C Game
Studios / 777 Studios) **nije pronađen**: nije u instalaciji (čiji
`data/Licenses.txt` sadrži samo licence trećih strana), nije na stranici izdavača, a
Steam EULA stranica se nije učitala. Provjerite ga sami prije nego što se oslonite na ovo.
Ovaj alat samo čita arhive i nikad ih ne mijenja. Razine koje piše ostaju na
vašem računalu: **nikad ih ne objavljujte**. Ovdje se ne isporučuju nikakvi podaci igre, a
testovi grade svaku datoteku koju čitaju.

## Licenca {#licence}

MIT - vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Koristi numpy (BSD-3-Clause) i, neobavezno,
numba (BSD-2-Clause). `heat3d_update` je zajednički ažurirač 3DHeat alata.
