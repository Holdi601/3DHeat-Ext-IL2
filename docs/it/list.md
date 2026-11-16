---
title: "Trovare le mappe: list"
nav_order: 2
lang: "it"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Trovare le mappe: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game CARTELLA ...]
python -m heat3d_ext_il2 list ...          lo stesso, senza installare
```

Non hai mai usato la riga di comando? Leggi prima [Prima di iniziare](before-you-start.md).

1. Installa una volta sola: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, apri un terminale
   in quella cartella ed esegui `python -m pip install -e .` (Python 3.10 o successivo; porta con sé
   numpy; `python -m pip install -e .[fast]` aggiunge numba).
2. Esegui `heat3d-il2-level list`.
3. Ogni mappa stampa una riga, separata da tabulazioni: il suo nome (il nome che accetta `extract`), il
   gioco (`Great Battles`, oppure `Korea` per [il secondo gioco](archives-without-table.md)), la mappa
   delle altezze che legge, e dove si trova sulla Terra - il suo riquadro di latitudine/longitudine
   dagli angoli della mappa, oppure l'adattamento sui punti di riferimento che la colloca, oppure "not
   placed on the earth" (non collocata sulla Terra). L'ultima riga (sull'errore standard) conta le
   mappe e indica le installazioni.

![list su un'installazione sintetica](../assets/img/list.svg)

L'immagine è un'esecuzione su un'installazione creata dai test
(`tests/synth.py`), non sul gioco.

## Dove vengono trovate le installazioni {#where-the-installs-are-found}

Tramite Steam; altrimenti `--game <cartella>` (ripetibile, una per installazione) oppure la variabile
d'ambiente `HEAT3D_IL2_GAME`. Un'installazione è una cartella la cui sottocartella `data` contiene
archivi `Maps*.gtp`.

| Opzione | Cosa fa |
|---|---|
| `--game CARTELLA` | una cartella di IL-2; ripetila per più installazioni |

Stato di uscita: 0 fatto, 2 nessuna installazione trovata.
