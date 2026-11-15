---
title: "Karten finden: list"
nav_order: 2
lang: de
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Karten finden: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          dasselbe, auch ohne den installierten Befehl
```

Noch nie in der Kommandozeile gearbeitet? Lies zuerst [Bevor du anfängst](before-you-start.md).

1. Einmal installieren: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, ein Terminal in
   diesem Ordner öffnen und `python -m pip install -e .` ausführen (Python 3.10 oder neuer; es bringt
   numpy mit; `python -m pip install -e .[fast]` fügt numba hinzu).
2. Führe `heat3d-il2-level list` aus.
3. Jede Karte gibt eine Zeile aus, durch Tabulatoren getrennt: ihren Namen (den `extract` annimmt), das
   Spiel (`Great Battles`, oder `Korea` für [das zweite Spiel](archives-without-table.md)), die
   Höhenkarte, die sie liest, und wo sie auf der Erde liegt – ihr Breiten-/Längengrad-Bereich aus den
   Ecken der Karte, oder die Anpassung über Orientierungspunkte, die sie platziert, oder
   `not placed on the earth` (nicht auf der Erde platziert). Die letzte Zeile (auf stderr) zählt die
   Karten und nennt die Installationen.

![list auf einer erfundenen Installation](../assets/img/list.svg)

Das Bild zeigt einen Lauf auf einer Installation, die aus den Test-Schreibern (`tests/synth.py`) gebaut
wurde, nicht auf dem Spiel selbst.

## Wo die Installationen gefunden werden {#where-the-installs-are-found}

Über Steam; sonst `--game <folder>` (mehrfach möglich, eins pro Installation) oder die Umgebungsvariable
`HEAT3D_IL2_GAME`. Eine Installation ist ein Ordner, dessen `data` `Maps*.gtp`-Archive enthält.

| Option | Wirkung |
|---|---|
| `--game FOLDER` | ein IL-2-Ordner; für mehrere Installationen wiederholen |

Exit-Status: 0: fertig, 2: keine Installation gefunden.
