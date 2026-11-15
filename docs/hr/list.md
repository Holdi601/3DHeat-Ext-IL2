---
title: "Pronalaženje karata: list"
nav_order: 2
lang: hr
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Pronalaženje karata: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          isto, bez instalacije
```

Ne znate ništa o naredbenom retku? Prvo pročitajte [Prije nego što počnete](before-you-start.md).

1. Instalirajte jednom: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, otvorite
   terminal u toj mapi i pokrenite `python -m pip install -e .` (Python 3.10
   ili noviji; donosi numpy; `python -m pip install -e .[fast]` dodaje numba).
2. Pokrenite `heat3d-il2-level list`.
3. Svaka karta ispisuje jedan redak, odvojen tabulatorima: ime (ime koje uzima `extract`), igru (`Great Battles`, ili `Korea` za [drugu igru](archives-without-table.md)), visinsku mapu koju čita i
   gdje leži na Zemlji - njezin okvir geografske širine/dužine iz kutova karte, ili prilagodbu prema orijentirima kojom se smješta, ili "not placed on the earth" (nije smještena na Zemlju).
   Zadnji redak (na stderr) broji karte i navodi instalacije.

![list na sintetičkoj instalaciji](../assets/img/list.svg)

Slika prikazuje pokretanje na instalaciji izgrađenoj od pisaca iz testova
(`tests/synth.py`), a ne na igri.

## Gdje se nalaze instalacije {#where-the-installs-are-found}

Preko Steama; inače `--game <folder>` (može se ponoviti, jedan po instalaciji) ili
varijabla okruženja `HEAT3D_IL2_GAME`. Instalacija je mapa čiji `data`
sadrži `Maps*.gtp` arhive.

| Opcija | Što radi |
|---|---|
| `--game FOLDER` | mapa IL-2; ponovite je za više instalacija |

Izlazni status: 0 gotovo, 2 nije pronađena nijedna instalacija.
