---
title: "Bevor du anfängst"
nav_order: 1.5
lang: "de"
source: before-you-start.md
source_hash: "9e62d9ba2baa"
nav_exclude: true
search_exclude: true
---
# Bevor du anfängst {#before-you-start}

Noch nie in der Kommandozeile gearbeitet? Diese Seite führt dich von null bis zum ersten Lauf.
Es dauert einmalig etwa zehn Minuten.

## 1. Python installieren {#install-python}

Dieses Werkzeug braucht **Python 3.10 oder neuer**.

- **Windows:** lade Python von [python.org/downloads](https://www.python.org/downloads/) herunter
  und starte das Installationsprogramm. Setze auf dem ersten Bildschirm das Häkchen bei
  **Add python.exe to PATH** (Python zum PATH hinzufügen), dann klicke auf **Install Now**
  (Jetzt installieren).
- **macOS und Linux:** Python 3 ist oft schon da. Wo diese Seiten `python` schreiben, tippe `python3`.

## 2. Dieses Werkzeug holen {#get-this-tool}

Öffne [github.com/Holdi601/3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2), klicke auf
den grünen Button **Code** und dann auf **Download ZIP**, und entpacke es in einen Ordner deiner
Wahl. Wenn du git benutzt: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`.

## 3. Ein Terminal in diesem Ordner öffnen {#open-a-terminal-in-that-folder}

Ein Terminal ist ein Fenster, in das du Befehle tippst.

- **Windows:** öffne den Ordner im Explorer, klicke in die Adressleiste, tippe `powershell` und
  drücke Enter. Ein blaues oder schwarzes Fenster öffnet sich, schon in diesem Ordner.
- **macOS:** öffne **Terminal**, tippe `cd ` (mit einem Leerzeichen), ziehe den Ordner in das
  Fenster und drücke Enter.

`cd` heißt „Ordner wechseln“: `cd C:\Tools\3DHeat-Ext-IL2` geht in diesen Ordner.

## 4. Das Werkzeug installieren {#install-the-tool}

Tippe dies und drücke Enter:

```bash
python -m pip install -e .
```

Am Ende solltest du sehen: `Successfully installed heat3d-ext-il2-...`.

## 5. Ausführen {#run-it}

```bash
heat3d-il2-level list
```

Du solltest etwa so etwas sehen:

```text
<map>	Great Battles	height /graphics/<map>/height.dat	<lat>..<lat> N, <lon>..<lon> E
<n> maps in C:\Games\IL-2 Sturmovik Great Battles
```

Weiter: [Karten finden: list](list.md), dann [Level bauen: extract](extract.md).

## So liest du die Befehle auf diesen Seiten {#how-to-read-the-commands-on-these-pages}

| Du siehst | Es bedeutet |
|---|---|
| `<folder>` | ein Platzhalter: tippe stattdessen deinen eigenen Wert, ohne die `< >` |
| `[--force]` | optional: lass es weg, oder tippe es so, wie es dasteht |
| `a\|b` | eine Wahl: tippe `a` oder `b` |
| `# a note` | ein Kommentar für dich: nicht eintippen |
| `"C:\My Files\x"` | einen Pfad mit Leerzeichen setzt du in Anführungszeichen |
| `D:\Demos` | ein Beispielordner unter Windows: nimm deinen eigenen |

## Wenn etwas schiefgeht {#when-something-goes-wrong}

| Die Meldung | Was zu tun ist |
|---|---|
| `'python' is not recognized` | Python ist nicht installiert, oder das Kästchen PATH war nicht angehakt: installiere es noch einmal und hake es an (oder tippe `py` statt `python`). |
| `'heat3d-il2-level' is not recognized` | Führe Schritt 4 im Ordner des Werkzeugs noch einmal aus, oder tippe `python -m heat3d_ext_il2` statt `heat3d-il2-level`: das tut dasselbe. |
| `No module named heat3d_ext_il2` | Du bist nicht im Ordner des Werkzeugs, oder Schritt 4 ist fehlgeschlagen: wechsle mit `cd` dorthin und führe Schritt 4 aus. |
| `No module named pip` | Führe `python -m ensurepip` aus, dann Schritt 4. |
| anything else | Lies die letzte Zeile der Meldung und öffne damit auf GitHub ein Issue. |

Jeder Befehl endet außerdem mit einem **Exit-Status**: 0 heißt, es hat funktioniert. Um ihn zu sehen,
tippe `echo $LASTEXITCODE` in PowerShell oder `echo $?` unter macOS und Linux.
