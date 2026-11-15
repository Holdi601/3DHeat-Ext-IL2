---
title: Arxius sense taula de fitxers
nav_order: 6
lang: ca
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Un joc els arxius del qual no tenen taula de fitxers {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea no conserva cap taula de fitxers llegible als seus arxius (els noms
estan triturats en un bloc al final de cada arxiu), i els seus fitxers de configuració no
s'emmagatzemen llegibles. `list` mostra el seu mapa amb el joc `Korea`. Així doncs:

- el seu mapa d'alçades i el seu mapa d'aigua es troben per la seva capçalera (la disposició
  de `height.dat`, sectors de 128 mostres; una quadrícula molt gran amb una mida de cel·la fina);
- es col·loca a la Terra ajustant els aeròdroms que col·loquen les seves missions
  (`data/Missions/**/*.Mission`, llegides a la teva màquina) a les coordenades publicades
  dels aeròdroms reals (`korea.py`): residus de desenes a pocs centenars de
  metres. El JSON enumera cada punt de referència i el seu residu;
- heightMul i SeaLevel s'estimen: els vaixells de les missions estan sobre el mar, de manera que
  la seva altura sobre el valor més comú (el mar) del mapa d'aigua dona l'escala.
  Les altures surten plausibles (el mar per sota del nivell del mar, els pobles de costa a pocs
  metres), sense més comprovacions. El JSON les marca com a estimades.
