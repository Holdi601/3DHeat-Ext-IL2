---
title: "Arhive fără tabel de fișiere"
nav_order: 6
lang: "ro"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Un joc cu arhive fără tabel de fișiere {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea nu păstrează în arhivele sale un tabel de fișiere citibil (numele sunt ascunse
într-un bloc la sfârșitul fiecărei arhive), iar fișierele sale de setări nu sunt stocate citibil.
`list` îi arată harta cu jocul `Korea`. Așadar:

- harta sa de înălțimi și harta sa de apă sunt găsite după antet (aspectul `height.dat`,
  sectoare de 128 de eșantioane; o grilă foarte mare, la o dimensiune fină a celulei);
- este plasată pe pământ potrivind aerodromurile pe care le plasează misiunile sale
  (`data/Missions/**/*.Mission`, citite pe calculatorul dumneavoastră) cu coordonatele publicate ale
  aerodromurilor reale (`korea.py`): reziduuri de zeci până la câteva sute de metri. JSON-ul listează
  fiecare reper și reziduul său;
- heightMul și SeaLevel sunt estimate: navele din misiuni stau pe mare, deci înălțimea lor peste cea
  mai frecventă valoare (marea) din harta de apă dă scara. Înălțimile ies plauzibile (marea sub nivelul
  mării, orașele de coastă la câțiva metri), dar nu au fost verificate mai departe. JSON-ul le marchează ca estimate.
