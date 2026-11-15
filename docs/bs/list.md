---
title: "Pronalaženje mapa: list"
nav_order: 2
lang: bs
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Pronalaženje mapa: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Komandna linija ti je nova? Prvo pročitaj [Prije nego počneš](before-you-start.md).

1. Instaliraj jednom: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, otvori
   terminal u tom folderu i pokreni `python -m pip install -e .` (Python 3.10
   ili noviji; donosi numpy; `python -m pip install -e .[fast]` dodaje numba).
2. Pokreni `heat3d-il2-level list`.
3. Svaka mapa ispisuje jedan red, odvojen tabulatorima: njeno ime (ime koje `extract`
   uzima), igra (`Great Battles` ili `Korea` za [drugu igru](archives-without-table.md)), visinska mapa koju čita i
   gdje leži na Zemlji - njen okvir geografske širine/dužine iz uglova mape,
   ili prilagođavanje orijentirima koje je postavlja, ili "not placed on the earth".
   Posljednji red (na stderr) broji mape i navodi instalacije.

![list na sintetičkoj instalaciji](../assets/img/list.svg)

Slika je pokretanje na instalaciji izgrađenoj pomoću pisača iz testova
(`tests/synth.py`), a ne na igri.

## Gdje se instalacije pronalaze {#where-the-installs-are-found}

Preko Steama; inače `--game <folder>` (ponavljajuće, po jedan za svaku instalaciju) ili
varijabla okruženja `HEAT3D_IL2_GAME`. Instalacija je folder čiji `data`
drži arhive `Maps*.gtp`.

| Opcija | Šta radi |
|---|---|
| `--game FOLDER` | IL-2 folder; ponovi ga za više instalacija |

Izlazni status: 0 gotovo, 2 nije pronađena nijedna instalacija.
