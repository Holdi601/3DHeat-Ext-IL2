---
title: "Archívy bez tabuľky súborov"
nav_order: 6
lang: sk
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Hra, ktorej archívy nemajú tabuľku súborov {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea nemá v archívoch čitateľnú tabuľku súborov (názvy sú zahashované v bloku na konci každého archívu) a jej nastavovacie súbory nie sú uložené čitateľne. `list` zobrazí jej mapu s hrou `Korea`. Preto:

- jej výšková mapa a mapa vody sa nájdu podľa hlavičky (rozloženie `height.dat`, sektory po 128 vzorkách; veľmi veľká mriežka pri jemnej veľkosti bunky);
- umiestni sa na zemi tak, že sa prispôsobia letiská, ktoré jej misie umiestňujú (`data/Missions/**/*.Mission`, čítané na vašom počítači), zverejneným súradniciam skutočných letísk (`korea.py`): odchýlky desiatky až niekoľko stoviek metrov. JSON vypisuje každý orientačný bod a jeho odchýlku;
- heightMul a SeaLevel sa odhadujú: lode v misiách stoja na mori, takže ich výška nad najbežnejšou (morskou) hodnotou mapy vody dáva mierku. Výšky vychádzajú vierohodne (more pod hladinou mora, pobrežné mestá na niekoľkých metroch), ďalej sa neoverovali. JSON ich označuje ako odhadnuté.
