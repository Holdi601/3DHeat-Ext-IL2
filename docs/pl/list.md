---
title: "Szukanie map: list"
nav_order: 2
lang: pl
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Szukanie map: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          to samo, bez instalowania
```

Nigdy nie używałeś wiersza poleceń? Najpierw przeczytaj [Zanim zaczniesz](before-you-start.md).

1. Zainstaluj raz: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, otwórz
   terminal w tym folderze i uruchom `python -m pip install -e .` (Python 3.10
   lub nowszy; instaluje numpy; `python -m pip install -e .[fast]` dodaje numba).
2. Uruchom `heat3d-il2-level list`.
3. Każda mapa wypisuje jedną linię, oddzieloną tabulatorami: jej nazwę (nazwę, którą przyjmuje `extract`),
   grę (`Great Battles` albo `Korea` dla [drugiej gry](archives-without-table.md)), mapę wysokości, z której
   czyta, oraz miejsce na Ziemi - jej prostokąt szerokości/długości geograficznej z rogów mapy,
   albo dopasowanie do punktów orientacyjnych, które ją umieszcza, albo „not placed on the earth”
   (nie umieszczona na Ziemi). Ostatnia linia (na stderr) liczy mapy i podaje nazwy instalacji.

![list na syntetycznej instalacji](../assets/img/list.svg)

Obrazek to przebieg na instalacji zbudowanej przez piszące ją testy (`tests/synth.py`), a nie na samej grze.

## Gdzie są szukane instalacje {#where-the-installs-are-found}

Przez Steam; w przeciwnym razie `--game <folder>` (można powtarzać, jeden na instalację) albo
zmienna środowiskowa `HEAT3D_IL2_GAME`. Instalacja to folder, którego `data`
zawiera archiwa `Maps*.gtp`.

| Opcja | Co robi |
|---|---|
| `--game FOLDER` | folder IL-2; powtórz, by podać kilka instalacji |

Kod wyjścia: 0 gotowe, 2 nie znaleziono instalacji.
