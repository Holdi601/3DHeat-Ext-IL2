---
title: "Geschwindigkeit, Tests, Bedingungen"
nav_order: 7
lang: "de"
source: terms.md
source_hash: "3baa9f57ade6"
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

Dieses Werkzeug liest die Archive deiner eigenen Installation von IL-2 Sturmovik: Great Battles auf deinem Rechner und verändert sie nie.

Nichts aus dem Spiel wird mitgeliefert oder weitergegeben: keine Spieldateien, kein Spielcode, keine DLLs; die Tests bauen jede Datei, die sie lesen, selbst. Die Levels, die es schreibt, bleiben auf deinem Rechner.

3DHeat IL-2 steht in keiner Verbindung zu 1C Game Studios / 777 Studios und wird von dort weder unterstützt noch empfohlen. IL-2 Sturmovik und zugehörige Namen und Marken gehören ihren Inhabern.

Rechteinhaber: Eröffnet ein Issue unter [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - wir antworten schnell und entfernen auf Anfrage alles.

## Lizenz {#licence}

MIT – siehe [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Verwendet numpy
(BSD-3-Clause) und optional numba (BSD-2-Clause). `heat3d_ext_il2.update` ist der gemeinsame Updater der
3DHeat-Werkzeuge.
