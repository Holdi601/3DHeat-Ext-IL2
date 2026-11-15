---
title: "Costruire i livelli: extract"
nav_order: 3
lang: it
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Costruire i livelli: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<mappa> ... | --all) -o <cartella> [--game CARTELLA ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Passo per passo {#step-by-step}

Non hai mai usato la riga di comando? Leggi prima [Prima di iniziare](before-you-start.md).

1. Trova il nome della mappa con [`list`](list.md).
2. Esegui `heat3d-il2-level extract <mappa> -o levels`. I nomi possono usare caratteri jolly, tra
   virgolette (`"<famiglia>_*"`); `--all` prende ogni mappa.
3. Per mettere una registrazione sul livello senza alcun passaggio di posizionamento, indica la sua
   origine: `--origin <lat> <lon>` con il valore `geo` della registrazione (il punto di riferimento
   della sua sessione). Senza, il centro della mappa è l'origine, e il `geo` del `.json` dice quale.
4. Il comando stampa una riga per mappa man mano che la decodifica, poi
   `ok <glb> <triangoli> (<frame> frame)` oppure `failed <mappa>: <motivo>`.
5. Carica `<cartella>/<mappa>/<mappa>.glb` nel pannello Sfondo / livello del visualizzatore.

![extract su un'installazione sintetica](../assets/img/extract.svg)

In metri del gioco, senza l'acqua:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Una seconda esecuzione sulle mappe già scritte:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opzioni {#options}

| Opzione | Predefinito | Cosa fa |
|---|---|---|
| `maps` | - | nomi delle mappe come li stampa `list`; sono ammessi i caratteri jolly |
| `--all` | disattivata | ogni mappa; le stagioni che condividono una mappa delle altezze e una mappa dell'acqua vengono scritte una volta sola |
| `-o`, `--out` | obbligatoria | la cartella di output; ogni mappa va in `<out>/<mappa>/` |
| `--game CARTELLA` | trovata | una cartella di IL-2 (ripetibile) |
| `--max-grid N` | `1024` | campioni della mappa delle altezze per lato, al massimo (1024: circa 2 milioni di triangoli); la mappa viene campionata ogni *k* campioni per entrarci |
| `--frame` `enu` o `game` | `enu` | `enu`: metri a est, altitudine, nord rispetto a `--origin`, come le tabelle Tacview del Watcher; `game`: le metri del gioco stesso (x nord, y altezza, z est). Una mappa che non può essere collocata sulla Terra viene scritta in `game` qualunque sia la richiesta |
| `--origin LAT LON` | il centro della mappa | l'origine del sistema `enu` (il `geo` di una registrazione) |
| `--no-water` | disattivata | lascia fuori l'acqua |
| `--no-towns` | disattivata | lascia fuori le impronte delle città |
| `--skip-existing` | disattivata | lascia le mappe di cui esiste già il `.glb` |

Ogni opzione, come la stampa il programma: [Riferimento dei comandi](../cli-reference.md).

Imposta `HEAT3D_DEBUG` per stampare il traceback completo di una mappa fallita. Il `.glb` viene
scritto in `<mappa>.glb.part` e rinominato quando è completo.

Stato di uscita: 0 ogni mappa scritta; 1 almeno una fallita (le altre vengono scritte comunque); 2
nessuna installazione o nessuna mappa corrispondente.

## Esempi {#examples}

```bash
heat3d-il2-level extract <mappa> -o levels                         # una mappa, sistema enu intorno al suo centro
heat3d-il2-level extract <mappa> --origin <lat> <lon> -o levels    # nella mappa piatta di una registrazione con quel geo
heat3d-il2-level extract "<famiglia>_*" --max-grid 2048 -o levels  # più fine, più mappe
heat3d-il2-level extract --all --skip-existing -o levels           # ogni mappa, solo le nuove
heat3d-il2-level extract <mappa> --frame game -o levels            # le metri del gioco, come le hanno i file di missione
```

Cosa c'è nei file: [I file del livello e i sistemi di riferimento](output.md).
