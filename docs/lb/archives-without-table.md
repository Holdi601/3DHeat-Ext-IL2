---
title: "Archiver ouni Dateitabell"
nav_order: 6
lang: lb
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# E Spill, dessen Archiver keng Dateitabell hunn {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea hält keng liesbar Dateitabell a sengen Archiver (d'Nimm
si gehasht an engem Block um Enn vun all Archiv), a seng Astellungsdateien sinn
net liesbar gespäichert. `list` weist seng Map mam Spill `Korea`. Also:

- seng Heightmap a Waasserkaart ginn un hirem Header fonnt (d'`height.dat`-
  Layout, Sektore vun 128 Echantillonen; e ganz grousst Gitter bei fenger Zellgréisst);
- et gëtt op der Äerd placéiert, andeems d'Fluchhäfen, déi seng Missioune placéieren
  (`data/Missions/**/*.Mission`, op Ärem Rechner gelies), un d'publizéiert Koordinate vun den
  richtege Fluchhäfen ugepasst ginn (`korea.py`): Residuen vun Zéngerte bis e puer honnert
  Meter. De JSON lëscht all Landmark a säi Residuum;
- heightMul a SeaLevel gi geschat: Schëffer an de Missioune sti um Mier,
  also gëtt hir Héicht iwwer dem heefegste (Mier-)Wäert vun der Waasserkaart d'Skala.
  D'Héichte kommen plausibel eraus (d'Mier ënner Mieresniveau, Küststied op e puer
  Meter), net weider gepréift. De JSON markéiert se als geschat.
