---
title: "Skjalasöfn án skráartöflu"
nav_order: 6
lang: is
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Leikur þar sem skjalasöfnin hafa enga skráartöflu {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea geymir enga læsilega skráartöflu í skjalasöfnum sínum (nöfnin
eru hössuð í blokk aftast í hverju skjalasafni), og stillingaskrár þess eru
ekki geymdar læsilegar. `list` sýnir kort þess með leiknum `Korea`. Þess vegna:

- hæðarkort þess og vatnskort finnast á haus sínum (uppbygging `height.dat`,
  geirar með 128 sýnum; mjög stórt net með fíngerðum reitastærðum);
- það er staðsett á jörðinni með því að fitta flugvellina sem verkefni þess setja
  (`data/Missions/**/*.Mission`, lesið á þinni vél) við birt hnit raunverulegra
  flugvalla (`korea.py`): afgangsskekkjur frá tugum upp í nokkur hundruð
  metra. JSON-skráin telur upp hvert kennileiti og afgangsskekkju þess;
- heightMul og SeaLevel eru áætluð: skip í verkefnunum sitja á sjónum,
  svo hæð þeirra yfir algengasta (sjávar) gildi vatnskortsins gefur kvarðann.
  Hæðirnar koma trúverðugar út (sjórinn undir sjávarmáli, strandbæir í nokkrum
  metrum), ekki athugað frekar. JSON-skráin merkir þær áætlaðar.
