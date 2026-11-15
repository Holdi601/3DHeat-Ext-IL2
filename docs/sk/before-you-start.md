---
title: "Ako začať"
nav_order: 1.5
lang: "sk"
source: before-you-start.md
source_hash: "9e62d9ba2baa"
nav_exclude: true
search_exclude: true
---
# Ako začať {#before-you-start}

Nikdy ste nepracovali s príkazovým riadkom? Táto stránka vás previedie od nuly až po prvé spustenie.
Trvá to asi desať minút, a len raz.

## 1. Nainštalujte Python {#install-python}

Tento nástroj potrebuje **Python 3.10 alebo novší**.

- **Windows:** stiahnite Python z [python.org/downloads](https://www.python.org/downloads/)
  a spustite inštalátor. Na jeho prvej obrazovke zaškrtnite **Add python.exe to PATH**,
  potom kliknite na **Install Now**.
- **macOS a Linux:** Python 3 tam často už je. Tam, kde tieto stránky píšu
  `python`, napíšte `python3`.

## 2. Získajte tento nástroj {#get-this-tool}

Otvorte [github.com/Holdi601/3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2), kliknite na
zelené tlačidlo **Code**, potom na **Download ZIP**, a rozbaľte ho do priečinka podľa vlastného výberu. Ak používate git: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`.

## 3. Otvorte terminál v tom priečinku {#open-a-terminal-in-that-folder}

Terminál je okno, do ktorého píšete príkazy.

- **Windows:** otvorte priečinok v Prieskumníkovi, kliknite do panela s adresou, napíšte
  `powershell` a stlačte Enter. Otvorí sa modré alebo čierne okno, ktoré už je v tom priečinku.
- **macOS:** otvorte **Terminal**, napíšte `cd ` (s medzerou), presuňte priečinok do
  okna a stlačte Enter.

`cd` znamená „zmeniť priečinok“: `cd C:\Tools\3DHeat-Ext-IL2` prejde do tohto priečinka.

## 4. Nainštalujte nástroj {#install-the-tool}

Napíšte tento príkaz a stlačte Enter:

```bash
python -m pip install -e .
```

Na konci by ste mali vidieť: `Successfully installed heat3d-ext-il2-...`.

## 5. Spustite ho {#run-it}

```bash
heat3d-il2-level list
```

Malo by sa zobraziť niečo takéto:

```text
<map>	Great Battles	height /graphics/<map>/height.dat	<lat>..<lat> N, <lon>..<lon> E
<n> maps in C:\Games\IL-2 Sturmovik Great Battles
```

Ďalej: [Hľadanie máp: list](list.md), potom [Vytváranie úrovní: extract](extract.md).

## Ako čítať príkazy na týchto stránkach {#how-to-read-the-commands-on-these-pages}

| Vidíte | Znamená to |
|---|---|
| `<folder>` | zástupný znak: namiesto neho napíšte svoju hodnotu, bez `< >` |
| `[--force]` | voliteľné: môžete ho vynechať, alebo ho napísať tak, ako je uvedené |
| `a\|b` | voľba: napíšte `a` alebo `b` |
| `# a note` | poznámka pre vás: nepíšte ju |
| `"C:\My Files\x"` | cestu, ktorá obsahuje medzery, dajte do úvodzoviek |
| `D:\Demos` | príklad priečinka vo Windows: použite svoj vlastný |

## Keď niečo nevyjde {#when-something-goes-wrong}

| Správa | Čo robiť |
|---|---|
| `'python' is not recognized` | Python nie je nainštalovaný alebo nebolo zaškrtnuté políčko PATH: nainštalujte ho znova a zaškrtnite ho (alebo napíšte `py` namiesto `python`). |
| `'heat3d-il2-level' is not recognized` | Spustite krok 4 znova v priečinku nástroja, alebo napíšte `python -m heat3d_ext_il2` namiesto `heat3d-il2-level`: urobí to isté. |
| `No module named heat3d_ext_il2` | Nie ste v priečinku nástroja alebo krok 4 zlyhal: prejdite tam príkazom `cd` a spustite krok 4. |
| `No module named pip` | Spustite `python -m ensurepip`, potom krok 4. |
| čokoľvek iné | Prečítajte si posledný riadok správy a potom s ním otvorte problém na GitHube. |

Každý príkaz tiež končí **stavovým kódom**: 0 znamená, že to fungovalo. Ak ho chcete vidieť,
napíšte `echo $LASTEXITCODE` v PowerShelli alebo `echo $?` na macOS a Linuxe.
