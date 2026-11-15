---
title: "Level bauen: extract"
nav_order: 3
lang: "de"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Level bauen: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Schritt für Schritt {#step-by-step}

Noch nie in der Kommandozeile gearbeitet? Lies zuerst [Bevor du anfängst](before-you-start.md).

1. Finde den Namen der Karte mit [`list`](list.md).
2. Führe `heat3d-il2-level extract <map> -o levels` aus. Namen dürfen Platzhalter enthalten, in
   Anführungszeichen (`"<family>_*"`); `--all` nimmt jede Karte.
3. Um eine Aufnahme ohne Platzierungsschritt auf das Level zu legen, gib ihren Ursprung an:
   `--origin <lat> <lon>`, gesetzt auf das `geo` der Aufnahme (ihr Referenzpunkt der Sitzung).
   Ohne ihn ist die Mitte der Karte der Ursprung, und das `geo` der `.json`-Datei sagt, welcher es ist.
4. Der Befehl gibt eine Zeile pro Karte aus, während er sie dekodiert, und dann
   `ok <glb> <triangles> (<frame> frame)` oder `failed <map>: <why>`.
5. Lade `<folder>/<map>/<map>.glb` im Panel „Hintergrund / Level“ des Viewers.

![extract auf einer erfundenen Installation](../assets/img/extract.svg)

In den eigenen Metern des Spiels, ohne das Wasser:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Ein zweiter Lauf über schon geschriebene Karten:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Optionen {#options}

| Option | Standard | Wirkung |
|---|---|---|
| `maps` | - | Kartennamen, wie `list` sie ausgibt; Platzhalter erlaubt |
| `--all` | aus | jede Karte; Saisons, die eine Höhenkarte und eine Wasserkarte teilen, werden einmal geschrieben |
| `-o`, `--out` | nötig | der Ausgabeordner; jede Karte kommt in `<out>/<map>/` |
| `--game FOLDER` | gefunden | ein IL-2-Ordner (mehrfach möglich) |
| `--max-grid N` | `1024` | höchstens so viele Höhenkarten-Samples pro Seite (1024: etwa 2 Millionen Dreiecke); die Karte wird jedes *k*-te Sample abgetastet, damit sie passt |
| `--frame` `enu` oder `game` | `enu` | `enu`: Meter nach Osten, Höhe, Meter nach Norden von `--origin`, wie die Tacview-Tabellen des Watchers; `game`: die eigenen Meter des Spiels (x Norden, y oben, z Osten). Eine Karte, die nicht auf der Erde platziert werden kann, wird immer in `game` geschrieben, egal was verlangt ist |
| `--origin LAT LON` | die Mitte der Karte | der Ursprung des `enu`-Rahmens (das `geo` einer Aufnahme) |
| `--no-water` | aus | das Wasser weglassen |
| `--no-towns` | aus | die Stadtflächen weglassen |
| `--skip-existing` | aus | Karten überspringen, deren `.glb` schon existiert |

Jede Option, so wie das Programm sie ausgibt: [Befehlsreferenz](../cli-reference.md).

Setze `HEAT3D_DEBUG`, um den vollständigen Traceback einer fehlgeschlagenen Karte auszugeben. Die
`.glb` wird nach `<map>.glb.part` geschrieben und umbenannt, wenn sie fertig ist.

Exit-Status: 0: jede Karte geschrieben, 1: mindestens eine fehlgeschlagen (die anderen werden trotzdem
geschrieben), 2: keine Installation oder keine Karte passt.

## Beispiele {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # eine Karte, enu-Rahmen um ihre Mitte
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in der flachen Karte einer Aufnahme mit diesem geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # feiner, mehrere Karten
heat3d-il2-level extract --all --skip-existing -o levels         # jede Karte, nur die neuen
heat3d-il2-level extract <map> --frame game -o levels            # die eigenen Meter des Spiels, so wie Missionsdateien sie haben
```

Was in den Dateien steht: [Die Level-Dateien und Rahmen](output.md).
