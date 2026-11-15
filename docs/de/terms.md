---
title: "Geschwindigkeit, Tests, Bedingungen"
nav_order: 7
lang: "de"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Geschwindigkeit, Tests, Bedingungen {#speed-tests-terms}

## Geschwindigkeit {#speed}

Das Dekodieren läuft in reinem Python, außer numba ist installiert (`python -m pip install -e .[fast]`):
eine mittelgroße Karte braucht etwa 15 s ohne und etwa eine Sekunde mit numba; die größte Karte, mehrere
hundert Millionen Samples, etwa 7 s mit numba (der erste Lauf kompiliert zusätzlich). Der Speicher bleibt
bei einer Zeile Sektoren plus dem Ausgaberaster.

## Tests {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` baut Archive, Höhenkarten (ein Encoder für den Codec oben), `height.hini`-Dateien und
Archive ohne Dateitabelle direkt im Code.

## Die Bedingungen {#the-terms}

Die Lizenzvereinbarung von IL-2 Sturmovik: Great Battles und IL-2 Series (1C Game Studios / 777 Studios)
wurde **nicht gefunden**: nicht in der Installation (deren `data/Licenses.txt` nur Lizenzen Dritter enthält),
nicht auf der Seite des Herausgebers, und die Steam-EULA-Seite lud nicht. Prüfe sie selbst, bevor du dich
darauf verlässt. Dieses Werkzeug liest nur die Archive und verändert sie nie. Die Level, die es schreibt,
bleiben auf deinem Rechner: **veröffentliche sie niemals**. Nichts hier liefert Spieldaten mit; die Tests
bauen jede Datei, die sie lesen.

## Lizenz {#licence}

MIT – siehe [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Verwendet numpy
(BSD-3-Clause) und optional numba (BSD-2-Clause). `heat3d_update` ist der gemeinsame Updater der
3DHeat-Werkzeuge.
