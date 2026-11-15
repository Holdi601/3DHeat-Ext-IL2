---
title: "Snelheid, tests, voorwaarden"
nav_order: 7
lang: "nl"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Snelheid, tests, voorwaarden {#speed-tests-terms}

## Snelheid {#speed}

Decoderen is pure Python tenzij numba is geïnstalleerd (`python -m pip install -e .[fast]`):
een kaart van gemiddelde grootte duurt zonder dit ongeveer 15 s en met dit ongeveer een seconde; de
grootste kaart, enkele honderden miljoenen monsters, ongeveer 7 s met dit (de eerste
run compileert ook). Het geheugen blijft bij één rij sectoren plus het uitvoerraster.

## Tests {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` bouwt archieven, hoogtekaarten (een encoder voor de codec hierboven),
`height.hini`-bestanden en archieven zonder bestandstabel in code.

## De voorwaarden {#the-terms}

De licentieovereenkomst van IL-2 Sturmovik: Great Battles en IL-2 Series (1C Game
Studios / 777 Studios) is **niet gevonden**: niet in de installatie (waarvan
`data/Licenses.txt` alleen licenties van derden bevat), niet op de site van de uitgever,
en de EULA-pagina van Steam laadde niet. Controleer dit zelf voordat je erop vertrouwt.
Deze tool leest alleen de archieven en verandert ze nooit. De levels die hij schrijft blijven
op jouw computer: **publiceer ze nooit**. Hier wordt geen spelgegeven meegeleverd, en de
tests bouwen elk bestand dat ze lezen.

## Licentie {#licence}

MIT - zie [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Gebruikt numpy (BSD-3-Clause) en, optioneel,
numba (BSD-2-Clause). `heat3d_update` is de gedeelde updater van de 3DHeat-tools.
