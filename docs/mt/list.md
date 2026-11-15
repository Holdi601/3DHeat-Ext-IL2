---
title: "Insibu l-mapep: list"
nav_order: 2
lang: mt
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Insibu l-mapep: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Ġdid mal-linja tal-kmandi? Aqra [Qabel ma tibda](before-you-start.md) l-ewwel.

1. Installa darba: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, iftaħ
   terminal f'dak il-folder u ħaddem `python -m pip install -e .` (Python 3.10
   jew aktar ġdid; iġib miegħu numpy; `python -m pip install -e .[fast]` iżid numba).
2. Ħaddem `heat3d-il2-level list`.
3. Kull mappa tistampa linja waħda, separata bit-tabs: l-isem tagħha (l-isem li jieħu
   `extract`), il-logħba (`Great Battles`, jew `Korea` għal [it-tieni logħba](archives-without-table.md)), l-heightmap li taqra, u
   fejn tinsab fuq l-art - il-kaxxa tagħha tal-latitudni/lonġitudni mill-
   kantunieri tal-mappa, jew il-landmark fit li jqiegħdha, jew "not placed on the earth".
   L-aħħar linja (fuq stderr) tgħodd il-mapep u tisemmi l-installazzjonijiet.

![list fuq installazzjoni sintetika](../assets/img/list.svg)

L-istampa hija użu fuq installazzjoni mibnija mill-writers tat-testijiet
(`tests/synth.py`), mhux fuq il-logħba.

## Fejn jinstabu l-installazzjonijiet {#where-the-installs-are-found}

Permezz ta' Steam; inkella `--game <folder>` (jista' jiġi ripetut, wieħed għal kull installazzjoni) jew il-
variabbli tal-ambjent `HEAT3D_IL2_GAME`. Installazzjoni hija folder li l-`data` tiegħu
fih arkivji `Maps*.gtp`.

| Għażla | X'jagħmel |
|---|---|
| `--game FOLDER` | folder ta' IL-2; irrepetiha għal bosta installazzjonijiet |

Status tal-ħruġ: 0 lest, 2 ebda installazzjoni ma nstabet.
