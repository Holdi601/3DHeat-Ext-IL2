---
title: "Budowanie poziomów: extract"
nav_order: 3
lang: pl
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Budowanie poziomów: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Krok po kroku {#step-by-step}

Nigdy nie używałeś wiersza poleceń? Najpierw przeczytaj [Zanim zaczniesz](before-you-start.md).

1. Znajdź nazwę mapy poleceniem [`list`](list.md).
2. Uruchom `heat3d-il2-level extract <map> -o levels`. Nazwy mogą zawierać symbole wieloznaczne,
   w cudzysłowie (`"<family>_*"`); `--all` bierze każdą mapę.
3. Aby położyć nagranie na poziomie bez kroku ustawiania, podaj jego punkt początkowy:
   `--origin <lat> <lon>` ustawiony na `geo` nagrania (punkt odniesienia jego sesji). Bez tego
   początkiem jest środek mapy, a `geo` w `.json` mówi, który to jest.
4. Polecenie wypisuje linię na mapę, gdy ją dekoduje, a potem
   `ok <glb> <triangles> (<frame> frame)` albo `failed <map>: <why>`.
5. Wczytaj `<folder>/<map>/<map>.glb` w panelu **Tło / poziom** przeglądarki.

![extract na syntetycznej instalacji](../assets/img/extract.svg)

W metrach samej gry, bez wody:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Drugi przebieg po mapach, które już zapisano:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opcje {#options}

| Opcja | Domyślnie | Co robi |
|---|---|---|
| `maps` | - | nazwy map, tak jak wypisuje je `list`; symbole wieloznaczne dozwolone |
| `--all` | wyłączone | każda mapa; pory roku, które współdzielą mapę wysokości i mapę wody, są zapisywane raz |
| `-o`, `--out` | wymagane | folder wyjściowy; każda mapa trafia do `<out>/<map>/` |
| `--game FOLDER` | znajdowany | folder IL-2 (można powtarzać) |
| `--max-grid N` | `1024` | najwyżej tyle próbek mapy wysokości na bok (1024: około 2 milionów trójkątów); mapa jest próbkowana co *k* próbek, by się zmieściła |
| `--frame` `enu` albo `game` | `enu` | `enu`: metry na wschód, wysokość nad poziomem morza i na północ od `--origin`, jak tabele Tacview Watchera; `game`: własne metry gry (x na północ, y w górę, z na wschód). Mapa, której nie da się umieścić na Ziemi, jest zapisywana w `game`, o cokolwiek by poproszono |
| `--origin LAT LON` | środek mapy | początek układu `enu` (`geo` nagrania) |
| `--no-water` | wyłączone | pomija wodę |
| `--no-towns` | wyłączone | pomija obrysy miast |
| `--skip-existing` | wyłączone | pomija mapy, których `.glb` już istnieje |

Każda opcja, tak jak ją wypisuje program: [Opis poleceń](../cli-reference.md).

Ustaw `HEAT3D_DEBUG`, aby wypisać pełny ślad błędu nieudanej mapy. Plik `.glb` jest zapisywany jako
`<map>.glb.part` i zmieniany na właściwą nazwę po zakończeniu.

Kod wyjścia: 0 wszystkie mapy zapisane, 1 któraś się nie udała (pozostałe i tak są zapisane),
2 nie znaleziono instalacji albo żadna mapa nie pasowała.

## Przykłady {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # jedna mapa, układ enu wokół jej środka
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # na płaskiej mapie nagrania z tym geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # dokładniej, kilka map
heat3d-il2-level extract --all --skip-existing -o levels         # każda mapa, tylko nowe
heat3d-il2-level extract <map> --frame game -o levels            # własne metry gry, jak mają je pliki misji
```

Co jest w plikach: [Pliki poziomu i układy](output.md).
