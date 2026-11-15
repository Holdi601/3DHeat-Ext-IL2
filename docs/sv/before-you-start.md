---
title: Innan du börjar
nav_order: 1.5
lang: sv
source: before-you-start.md
source_hash: "9e62d9ba2baa"
nav_exclude: true
search_exclude: true
---
# Innan du börjar {#before-you-start}

Har du aldrig använt kommandoraden förut? Den här sidan tar dig från noll till en första körning.
Det tar ungefär tio minuter, en gång.

## 1. Installera Python {#install-python}

Det här verktyget behöver **Python 3.10 eller senare**.

- **Windows:** ladda ner Python från [python.org/downloads](https://www.python.org/downloads/)
  och kör installationsprogrammet. På första skärmen kryssar du i **Add python.exe to PATH**,
  och klickar sedan på **Install Now**.
- **macOS och Linux:** Python 3 finns ofta redan. Där sidorna säger `python`, skriv `python3`.

## 2. Hämta verktyget {#get-this-tool}

Öppna [github.com/Holdi601/3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2), klicka på den
gröna knappen **Code**, sedan på **Download ZIP**, och packa upp filen i en mapp du väljer. Använder du git: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`.

## 3. Öppna en terminal i mappen {#open-a-terminal-in-that-folder}

En terminal är ett fönster där du skriver kommandon.

- **Windows:** öppna mappen i Utforskaren, klicka i adressfältet, skriv `powershell` och tryck på Enter. Ett blått eller svart fönster öppnas, redan i den mappen.
- **macOS:** öppna **Terminal**, skriv `cd ` (med ett mellanslag), dra mappen till fönstret och tryck på Enter.

`cd` betyder "byt mapp": `cd C:\Tools\3DHeat-Ext-IL2` går till den mappen.

## 4. Installera verktyget {#install-the-tool}

Skriv det här och tryck på Enter:

```bash
python -m pip install -e .
```

Till slut ska du se: `Successfully installed heat3d-ext-il2-...`.

## 5. Kör det {#run-it}

```bash
heat3d-il2-level list
```

Du bör se något i stil med:

```text
<map>	Great Battles	height /graphics/<map>/height.dat	<lat>..<lat> N, <lon>..<lon> E
<n> maps in C:\Games\IL-2 Sturmovik Great Battles
```

Nästa steg: [Hitta kartor: list](list.md), sedan [Bygga nivåer: extract](extract.md).

## Så läser du kommandona på de här sidorna {#how-to-read-the-commands-on-these-pages}

| Du ser | Det betyder |
|---|---|
| `<folder>` | en platshållare: skriv ditt eget värde i stället, utan `< >` |
| `[--force]` | valfritt: utelämna det, eller skriv det som det står |
| `a\|b` | ett val: skriv `a` eller `b` |
| `# a note` | en kommentar till dig: skriv inte av den |
| `"C:\My Files\x"` | sätt en sökväg med mellanslag inom citattecken |
| `D:\Demos` | en exempelmapp i Windows: använd din egen |

## När något går fel {#when-something-goes-wrong}

| Meddelandet | Gör så här |
|---|---|
| `'python' is not recognized` | Python är inte installerat, eller rutan PATH var inte ikryssad: installera om och kryssa i den (eller skriv `py` i stället för `python`). |
| `'heat3d-il2-level' is not recognized` | Kör steg 4 igen i verktygets mapp, eller skriv `python -m heat3d_ext_il2` i stället för `heat3d-il2-level`: det gör samma sak. |
| `No module named heat3d_ext_il2` | Du står inte i verktygets mapp, eller steg 4 misslyckades: gå dit med `cd` och kör steg 4. |
| `No module named pip` | Kör `python -m ensurepip`, och sedan steg 4. |
| något annat | Läs sista raden i meddelandet och öppna ett ärende på GitHub med den raden. |

Varje kommando avslutas också med en **avslutskod**: 0 betyder att det lyckades. För att se den,
skriv `echo $LASTEXITCODE` i PowerShell eller `echo $?` på macOS och Linux.
