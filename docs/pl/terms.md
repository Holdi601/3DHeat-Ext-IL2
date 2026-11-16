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

To narzędzie odczytuje archiwa twojej własnej instalacji IL-2 Sturmovik: Great Battles na twoim komputerze i nigdy ich nie zmienia.

Nic z gry nie jest dołączane ani rozpowszechniane: żadnych plików gry, żadnego kodu gry, żadnych bibliotek DLL; testy same budują każdy plik, który czytają. Zapisane poziomy zostają na twoim komputerze.

3DHeat IL-2 nie jest powiązany z 1C Game Studios / 777 Studios ani przez nią wspierany. IL-2 Sturmovik oraz powiązane nazwy i znaki towarowe należą do ich właścicieli.

Właściciele praw: otwórzcie zgłoszenie pod adresem [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - odpowiadamy szybko i na prośbę usuwamy wszystko.

## Licencja {#licence}

MIT - zob. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Używa numpy (BSD-3-Clause) oraz, opcjonalnie,
numba (BSD-2-Clause). `heat3d_update` to wspólny moduł aktualizacji narzędzi 3DHeat.
