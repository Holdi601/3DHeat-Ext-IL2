---
title: Ātrums, testi, noteikumi
nav_order: 7
lang: "lv"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Ātrums, testi, noteikumi {#speed-tests-terms}

## Ātrums {#speed}

Dekodēšana ir tīrs Python, ja vien nav uzstādīts numba (`python -m pip install -e .[fast]`):
vidēji liela karte aizņem apmēram 15 s bez tā un apmēram vienu sekundi ar to; lielākā karte, vairāki simti miljonu paraugu, apmēram 7 s ar to (pirmā palaišana arī kompilē). Atmiņā paliek viena sektoru rinda un izvades režģis.

## Testi {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` koda veidā izveido arhīvus, augstuma kartes (iepriekš aprakstītā kodeka kodētāju), `height.hini` failus un arhīvus bez failu tabulas.

## Noteikumi {#the-terms}

IL-2 Sturmovik: Great Battles un IL-2 Series (1C Game Studios / 777 Studios) licences līgums **netika atrasts**: ne uzstādījumā (kur `data/Licenses.txt` satur tikai trešo pušu licences), ne izdevēja vietnē, un Steam EULA lapa neielādējās. Pārbaudiet paši, pirms paļaujaties uz to.
Šis rīks tikai nolasa arhīvus un nekad tos nemaina. Līmeņi, ko tas raksta, paliek jūsu datorā: **nekad nepublicējiet tos**. Šeit nekas nepiegādā spēles datus, un testi veido katru failu, ko tie nolasa.

## Licence {#licence}

MIT - skat. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Izmanto numpy (BSD-3-Clause) un pēc izvēles numba (BSD-2-Clause). `heat3d_update` ir 3DHeat rīku kopīgais atjauninātājs.
