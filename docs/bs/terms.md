---
title: "Brzina, testovi, uvjeti"
nav_order: 7
lang: "bs"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Brzina, testovi, uvjeti {#speed-tests-terms}

## Brzina {#speed}

Dekodiranje je čisti Python osim ako je instaliran numba (`python -m pip install -e .[fast]`):
mapa srednje veličine traje oko 15 s bez njega, a oko sekundu s njim; najveća
mapa, nekoliko stotina miliona uzoraka, oko 7 s s njim (prvo
pokretanje i kompilira). Memorija ostaje na jednom redu sektora plus izlazna mreža.

## Testovi {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` u kodu gradi arhive, visinske mape (koder za gornji kodek),
datoteke `height.hini` i arhive bez tabele datoteka.

## Uvjeti {#the-terms}

Ugovor o licenci za IL-2 Sturmovik: Great Battles i IL-2 Series (1C Game
Studios / 777 Studios) **nije pronađen**: ni u instalaciji (čiji
`data/Licenses.txt` drži samo licence trećih strana), ni na stranici izdavača,
a stranica Steam EULA se nije učitala. Provjeri ga sam prije nego se osloniš na ovo.
Ovaj alat samo čita arhive i nikad ih ne mijenja. Nivoi koje piše ostaju
na tvom računaru: **nikad ih ne objavljuj**. Ništa ovdje ne isporučuje podatke igre, a
testovi grade svaku datoteku koju čitaju.

## Licenca {#licence}

MIT - vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Koristi numpy (BSD-3-Clause) i, neobavezno,
numba (BSD-2-Clause). `heat3d_update` je zajednički alat za ažuriranje 3DHeat alata.
