---
title: "Arkiva pa tabelë skedarësh"
nav_order: 6
lang: "sq"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Një lojë arkivat e së cilës nuk kanë tabelë skedarësh {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea nuk mban asnjë tabelë skedarësh të lexueshme në arkivat e saj (emrat
janë hash-uar në një bllok në fund të çdo arkive), dhe skedarët e saj të cilësimeve
nuk ruhen të lexueshëm. `list` e shfaq hartën e saj me lojën `Korea`. Pra:

- heightmap dhe harta e ujit gjenden nga koka e tyre (skema `height.dat`,
  sektorë me 128 mostra; një rrjetë shumë e madhe me qelizë të imët);
- vendoset mbi tokë duke përshtatur aeroportet që i vendosin misionet e saj
  (`data/Missions/**/*.Mission`, lexuar në kompjuterin tënd) me koordinatat e botuara
  të aeroporteve të vërteta (`korea.py`): mbetje nga dhjetëra në disa qindra
  metra. JSON liston çdo pikë referimi dhe mbetjen e saj;
- heightMul dhe SeaLevel vlerësohen: anijet në misione ulen mbi det,
  kështu që lartësia e tyre mbi vlerën më të zakonshme (të detit) të hartës së ujit jep shkallën.
  Lartësitë dalin të besueshme (deti nën nivelin e detit, qytetet bregdetare në disa
  metra), por nuk u kontrolluan më tej. JSON i shënon si të vlerësuara.
