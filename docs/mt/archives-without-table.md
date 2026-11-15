---
title: Arkivji mingħajr tabella tal-fajls
nav_order: 6
lang: mt
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Logħba li l-arkivji tagħha m'għandhomx tabella tal-fajls {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea ma żżomm ebda tabella tal-fajls li tinqara fl-arkivji tagħha (l-ismijiet
huma hashed f'blokk fl-aħħar ta' kull arkivju), u l-fajls tas-settings tagħha
mhumiex maħżunin b'mod li jinqara. `list` juri l-mappa tagħha bil-logħba `Korea`. Allura:

- l-heightmap u l-water map tagħha jinstabu bl-header tagħhom (il-layout ta'
  `height.dat`, setturi ta' 128 kampjun; grilja kbira ħafna b'cell fin);
- titqiegħed fuq l-art billi jitqiegħdu l-ajrudromi li l-missjonijiet tagħha jqiegħdu
  (`data/Missions/**/*.Mission`, moqrija fuq il-magna tiegħek) fuq il-koordinati
  ppubblikati tal-ajrudromi reali (`korea.py`): residwi ta' għexieren sa ftit mijiet ta'
  metri. Il-JSON jelenka kull landmark u r-residwu tiegħu;
- heightMul u SeaLevel huma stmati: il-vapuri fil-missjonijiet joqogħdu fuq il-baħar,
  allura l-għoli tagħhom fuq il-valur l-aktar komuni (baħar) tal-water map jagħti l-iskala.
  L-għoli joħroġ plawżibbli (il-baħar taħt il-livell tal-baħar, irħula kostali f'ftit
  metri), mhux ikkontrollat aktar. Il-JSON jimmarkahom stmati.
