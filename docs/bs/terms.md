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

Ovaj alat čita arhive tvoje vlastite instalacije IL-2 Sturmovik: Great Battles na tvom računaru i nikad ih ne mijenja.

Ništa iz igre se ne isporučuje niti dalje distribuira: nema datoteka igre, nema koda igre, nema DLL-ova; testovi sami prave svaku datoteku koju čitaju. Nivoi koje zapiše ostaju na tvom računaru.

3DHeat IL-2 nije povezan s 1C Game Studios / 777 Studios niti ga 1C Game Studios / 777 Studios podržava. IL-2 Sturmovik i povezani nazivi i zaštitni znakovi pripadaju svojim vlasnicima.

Nosioci prava: otvorite prijavu na [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - odgovaramo brzo i na zahtjev uklanjamo bilo šta.

## Licenca {#licence}

MIT - vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Koristi numpy (BSD-3-Clause) i, neobavezno,
numba (BSD-2-Clause). `heat3d_update` je zajednički alat za ažuriranje 3DHeat alata.
