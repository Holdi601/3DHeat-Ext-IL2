---
title: "Szybkość, testy, warunki"
nav_order: 7
lang: "pl"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Szybkość, testy, warunki {#speed-tests-terms}

## Szybkość {#speed}

Dekodowanie jest czystym Pythonem, chyba że zainstalowano numba (`python -m pip install -e .[fast]`):
średnia mapa zajmuje około 15 s bez niego i około sekundy z nim; największa mapa, kilkaset milionów próbek,
około 7 s z nim (pierwsze uruchomienie też kompiluje). Pamięć to jeden wiersz sektorów plus siatka wyjściowa.

## Testy {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` buduje w kodzie archiwa, mapy wysokości (koder wspomnianego wyżej kodeka),
pliki `height.hini` oraz archiwa bez tabeli plików.

## Warunki {#the-terms}

Umowa licencyjna IL-2 Sturmovik: Great Battles i IL-2 Series (1C Game
Studios / 777 Studios) **nie została znaleziona**: nie ma jej w instalacji (której
`data/Licenses.txt` zawiera tylko licencje stron trzecich), nie ma jej na stronie wydawcy,
a strona EULA Steam się nie wczytała. Sprawdź ją samodzielnie, zanim na tym polegasz.
To narzędzie tylko czyta archiwa i nigdy ich nie zmienia. Poziomy, które zapisuje, zostają
na twoim komputerze: **nigdy ich nie publikuj**. Nic tutaj nie dostarcza żadnych danych gry,
a testy budują każdy plik, który czytają.

## Licencja {#licence}

MIT - zob. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Używa numpy (BSD-3-Clause) oraz, opcjonalnie,
numba (BSD-2-Clause). `heat3d_update` to wspólny moduł aktualizacji narzędzi 3DHeat.
