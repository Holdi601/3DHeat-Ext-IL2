---
title: "Trobar mapes: list"
nav_order: 2
lang: "ca"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Trobar mapes: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game CARPETA ...]
python -m heat3d_ext_il2 list ...          el mateix, sense instal·lar-lo
```

Si ets nou amb la línia d'ordres, llegeix primer [Abans de començar](before-you-start.md).

1. Instal·la-la una vegada: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, obre
   una terminal en aquesta carpeta i executa `python -m pip install -e .` (Python 3.10
   o posterior; porta numpy; `python -m pip install -e .[fast]` hi afegeix numba).
2. Executa `heat3d-il2-level list`.
3. Cada mapa imprimeix una línia, separada per tabulacions: el seu nom (el nom que pren
   `extract`), el joc (`Great Battles`, o `Korea` per al [segon joc](archives-without-table.md)),
   el mapa d'alçades que llegeix, i on es troba a la Terra: la seva caixa de latitud/longitud
   a partir de les cantonades del mapa, o l'ajust per punts de referència que el col·loca, o
   «not placed on the earth» (no col·locat a la Terra). L'última línia (a stderr) compta els
   mapes i anomena les instal·lacions.

![list sobre una instal·lació sintètica](../assets/img/list.svg)

La imatge és una execució sobre una instal·lació construïda amb els escriptors de les proves
(`tests/synth.py`), no sobre el joc.

## On es troben les instal·lacions {#where-the-installs-are-found}

Per Steam; si no, `--game <carpeta>` (es pot repetir, un per instal·lació) o la variable
d'entorn `HEAT3D_IL2_GAME`. Una instal·lació és una carpeta amb una subcarpeta `data` que
conté arxius `Maps*.gtp`.

| Opció | Què fa |
|---|---|
| `--game CARPETA` | una carpeta d'IL-2; repeteix-la per a diverses instal·lacions |

Estat de sortida: 0 fet; 2 no s'ha trobat cap instal·lació.
