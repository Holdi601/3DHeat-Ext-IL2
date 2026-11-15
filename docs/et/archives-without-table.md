---
title: "Arhiivid ilma failitabelita"
nav_order: 6
lang: "et"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Mäng, mille arhiividel ei ole failitabelit {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea ei hoia oma arhiivides loetavat failitabelit (nimed on räsitud
plokis iga arhiivi lõpus) ja selle seadistusfailid ei ole salvestatud loetavalt. `list` näitab tema kaarti mänguga `Korea`. Seega:

- selle kõrgustikukaart ja veekaart leitakse päise järgi (`height.dat`
  paigutus, sektorid 128 proovi kaupa; väga suur ruudustik peene lahtri suurusega);
- see paigutatakse maakerale, sobitades lennuväljad, mida tema missioonid paigutavad
  (`data/Missions/**/*.Mission`, loetud sinu masinas), avaldatud tegelike lennuväljade
  koordinaatidega (`korea.py`): jäägid kümnetest kuni mõnesaja meetrini. JSON loetleb
  iga maamärgi ja selle jäägi;
- heightMul ja SeaLevel on hinnatud: missioonide laevad seisavad merel, nii et nende kõrgus
  veekaardi kõige levinuma (mere) väärtuse suhtes annab skaala.
  Kõrgused tulevad mõistlikud (meri allpool merepinda, rannikulinnad mõne meetri kõrgusel),
  rohkem ei ole kontrollitud. JSON märgib need hinnatuks.
