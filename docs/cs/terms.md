---
title: "Rychlost, testy, podmínky"
nav_order: 7
lang: "cs"
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

Tento nástroj čte archivy vaší vlastní instalace IL-2 Sturmovik: Great Battles na vašem počítači a nikdy je nemění.

Nic ze hry se nedodává ani dále nešíří: žádné soubory hry, žádný kód hry, žádné knihovny DLL; testy si každý soubor, který čtou, vytvoří samy. Úrovně, které zapíše, zůstávají na vašem počítači.

3DHeat IL-2 není přidružen k 1C Game Studios / 777 Studios ani jím schválen. IL-2 Sturmovik a související názvy a ochranné známky patří jejich vlastníkům.

Držitelé práv: založte hlášení na [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - odpovídáme rychle a na požádání cokoli odstraníme.

## Licence {#licence}

MIT – viz [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Používá numpy (BSD-3-Clause) a volitelně
knihovnu numba (BSD-2-Clause). `heat3d_update` je sdílený aktualizátor nástrojů 3DHeat.
