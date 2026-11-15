---
title: "Mappen fannen: list"
nav_order: 2
lang: lb
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Mappen fannen: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Nei op der Kommandozeil? Liest fir d'éischt [Ier Dir ufänkt](before-you-start.md).

1. Eemol installéieren: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, e
   Terminal an deem Ordner opmaachen an `python -m pip install -e .` ausféieren (Python 3.10
   oder méi nei; et bréngt numpy mat; `python -m pip install -e .[fast]` füügt numba derbäi).
2. `heat3d-il2-level list` ausféieren.
3. All Map gëtt eng Zeil aus, mat Tab getrennt: säin Numm (den Numm, deen `extract`
   hëlt), d'Spill (`Great Battles`, oder `Korea` fir [dat zweet Spill](archives-without-table.md)), d'Heightmap, déi et liest, a
   wou et op der Äerd läit - seng Breeden-/Längtegrad-Këscht aus den Ecke vun der Map,
   oder de Landmark-Fit, deen et placéiert, oder "not placed on the earth".
   Déi lescht Zeil (op stderr) zielt d'Mappen a nennt d'Installatiounen.

![list op enger syntheteschen Installatioun](../assets/img/list.svg)

D'Bild ass en Duerchlaf op enger Installatioun, gebaut aus de Schreiwer vun den Tester
(`tests/synth.py`), net op dem Spill.

## Wou d'Installatioune fonnt ginn {#where-the-installs-are-found}

Iwwer Steam; soss `--game <folder>` (widderhuelbar, eng pro Installatioun) oder d'
Ëmgéigungsvariabel `HEAT3D_IL2_GAME`. Eng Installatioun ass en Ordner, dessen `data`
`Maps*.gtp`-Archiver hält.

| Optioun | Mécht |
|---|---|
| `--game FOLDER` | en IL-2-Ordner; widderhuelt et fir e puer Installatiounen |

Exit-Status: 0 fäerdeg, 2 keng Installatioun fonnt.
