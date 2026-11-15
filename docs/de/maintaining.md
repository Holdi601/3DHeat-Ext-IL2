---
title: "Diese Doku pflegen"
nav_order: 91
lang: "de"
source: maintaining.md
source_hash: "a37a32cc5026"
nav_exclude: true
search_exclude: true
---
# Diese Doku pflegen {#maintaining-these-docs}

Eine Checkliste für jedes Release, damit die Seiten nie hinter dem Code zurückbleiben.

1. **Die Referenz neu erzeugen.** `python tools/gen_docs_reference.py` schreibt die
   [Befehlsreferenz](../cli-reference.md) aus dem eigenen `--help` des Programms und seinen Ausgabespalten neu.
   `python tools/gen_docs_reference.py --check` endet mit 1, wenn die gespeicherte Seite veraltet ist.
2. **Auflisten, was sich geändert hat.** `git log v<VERSION>..HEAD --oneline`, wobei `<VERSION>` die
   zuletzt veröffentlichte Version ist (die Datei `VERSION` beim Release). Gib jeder neuen Funktion, jeder
   Option und jeder Ausgabespalte einen Platz auf einer Seite und eine Zeile im Abschnitt **Docs** von
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/CHANGELOG.md).
3. **Unabhängige Prüfung.** Jemand, der die Seiten nicht geschrieben hat, liest die README und jede
   geänderte Seite, die Bilder eingeschlossen, dreimal: als Anfänger, der noch nie ein Terminal benutzt
   hat, als Achtjähriger und als Experte, der jede Option gegen `--help` prüft. Beispiele verwenden nur
   erfundene Namen und Zahlen.
4. **Behebe** alles, was die Prüfung findet.
5. **Übersetzungen.** Jede übersetzte Seite speichert den Hash der englischen Seite, aus der sie entstand.
   Übersetze die Seiten neu, deren englische Quelle sich geändert hat, und prüfe dann jede Sprache: klarer
   Text, richtige Beschriftungen der Diagramme, dieselben Wörter wie die übersetzte Oberfläche des Viewers.
6. **Führe die Tests aus** (`pytest`).
7. **Hochladen** (Push) erst nach dem Okay des Eigentümers.

## Übersetzungen: die Befehle {#translations-the-commands}

Die Seite wird in die 40 Sprachen des 3DHeat-Viewers übersetzt: Englisch in `docs/`, jede andere Sprache in
`docs/<lang>/` mit denselben Dateinamen. `tools/docs_i18n.py` führt die Buchhaltung:

```bash
python tools/docs_i18n.py hashes             # nach jeder englischen Änderung: den Hash jeder Seite speichern
python tools/docs_i18n.py svg-strings        # nach jeder Bildänderung: die zu übersetzenden Beschriftungen
python tools/docs_i18n.py status             # pro Sprache: aktuelle, veraltete und fehlende Seiten
python tools/docs_i18n.py todo --lang de     # die deutschen Seiten, die (neu) zu übersetzen sind
python tools/docs_i18n.py svg-build --lang de    # deutsche Bilder aus docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # die deutschen Seiten mit dem englischen Hash stempeln
python tools/docs_i18n.py check              # endet mit 1, wenn Hashes oder Beschriftungen veraltet sind
```

Übersetze nur, was `todo` auflistet: Markdown, Links, Code, Datei- und Spaltennamen bleiben, wie sie sind.
Übersetze Titel und Bildbeschreibungen, und verwende die eigenen Wörter des 3DHeat-Viewers für seine
Buttons und Panels (sein `src/i18n/locales/<lang>/`). Erzeugte Referenzseiten und Terminal-Bilder bleiben
englisch. Auf der Seite sagt eine veraltete Übersetzung das und verlinkt die englische Seite; eine fehlende
fällt auf Englisch zurück. Das Sprachmenü im Kopf und die Weiterleitung der Startseite nach Browsersprache
kommen aus `docs/_includes/`.
