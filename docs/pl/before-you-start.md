---
title: "Zanim zaczniesz"
nav_order: 1.5
lang: pl
source: before-you-start.md
source_hash: "9e62d9ba2baa"
nav_exclude: true
search_exclude: true
---
# Zanim zaczniesz {#before-you-start}

Nigdy nie używałeś wiersza poleceń? Ta strona przeprowadzi cię od zera do pierwszego uruchomienia.
Zajmie to około dziesięciu minut, tylko raz.

## 1. Zainstaluj Pythona {#install-python}

To narzędzie wymaga **Pythona 3.10 lub nowszego**.

- **Windows:** pobierz Pythona ze strony [python.org/downloads](https://www.python.org/downloads/)
  i uruchom instalator. Na jego pierwszym ekranie zaznacz **Add python.exe to PATH**,
  a potem kliknij **Install Now**.
- **macOS i Linux:** Python 3 często jest już zainstalowany. Tam, gdzie te strony piszą
  `python`, wpisz `python3`.

## 2. Pobierz to narzędzie {#get-this-tool}

Otwórz [github.com/Holdi601/3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2), kliknij
zielony przycisk **Code**, potem **Download ZIP**, i rozpakuj plik do wybranego folderu. Jeśli używasz gita:
`git clone https://github.com/Holdi601/3DHeat-Ext-IL2`.

## 3. Otwórz terminal w tym folderze {#open-a-terminal-in-that-folder}

Terminal to okno, w którym wpisujesz polecenia.

- **Windows:** otwórz folder w Eksploratorze, kliknij w pasek adresu, wpisz
  `powershell` i naciśnij Enter. Otworzy się niebieskie lub czarne okno, już w tym folderze.
- **macOS:** otwórz **Terminal**, wpisz `cd ` (ze spacją), przeciągnij folder do
  okna i naciśnij Enter.

`cd` znaczy „zmień folder”: `cd C:\Tools\3DHeat-Ext-IL2` przechodzi do tego folderu.

## 4. Zainstaluj narzędzie {#install-the-tool}

Wpisz to i naciśnij Enter:

```bash
python -m pip install -e .
```

Na końcu powinieneś zobaczyć: `Successfully installed heat3d-ext-il2-...`.

## 5. Uruchom je {#run-it}

```bash
heat3d-il2-level list
```

Powinieneś zobaczyć mniej więcej taki wynik:

```text
<map>	Great Battles	height /graphics/<map>/height.dat	<lat>..<lat> N, <lon>..<lon> E
<n> maps in C:\Games\IL-2 Sturmovik Great Battles
```

Dalej: [Szukanie map: list](list.md), potem [Budowanie poziomów: extract](extract.md).

## Jak czytać polecenia na tych stronach {#how-to-read-the-commands-on-these-pages}

| Widzisz | Znaczy to |
|---|---|
| `<folder>` | symbol zastępczy: wpisz zamiast niego własną wartość, bez `< >` |
| `[--force]` | opcjonalne: pomiń to albo wpisz tak, jak pokazano |
| `a\|b` | wybór: wpisz `a` albo `b` |
| `# a note` | komentarz dla ciebie: nie wpisuj tego |
| `"C:\My Files\x"` | ścieżkę ze spacjami wpisz w cudzysłowie |
| `D:\Demos` | przykładowy folder Windows: użyj własnego |

## Gdy coś pójdzie nie tak {#when-something-goes-wrong}

| Komunikat | Co zrobić |
|---|---|
| `'python' is not recognized` | Python nie jest zainstalowany albo nie zaznaczono PATH: zainstaluj go ponownie i zaznacz tę opcję (lub wpisz `py` zamiast `python`). |
| `'heat3d-il2-level' is not recognized` | Uruchom krok 4 ponownie w folderze narzędzia albo wpisz `python -m heat3d_ext_il2` zamiast `heat3d-il2-level`: zrobi to samo. |
| `No module named heat3d_ext_il2` | Nie jesteś w folderze narzędzia albo krok 4 się nie udał: wejdź tam poleceniem `cd` i uruchom krok 4. |
| `No module named pip` | Uruchom `python -m ensurepip`, a potem krok 4. |
| coś innego | Przeczytaj ostatni wiersz komunikatu i zgłoś go, zakładając zgłoszenie (issue) na GitHubie. |

Każde polecenie kończy się też **kodem wyjścia**: 0 znaczy, że się udało. Aby go zobaczyć,
wpisz `echo $LASTEXITCODE` w PowerShellu albo `echo $?` na macOS i Linuksie.
