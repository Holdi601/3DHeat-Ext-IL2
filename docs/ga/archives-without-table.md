---
title: Cartlanna gan tábla comhad
nav_order: 6
lang: "ga"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Cluiche a bhfuil a chartlanna gan tábla comhad {#a-game-whose-archives-have-no-file-table}

Ní choinníonn IL-2 Series: Korea aon tábla comhad inléite ina chartlanna (tá na hainmneacha
haiseáilte i mbloc ag deireadh gach cartlainne), agus níl a chomhaid socruithe
stóráilte inléite. Taispeánann `list` a léarscáil leis an gcluiche `Korea`. Mar sin:

- aimsítear a léarscáil airde agus a léarscáil uisce de réir a gceannteidil (leagan amach
  `height.dat`, hearnálacha de 128 sampla; greille an-mhór ar mhéid cille mhín);
- cuirtear ar an domhan é trí aerpháirceanna a gcuireann a mhisin (`data/Missions/**/*.Mission`,
  léite ar do mheaisín) a fheistiú le comhordanáidí foilsithe na n-aerpháirceanna
  fíora (`korea.py`): iarmhair de na deicheanna go cúpla céad
  méadar. Liostaíonn an JSON gach tírdhreach agus a iarmhar;
- meastar heightMul agus SeaLevel: suíonn longa sna misin ar an bhfarraige,
  mar sin tugann a n-airde os cionn luach is coitianta (farraige) na léarscáile uisce an scála.
  Tagann airde inchreidte amach (an fharraige faoi leibhéal na farraige, bailte cósta ag cúpla
  méadar), gan seiceáil ní b'fhaide. Marcálann an JSON iad mar mheasta.
