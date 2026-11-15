---
title: "Hľadanie máp: list"
nav_order: 2
lang: sk
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Hľadanie máp: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          to isté, bez inštalácie
```

Nikdy ste nepracovali s príkazovým riadkom? Najprv si prečítajte [Ako začať](before-you-start.md).

1. Nainštalujte raz: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, otvorte
   terminál v tom priečinku a spustite `python -m pip install -e .` (Python 3.10
   alebo novší; nainštaluje numpy; `python -m pip install -e .[fast]` pridá numba).
2. Spustite `heat3d-il2-level list`.
3. Každá mapa vypíše jeden riadok, oddelený tabulátormi: jej názov (názov, ktorý berie `extract`), hru (`Great Battles`, alebo `Korea` pre [druhú hru](archives-without-table.md)), výškovú mapu, ktorú číta, a
   kde leží na zemi – jej ohraničujúci box zemepisnej šírky a dĺžky z rohov mapy,
   alebo prispôsobenie orientačným bodom, ktoré ju umiestňuje, alebo „not placed on the earth“ (neumiestnená na zemi).
   Posledný riadok (na stderr) spočíta mapy a pomenuje inštalácie.

![list na syntetickej inštalácii](../assets/img/list.svg)

Obrázok je spustenie na inštalácii postavenej zapisovačmi z testov
(`tests/synth.py`), nie na hre.

## Kde sa inštalácie nachádzajú {#where-the-installs-are-found}

Cez Steam; inak `--game <folder>` (možno opakovať, jeden na inštaláciu) alebo
premenná prostredia `HEAT3D_IL2_GAME`. Inštalácia je priečinok, ktorého `data`
obsahuje archívy `Maps*.gtp`.

| Možnosť | Čo robí |
|---|---|
| `--game FOLDER` | priečinok IL-2; opakujte ho pre viac inštalácií |

Stavový kód: 0 hotovo, 2 nenájdená inštalácia.
