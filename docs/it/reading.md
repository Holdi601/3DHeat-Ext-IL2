---
title: Come vengono letti i file
nav_order: 5
lang: "it"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Come vengono letti i file {#how-the-files-are-read}

| Parte | Stato |
|---|---|
| Archivi (`data/*.gtp`, Great Battles) | la tabella dei file (record `S16R`, `STRMFAT?`, `DIR!`/`FILE`) e le voci (intestazione `STRMFILE`, dati memorizzati così come sono); ogni `Maps*.gtp` dell'installazione di prova |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, i limiti di gioco e `MapNW/NE/SE/SW`; tutti quelli dell'installazione di prova |
| Mappe delle altezze (`height.dat`) | il codec qui sotto; ogni settore delle mappe decodificato per intero durante lo studio usa esattamente il suo flusso di bit (al massimo il riempimento di byte rimasto), il resto verificato dall'intestazione. Verificato bit per bit contro i file `distlod.raw` non compressi che il gioco fornisce accanto ai loro `distlod.dat`, e contro la mappa delle altezze a LOD lontano di una mappa (correlazione 0,999) |
| Altezze | metri = grezzo x heightMul / 256 - SeaLevel x heightMul. Il mare di una mappa si decodifica esattamente nell'altezza indicata dai commenti del suo hini; il bordo di un'altra nel suo `bounds_level` |
| Collocazione | bilineare tra i quattro angoli dell'hini, riga 0 a nord, colonna 0 a ovest. Verificata su una mappa contro città, coste e mari noti (altezze delle città entro circa 10 m di quelle reali, i mari sotto il livello del mare). Gli angoli sono un quadrilatero, non la proiezione propria del gioco, quindi aspettati un errore di alcune centinaia di metri al centro di una mappa grande. L'hini di una famiglia di mappe riporta gli angoli di un'altra mappa (coprono una frazione della sua dimensione reale); questo viene rilevato, e quella famiglia viene collocata invece con un adattamento sui punti di riferimento: città e aeroporti dei database di posizione del gioco (`*.ldfbin`) confrontati con le loro posizioni reali, errore quadratico medio di un paio di chilometri (le città confrontate con gli aeroporti che portano il loro nome, e le coordinate dei luoghi reali a circa un chilometro). Il JSON elenca ogni punto di riferimento e il suo scarto |
| Maschera dell'acqua (`water.wtr`: quattro livelli piramidali di tessere, ogni tessera una tabella di blocchi da 400 m, ogni blocco terra, pieno o in parte acqua con la sua forma in un flusso di bit) | il contenitore viene letto su ogni mappa (nessun byte avanzato sui file decodificati per intero); la forma dentro un blocco parzialmente acqueo **non viene decodificata**. I blocchi pieni sono acqua; nei blocchi parzialmente acquei un campione è acqua dove la mappa dell'acqua (`height_w.dat`, stesso codec della mappa delle altezze) è sopra il terreno oppure, accanto a un lago, dove il terreno non è più alto del lago; i blocchi di terra sono asciutti. Questo elimina la palude che la sola mappa dell'acqua segnala come acqua. I fiumi più stretti della griglia di output risultano spezzati in pezzi |
| Impronte delle città (le mesh di decalcomania elencate in `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: tessere di 25,6 km di triangoli piatti testurizzati) | lette su ogni mappa; si conservano le facce la cui trama è una città, un villaggio o un terreno industriale. Verificate contro città reali su alcune mappe (una città su entrambe le sponde di un fiume, una confluenza). Sono impronte: il gioco colloca gli edifici a runtime, e i file non contengono edifici |
| Aeroporti, ponti, edifici | **non letti**: gli aeroporti sono oggetti di missione, gli edifici vengono dalla collocazione propria del gioco |
| Foreste (`forest_map.wtr`) | i suoi blocchi si leggono allo stesso modo, ma quasi ogni blocco è "in parte foresta", quindi senza il flusso di bit non c'è una maschera della foresta utilizzabile; non disegnata |
| Le trame del terreno | non lette |

## Il codec della mappa delle altezze {#the-heightmap-codec}

Ricavato dai soli file di dati; non è stato letto né disassemblato alcun codice del gioco.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            dall'inizio del file, per righe, riga superiore per prima
settore: u16 count (byte che seguono), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
         poi un flusso di bit letto dal più significativo:
  PRE   2 * (log2(sectorSize) - 5) bit, finora sempre 0
  LIT   il primo campione: segno (1), n (bit LW), grandezza (n + 1 bit)
  poi fino a riempire il settore:
    0 LIT       successivo = precedente + LIT
    1 RUN LIT   il campione precedente si ripete RUN volte (k: 3 bit, m: k + 1 bit, RUN = m + 1),
                poi (a meno che il settore non sia pieno) successivo = precedente + LIT
  i valori sono a 16 bit: leggili modulo 65536
```

I settori parziali sui bordi destro e inferiore vengono riempiti e ritagliati. Lo stesso codec vale per
la mappa dell'acqua e per la mappa delle altezze a LOD lontano.

## Adattamenti sui punti di riferimento {#landmark-fits}

Dove gli angoli di una mappa non possono essere usati, `landmarks.py` adatta una trasformazione affine
dai metri del gioco alla Terra con il metodo dei minimi quadrati: le posizioni nel gioco dai file
dell'utente (blocchi `Airfield` delle missioni, i database delle posizioni della carriera), le
posizioni reali dalle tabelle delle coordinate pubblicate dei luoghi nel codice. Il `georeference` del
JSON riporta la matrice, l'origine, ogni punto di riferimento con il suo scarto e l'errore quadratico
medio.
