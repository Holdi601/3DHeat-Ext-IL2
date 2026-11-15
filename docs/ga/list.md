---
title: "Léarscáileanna a aimsiú: list"
nav_order: 2
lang: ga
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Léarscáileanna a aimsiú: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

An bhfuil tú nua leis an líne ordaithe? Léigh [Sula dtosaíonn tú](before-you-start.md) ar dtús.

1. Suiteáil uair amháin: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, oscail
   teirminéal sa fhillteán sin agus rith `python -m pip install -e .` (Python 3.10
   nó níos nuaí; tugann sé numpy leis; cuireann `python -m pip install -e .[fast]` numba leis).
2. Rith `heat3d-il2-level list`.
3. Priontálann gach léarscáil líne amháin, scartha le táib: a hainm (an t-ainm a ghlacann
   `extract`), an cluiche (`Great Battles`, nó `Korea` don [dara cluiche](archives-without-table.md)), an léarscáil airde a léann sí, agus
   an áit a luíonn sí ar an domhan - a bosca domhanleithid/domhanfhad ó choirnéil na léarscáile,
   nó an feistiú tírdhreacha a chuireann ar an domhan í, nó "not placed on the earth".
   Comhairíonn an líne dheireanach (ar stderr) na léarscáileanna agus ainmníonn na suiteálacha.

![list ar shuiteáil sintéiseach](../assets/img/list.svg)

Is rith é an pictiúr ar shuiteáil a tógadh ó scríbhneoirí na dtástálacha
(`tests/synth.py`), ní ar an gcluiche.

## An áit a n-aimsítear na suiteálacha {#where-the-installs-are-found}

Trí Steam; ar shlí eile `--game <folder>` (is féidir é a athdhéanamh, ceann in aghaidh na suiteála) nó an
athróg timpeallachta `HEAT3D_IL2_GAME`. Is fillteán é suiteáil a bhfuil cartlanna `Maps*.gtp`
ina `data`.

| Rogha | Cad a dhéanann sí |
|---|---|
| `--game FOLDER` | fillteán IL-2; athdhéan é do roinnt suiteálacha |

Stádas scoir: 0 déanta, 2 gan suiteáil aimsithe.
