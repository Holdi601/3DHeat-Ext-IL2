---
title: Arkiver uten filtabell
nav_order: 6
lang: no
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Et spill der arkivene ikke har en filtabell {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea har ingen lesbar filtabell i arkivene sine (navnene er hashet i en blokk
på slutten av hvert arkiv), og innstillingsfilene er ikke lagret lesbart. `list` viser kartet
med spillet `Korea`. Derfor:

- høydekartet og vannkartet finnes ved hodet deres (`height.dat`-oppsettet,
  sektorer på 128 prøver; et veldig stort rutenett med en fin cellestørrelse);
- det plasseres på jorden ved å tilpasse flyplassene oppdragene plasserer
  (`data/Missions/**/*.Mission`, lest på din egen maskin) til de virkelige flyplassenes
  publiserte koordinater (`korea.py`): avvik på titalls til noen hundre
  meter. JSON-filen lister hvert landemerke og dets avvik;
- heightMul og SeaLevel er anslått: skip i oppdragene ligger på havet, så
  deres høyde over vannkartets vanligste (havets) verdi gir skalaen.
  Høydene blir rimelige (havet under havnivå, kystbyer noen få meter over), ikke
  kontrollert videre. JSON-filen merker dem som anslått.
