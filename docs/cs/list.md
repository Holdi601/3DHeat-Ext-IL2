---
title: "Hledání map: list"
nav_order: 2
lang: cs
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Hledání map: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Nikdy jste nepracovali s příkazovým řádkem? Nejdřív si přečtěte [Než začnete](before-you-start.md).

1. Nainstalujte jednou: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, otevřete
   terminál v této složce a spusťte `python -m pip install -e .` (Python 3.10
   nebo novější; přinese numpy; `python -m pip install -e .[fast]` přidá numba).
2. Spusťte `heat3d-il2-level list`.
3. Každá mapa vypíše jeden řádek oddělený tabulátory: její název (ten, který bere `extract`),
   hru (`Great Battles`, nebo `Korea` pro [druhou hru](archives-without-table.md)), výškovou
   mapu, kterou čte, a kde leží na Zemi – její box zeměpisné šířky a délky z rohů mapy,
   nebo přizpůsobení orientačním bodům, které ji umisťuje, nebo „not placed on the earth“ (neumístěno na Zemi).
   Poslední řádek (na stderr) počítá mapy a jmenuje instalace.

![list na syntetické instalaci](../assets/img/list.svg)

Obrázek je běh na instalaci vytvořené zapisovači z testů
(`tests/synth.py`), ne na hře.

## Kde se instalace hledají {#where-the-installs-are-found}

Přes Steam; jinak `--game <folder>` (lze opakovat, jedno na instalaci) nebo proměnná prostředí
`HEAT3D_IL2_GAME`. Instalace je složka, jejíž `data` obsahuje archivy `Maps*.gtp`.

| Možnost | Co dělá |
|---|---|
| `--game FOLDER` | složka IL-2; pro více instalací ji zopakujte |

Stavový kód: 0 hotovo, 2 nenalezena žádná instalace.
