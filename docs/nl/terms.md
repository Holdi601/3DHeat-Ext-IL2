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

Deze tool leest de archieven van je eigen installatie van IL-2 Sturmovik: Great Battles op je computer en verandert ze nooit.

Niets uit het spel wordt meegeleverd of verspreid: geen spelbestanden, geen spelcode, geen DLL's; de tests bouwen elk bestand dat ze lezen zelf. De levels die hij schrijft blijven op je computer.

3DHeat IL-2 is niet verbonden aan en niet goedgekeurd door 1C Game Studios / 777 Studios. IL-2 Sturmovik en bijbehorende namen en handelsmerken zijn van hun eigenaars.

Rechthebbenden: open een issue op [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - we reageren snel en verwijderen alles op verzoek.

## Licentie {#licence}

MIT - zie [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Gebruikt numpy (BSD-3-Clause) en, optioneel,
numba (BSD-2-Clause). `heat3d_update` is de gedeelde updater van de 3DHeat-tools.
