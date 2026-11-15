---
title: Hastighet, tester, villkor
nav_order: 7
lang: sv
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

Licensavtalet för IL-2 Sturmovik: Great Battles och IL-2 Series (1C Game
Studios / 777 Studios) **hittades inte**: inte i installationen (vars
`data/Licenses.txt` bara innehåller licenser från tredje part), inte på utgivarens sida,
och Steams EULA-sida laddades inte. Kontrollera det själv innan du förlitar dig på det.
Det här verktyget läser bara arkiven och ändrar dem aldrig. Nivåerna det skriver stannar på
din dator: **publicera dem aldrig**. Inget här levererar några speldata, och testerna bygger
varje fil de läser.

## Licens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Använder numpy (BSD-3-Clause) och, valfritt,
numba (BSD-2-Clause). `heat3d_update` är 3DHeat-verktygens gemensamma uppdaterare.
