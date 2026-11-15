---
title: "Gjetja e hartave: list"
nav_order: 2
lang: "sq"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Gjetja e hartave: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Je i ri me rreshtin e komandave? Lexo së pari [Para se të fillosh](before-you-start.md).

1. Instalo një herë: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, hap
   një terminal në atë dosje dhe ekzekuto `python -m pip install -e .` (Python 3.10
   ose më i ri; sjell numpy; `python -m pip install -e .[fast]` shton numba).
2. Ekzekuto `heat3d-il2-level list`.
3. Çdo hartë shtyp një rresht, e ndarë me tab: emrin e saj (emri që e merr `extract`),
   lojën (`Great Battles`, ose `Korea` për [lojën e dytë](archives-without-table.md)), heightmap që lexon, dhe
   ku shtrihet mbi tokë - kutia e gjerësisë/gjatësisë gjeografike nga
   qoshet e hartës, ose përshtatja me pika referimi që e vendos, ose "not placed on the earth".
   Rreshti i fundit (në stderr) numëron hartat dhe emërton instalimet.

![list mbi një instalim sintetik](../assets/img/list.svg)

Pamja është një ekzekutim mbi një instalim të ndërtuar nga shkruesit e testeve
(`tests/synth.py`), jo mbi lojën.

## Ku gjenden instalimet {#where-the-installs-are-found}

Përmes Steam; përndryshe `--game <folder>` (i përsëritshëm, një për instalim) ose
ndryshorja e mjedisit `HEAT3D_IL2_GAME`. Një instalim është një dosje `data` e së cilës
mban arkiva `Maps*.gtp`.

| Opsioni | Çfarë bën |
|---|---|
| `--game FOLDER` | një dosje IL-2; përsërite për disa instalime |

Statusi i daljes: 0 u krye, 2 nuk u gjet instalim.
