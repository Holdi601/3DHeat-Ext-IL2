---
title: "Arhive bez tabele datoteka"
nav_order: 6
lang: bs
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Igra čije arhive nemaju tabelu datoteka {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea u svojim arhivama ne drži čitljivu tabelu datoteka (imena
su heširana u bloku na kraju svake arhive), a njene datoteke postavki
nisu pohranjene u čitljivom obliku. `list` prikazuje njenu mapu s igrom `Korea`. Dakle:

- njena visinska mapa i vodena mapa nalaze se po zaglavlju (raspored
  `height.dat`, sektori od 128 uzoraka; vrlo velika mreža s finom veličinom ćelije);
- postavlja se na Zemlju prilagođavanjem aerodroma koje njene misije postavljaju
  (`data/Missions/**/*.Mission`, čitaju se na tvom računaru) prema objavljenim
  koordinatama stvarnih aerodroma (`korea.py`): odstupanja od desetina do nekoliko stotina
  metara. JSON navodi svaki orijentir i njegovo odstupanje;
- heightMul i SeaLevel su procijenjeni: brodovi u misijama stoje na moru,
  pa njihova visina nad najčešćom (morskom) vrijednošću vodene mape daje skalu.
  Visine izlaze prihvatljive (more ispod nivoa mora, obalni gradovi na nekoliko
  metara), ali nisu dalje provjerene. JSON ih označava kao procijenjene.
