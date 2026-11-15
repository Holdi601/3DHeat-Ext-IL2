---
title: Arhivi bez tablice datoteka
nav_order: 6
lang: hr
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Igra čiji arhivi nemaju tablicu datoteka {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea ne čuva čitljivu tablicu datoteka u svojim arhivima (imena su
sažeta u bloku na kraju svakog arhiva), a njezine datoteke postavki nisu
spremljene čitljivo. `list` prikazuje njezinu kartu s igrom `Korea`. Zato:

- njezina visinska mapa i karta vode pronalaze se po zaglavlju (raspored `height.dat`,
  sektori od 128 uzoraka; vrlo velika mreža s finom veličinom ćelije);
- postavlja se na Zemlju prilagodbom zračnih luka koje njezine misije postavljaju
  (`data/Missions/**/*.Mission`, čitano na vašem računalu) objavljenim koordinatama
  stvarnih zračnih luka (`korea.py`): odstupanja od desetaka do nekoliko stotina
  metara. JSON navodi svaki orijentir i njegovo odstupanje;
- heightMul i SeaLevel su procijenjeni: brodovi u misijama stoje na moru, pa se njihova
  visina iznad najčešće (morske) vrijednosti karte vode daje mjerilo. Visine ispadaju
  vjerojatne (more ispod razine mora, obalni gradovi na nekoliko metara), dalje nisu provjeravane.
  JSON ih označava kao procijenjene.
