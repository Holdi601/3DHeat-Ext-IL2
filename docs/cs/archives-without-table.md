---
title: "Archivy bez tabulky souborů"
nav_order: 6
lang: cs
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Hra, jejíž archivy nemají tabulku souborů {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea nemá v archivech čitelnou tabulku souborů (názvy jsou zahašované v bloku
na konci každého archivu) a její nastavení nejsou uložena čitelně. `list` zobrazí její mapu
s hrou `Korea`. Proto:

- její výškovou mapu a mapu vody najde podle hlavičky (rozložení `height.dat`, sektory po 128
  vzorcích; velmi velká mřížka s jemnou velikostí buňky);
- umístí se na Zemi přizpůsobením letišť, která její mise rozmísťují
  (`data/Missions/**/*.Mission`, čteno na vašem počítači), k zveřejněným souřadnicím
  skutečných letišť (`korea.py`): odchylky desítek až několika set metrů. JSON vypisuje
  každý orientační bod a jeho odchylku;
- výška heightMul a SeaLevel se odhaduje: lodě v misích stojí na moři, takže jejich výška nad
  nejčastější (mořskou) hodnotou mapy vody dá měřítko. Výšky vycházejí věrohodně (moře pod
  hladinou, pobřežní města několik metrů nad ní), dál se neověřovaly. JSON je označuje jako odhadnuté.
