---
title: Arhīvi bez failu tabulas
nav_order: 6
lang: lv
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Spēle, kuras arhīviem nav failu tabulas {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea arhīvos neglabā lasāmu failu tabulu (vārdi ir sajaukti blokā katra arhīva beigās),
un tās iestatījumu faili nav saglabāti lasāmi. `list` rāda tās karti ar spēli `Korea`. Tātad:

- tās augstuma karti un ūdens karti atrod pēc galvenes (`height.dat` izkārtojums, sektori pa 128 paraugiem; ļoti liels režģis ar smalku šūnas izmēru);
- tā tiek novietota uz zemes, pieskaņojot lidlaukus, ko tās misijas novieto (`data/Missions/**/*.Mission`, nolasīti tavā datorā), reāliem lidlaukiem ar publicētām koordinātēm (`korea.py`): atlikumi desmiti līdz dažu simtu metru. JSON uzskaita katru orientieri un tā atlikumu;
- heightMul un SeaLevel tiek novērtēti: kuģi misijās atrodas uz jūras, tāpēc to augstums virs ūdens kartes visbiežāk sastopamās (jūras) vērtības dod mērogu. Augstumi izrādās ticami (jūra zem jūras līmeņa, piekrastes pilsētas dažu metru augstumā), tālāk nav pārbaudīti. JSON atzīmē tos kā novērtētus.
