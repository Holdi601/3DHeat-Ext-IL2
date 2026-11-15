---
title: "Velocità, test, condizioni"
nav_order: 7
lang: it
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Velocità, test, condizioni {#speed-tests-terms}

## Velocità {#speed}

La decodifica è in puro Python, a meno che non sia installato numba (`python -m pip install -e .[fast]`):
una mappa di medie dimensioni richiede circa 15 s senza, e circa un secondo con esso; la mappa più
grande, diverse centinaia di milioni di campioni, circa 7 s con esso (la prima esecuzione compila anche
il codice). La memoria resta a una riga di settori più la griglia di output.

## Test {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` costruisce in codice archivi, mappe delle altezze (un codificatore per il codec qui
sopra), file `height.hini` e archivi senza tabella dei file.

## Le condizioni {#the-terms}

Il contratto di licenza di IL-2 Sturmovik: Great Battles e IL-2 Series (1C Game Studios / 777 Studios)
**non è stato trovato**: né nell'installazione (la cui `data/Licenses.txt` contiene solo licenze di
terze parti), né sul sito dell'editore, e la pagina dell'EULA di Steam non si è caricata. Verificalo tu
prima di fare affidamento su questo strumento. Questo strumento legge soltanto gli archivi e non li
modifica mai. I livelli che scrive restano sul tuo computer: **non pubblicarli mai**. Nulla qui distribuisce
dati di gioco, e i test costruiscono ogni file che leggono.

## Licenza {#licence}

MIT - vedi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Usa numpy
(BSD-3-Clause) e, facoltativamente, numba (BSD-2-Clause). `heat3d_update` è l'aggiornatore condiviso
degli strumenti 3DHeat.
