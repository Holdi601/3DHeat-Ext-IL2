---
title: "Velocità, test, condizioni"
nav_order: 7
lang: "it"
source: terms.md
source_hash: "3baa9f57ade6"
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

Questo strumento legge gli archivi della tua installazione di IL-2 Sturmovik: Great Battles sul tuo computer e non li modifica mai.

Nulla del gioco viene distribuito o ridistribuito: nessun file del gioco, nessun codice del gioco, nessuna DLL; i test costruiscono da sé ogni file che leggono. I livelli che scrive restano sul tuo computer.

3DHeat IL-2 non è affiliato a 1C Game Studios / 777 Studios né approvato da esso. IL-2 Sturmovik e i nomi e marchi correlati appartengono ai rispettivi proprietari.

Titolari dei diritti: aprite una segnalazione su [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - rispondiamo in fretta e rimuoviamo qualsiasi cosa su richiesta.

## Licenza {#licence}

MIT - vedi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Usa numpy
(BSD-3-Clause) e, facoltativamente, numba (BSD-2-Clause). `heat3d_ext_il2.update` è l'aggiornatore condiviso
degli strumenti 3DHeat.
