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

Šis rīks lasa tavas IL-2 Sturmovik: Great Battles instalācijas arhīvus tavā datorā un nekad tos nemaina.

No spēles nekas netiek piegādāts vai izplatīts tālāk: nekādu spēles failu, nekāda spēles koda, nekādu DLL; testi paši izveido katru failu, ko tie lasa. Līmeņi, ko tas uzraksta, paliek tavā datorā.

3DHeat IL-2 nav saistīts ar 1C Game Studios / 777 Studios un to neatbalsta 1C Game Studios / 777 Studios. IL-2 Sturmovik un saistītie nosaukumi un preču zīmes pieder to īpašniekiem.

Tiesību īpašnieki: atveriet pieteikumu vietnē [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - mēs atbildam ātri un pēc pieprasījuma noņemam jebko.

## Licence {#licence}

MIT - skat. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Izmanto numpy (BSD-3-Clause) un pēc izvēles numba (BSD-2-Clause). `heat3d_update` ir 3DHeat rīku kopīgais atjauninātājs.
