---
title: "Ein Spiel ohne Dateitabelle in den Archiven"
nav_order: 6
lang: "de"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Ein Spiel, dessen Archive keine Dateitabelle haben {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea hat in seinen Archiven keine lesbare Dateitabelle (die Namen stehen gehasht in einem Block am Ende jedes Archivs), und seine Einstellungsdateien sind nicht lesbar gespeichert. `list` zeigt seine Karte mit dem Spiel `Korea`. Deshalb:

- werden seine Höhenkarte und Wasserkarte an ihrem Kopfteil erkannt (das Layout von `height.dat`, Sektoren zu 128 Samples; ein sehr großes Raster mit feiner Zellgröße);
- wird sie auf der Erde platziert, indem die Flugplätze angepasst werden, die seine Missionen setzen (`data/Missions/**/*.Mission`, auf deinem Rechner gelesen), an die veröffentlichten Koordinaten der echten Flugplätze (`korea.py`): Abweichungen von zehn bis einigen hundert Metern. Die JSON-Datei listet jeden Orientierungspunkt und seine Abweichung auf;
- werden heightMul und SeaLevel geschätzt: Schiffe in den Missionen liegen auf dem Meer, daher ergibt ihre Höhe über dem häufigsten (Meer-)Wert der Wasserkarte den Maßstab. Die Höhen wirken plausibel (das Meer unter dem Meeresspiegel, Küstenstädte einige Meter hoch), wurden aber nicht weiter geprüft. Die JSON-Datei markiert sie als geschätzt.
