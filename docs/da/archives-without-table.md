---
title: Arkiver uden filtabel
nav_order: 6
lang: da
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Et spil, hvis arkiver ikke har nogen filtabel {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea har ingen læsbar filtabel i sine arkiver (navnene er hashet i en blok til
sidst i hvert arkiv), og dets indstillingsfiler er ikke gemt læsbart. `list` viser dets kort med spillet
`Korea`. Så:

- dets højdekort og vandkort findes via deres header (layoutet i `height.dat`,
  sektorer på 128 prøver; et meget stort gitter med en fin cellestørrelse);
- det placeres på jorden ved at tilpasse de flyvepladser, dets missioner placerer
  (`data/Missions/**/*.Mission`, læst på din maskine), til de rigtige flyvepladsers
  offentliggjorte koordinater (`korea.py`): afvigelser på titalls til nogle få hundrede
  meter. JSON'en lister hvert landemærke og dets afvigelse;
- heightMul og SeaLevel er estimeret: skibene i missionerne står på havet, så deres højde over
  vandkortets hyppigste (havets) værdi giver skalaen. Højderne bliver plausible (havet under havniveau,
  kystbyer få meter op), ikke kontrolleret yderligere. JSON'en markerer dem som estimerede.
