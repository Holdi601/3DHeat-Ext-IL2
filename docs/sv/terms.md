---
title: Hastighet, tester, villkor
nav_order: 7
lang: "sv"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Hastighet, tester, villkor {#speed-tests-terms}

## Hastighet {#speed}

Avkodningen är ren Python om inte numba är installerat (`python -m pip install -e .[fast]`):
en karta av medelstorlek tar ungefär 15 s utan det och ungefär en sekund med det; den största kartan, flera hundra miljoner prov, ungefär 7 s med det (första körningen kompilerar också). Minnet hålls till en rad av sektorer plus utdatarutnätet.

## Tester {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` bygger arkiv, höjdkartor (en kodare för kodeken ovan), `height.hini`-filer och arkiv utan filtabell i kod.

## Villkoren {#the-terms}

Det här verktyget läser arkiven i din egen installation av IL-2 Sturmovik: Great Battles på din dator och ändrar dem aldrig.

Ingenting från spelet följer med eller distribueras vidare: inga spelfiler, ingen spelkod, inga DLL-filer; testerna bygger själva varje fil de läser. Banorna den skriver stannar på din dator.

3DHeat IL-2 är inte knutet till eller godkänt av 1C Game Studios / 777 Studios. IL-2 Sturmovik och tillhörande namn och varumärken tillhör sina ägare.

Rättighetsinnehavare: öppna ett ärende på [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - vi svarar snabbt och tar bort vad som helst på begäran.

## Licens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Använder numpy (BSD-3-Clause) och, valfritt,
numba (BSD-2-Clause). `heat3d_update` är 3DHeat-verktygens gemensamma uppdaterare.
