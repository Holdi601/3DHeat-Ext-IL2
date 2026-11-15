---
title: "Rychlost, testy, podmínky"
nav_order: 7
lang: cs
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Rychlost, testy, podmínky {#speed-tests-terms}

## Rychlost {#speed}

Dekódování je čistý Python, pokud není nainstalována numba (`python -m pip install -e .[fast]`):
střední mapa trvá bez ní zhruba 15 s a s ní zhruba jednu sekundu; největší mapa, několik set
milionů vzorků, zhruba 7 s s ní (první běh také kompiluje). Paměť zůstává na jednom řádku sektorů
plus výstupní mřížce.

## Testy {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` vytváří v kódu archivy, výškové mapy (kodér výše popsaného kodeku),
soubory `height.hini` a archivy bez tabulky souborů.

## Podmínky {#the-terms}

Licenční smlouva IL-2 Sturmovik: Great Battles a IL-2 Series (1C Game
Studios / 777 Studios) **nebyla nalezena**: ani v instalaci (jejíž
`data/Licenses.txt` obsahuje jen licence třetích stran), ani na webu vydavatele,
a stránka EULA na Steamu se nenačetla. Ověřte si ji sami, než se na to spolehnete.
Tento nástroj jen čte archivy a nikdy je nemění. Úrovně, které zapisuje, zůstávají
na vašem počítači: **nikdy je nezveřejňujte**. Tento nástroj nedodává žádná herní data
a testy si vytvářejí každý soubor, který čtou.

## Licence {#licence}

MIT – viz [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Používá numpy (BSD-3-Clause) a volitelně
knihovnu numba (BSD-2-Clause). `heat3d_update` je sdílený aktualizátor nástrojů 3DHeat.
