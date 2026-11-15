---
title: Archivi senza tabella dei file
nav_order: 6
lang: it
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Un gioco i cui archivi non hanno una tabella dei file {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea non conserva negli archivi una tabella dei file leggibile (i nomi sono cifrati in un
blocco alla fine di ogni archivio), e i suoi file di impostazione non sono memorizzati in forma
leggibile. `list` mostra la sua mappa con il gioco `Korea`. Quindi:

- la sua mappa delle altezze e la sua mappa dell'acqua vengono trovate dalla loro intestazione (il
  layout di `height.dat`, settori da 128 campioni; una griglia molto grande a una dimensione di cella
  fine);
- viene collocata sulla Terra adattando gli aeroporti che le sue missioni collocano
  (`data/Missions/**/*.Mission`, letti sulla tua macchina) alle coordinate pubblicate dei veri
  aeroporti (`korea.py`): scarti di decine fino a qualche centinaio di metri. Il JSON elenca ogni
  punto di riferimento e il suo scarto;
- heightMul e SeaLevel sono stimati: le navi nelle missioni stanno sul mare, quindi la loro altezza
  rispetto al valore più comune (il mare) della mappa dell'acqua dà la scala. Le altezze risultano
  plausibili (il mare sotto il livello del mare, le città costiere a pochi metri), non verificate
  oltre. Il JSON le segna come stimate.
