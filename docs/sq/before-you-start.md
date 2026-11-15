---
title: "Para se të fillosh"
nav_order: 1.5
lang: "sq"
source: before-you-start.md
source_hash: "9e62d9ba2baa"
nav_exclude: true
search_exclude: true
---
# Para se të fillosh {#before-you-start}

Je i ri me rreshtin e komandave? Kjo faqe të çon nga zero te një ekzekutim i parë.
Duhen rreth dhjetë minuta, vetëm një herë.

## 1. Instalo Python {#install-python}

Ky mjet kërkon **Python 3.10 ose më të ri**.

- **Windows:** shkarko Python nga [python.org/downloads](https://www.python.org/downloads/)
  dhe nis instaluesin. Në ekranin e parë, zgjidh **Add python.exe to PATH**,
  pastaj kliko **Install Now**.
- **macOS dhe Linux:** Python 3 shpesh është tashmë aty. Kudo ku këto faqe thonë
  `python`, shkruaj `python3`.

## 2. Merr këtë mjet {#get-this-tool}

Hap [github.com/Holdi601/3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2), kliko butonin
jeshil **Code**, pastaj **Download ZIP**, dhe shpaketoje në një dosje të zgjedhjes tënde.
Nëse përdor git: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`.

## 3. Hap një terminal në atë dosje {#open-a-terminal-in-that-folder}

Terminali është një dritare ku shkruan komanda.

- **Windows:** hap dosjen në Explorer, kliko te shiriti i adresës, shkruaj
  `powershell` dhe shtyp Enter. Hapet një dritare blu ose e zezë, tashmë brenda asaj
  dosjeje.
- **macOS:** hap **Terminal**, shkruaj `cd ` (me një hapësirë), tërhiq dosjen në
  dritare dhe shtyp Enter.

`cd` do të thotë "ndrysho dosjen": `cd C:\Tools\3DHeat-Ext-IL2` shkon te ajo dosje.

## 4. Instalo mjetin {#install-the-tool}

Shkruaj këtë dhe shtyp Enter:

```bash
python -m pip install -e .
```

Në fund duhet të shohësh: `Successfully installed heat3d-ext-il2-...`.

## 5. Ekzekutoje {#run-it}

```bash
heat3d-il2-level list
```

Duhet të shohësh diçka të tillë:

```text
<map>	Great Battles	height /graphics/<map>/height.dat	<lat>..<lat> N, <lon>..<lon> E
<n> maps in C:\Games\IL-2 Sturmovik Great Battles
```

Më pas: [Gjetja e hartave: list](list.md), pastaj [Ndërtimi i niveleve: extract](extract.md).

## Si t'i lexo komandat në këto faqe {#how-to-read-the-commands-on-these-pages}

| Çfarë sheh | Çfarë do të thotë |
|---|---|
| `<folder>` | një vendmbajtës: shkruaj vlerën tënde në vend të tij, pa `< >` |
| `[--force]` | opsional: lëre jashtë ose shkruaje siç është shfaqur |
| `a\|b` | një zgjedhje: shkruaj `a` ose `b` |
| `# a note` | një koment për ty: mos e shkruaj |
| `"C:\My Files\x"` | vendose në thonjëza një shteg që ka hapësira |
| `D:\Demos` | një dosje shembull në Windows: përdor të tënden |

## Kur diçka shkon keq {#when-something-goes-wrong}

| Mesazhi | Çfarë të bësh |
|---|---|
| `'python' is not recognized` | Python nuk është instaluar, ose kutia PATH nuk u zgjodh: instaloje përsëri dhe zgjidhe (ose shkruaj `py` në vend të `python`). |
| `'heat3d-il2-level' is not recognized` | Ekzekuto sërish hapin 4 në dosjen e mjetit, ose shkruaj `python -m heat3d_ext_il2` në vend të `heat3d-il2-level`: bën të njëjtën gjë. |
| `No module named heat3d_ext_il2` | Nuk je në dosjen e mjetit, ose hapi 4 dështoi: bëj `cd` atje dhe ekzekuto hapin 4. |
| `No module named pip` | Ekzekuto `python -m ensurepip`, pastaj hapin 4. |
| çdo gjë tjetër | Lexo rreshtin e fundit të mesazhit, pastaj hap një issue në GitHub me të. |

Çdo komandë përfundon edhe me një **status dalje**: 0 do të thotë se funksionoi. Për ta parë,
shkruaj `echo $LASTEXITCODE` në PowerShell ose `echo $?` në macOS dhe Linux.
