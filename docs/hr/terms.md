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

Ovaj alat čita arhive tvoje vlastite instalacije IL-2 Sturmovik: Great Battles na tvom računalu i nikad ih ne mijenja.

Ništa iz igre ne isporučuje se niti dalje distribuira: nema datoteka igre, nema koda igre, nema DLL-ova; testovi sami grade svaku datoteku koju čitaju. Razine koje zapiše ostaju na tvom računalu.

3DHeat IL-2 nije povezan s 1C Game Studios / 777 Studios niti ga 1C Game Studios / 777 Studios podržava. IL-2 Sturmovik i povezani nazivi i zaštitni znakovi pripadaju svojim vlasnicima.

Nositelji prava: otvorite prijavu na [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - odgovaramo brzo i na zahtjev uklanjamo bilo što.

## Licenca {#licence}

MIT - vidi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Koristi numpy (BSD-3-Clause) i, neobavezno,
numba (BSD-2-Clause). `heat3d_update` je zajednički ažurirač 3DHeat alata.
