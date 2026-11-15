---
title: "Kaartide leidmine: list"
nav_order: 2
lang: et
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Kaartide leidmine: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          sama, ilma paigaldamata
```

Pole sul käsurealt kogemust? Loe esmalt [Enne alustamist](before-you-start.md).

1. Paigalda üks kord: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, ava
   terminal selles kaustas ja käivita `python -m pip install -e .` (Python 3.10
   või uuem; see toob kaasa numpy; `python -m pip install -e .[fast]` lisab numba).
2. Käivita `heat3d-il2-level list`.
3. Iga kaart prindib ühe rea, tabulaatoritega eraldatud: tema nimi (nimi, mida `extract`
   võtab), mäng (`Great Battles` või `Korea` [teise mängu](archives-without-table.md) puhul), kõrgustikukaart, mida see loeb, ja see, kus ta maakeral asub — tema laiuskraadi/pikkuskraadi kast kaardi nurkadest, või maamärkide sobitus, mis ta paigutab, või "not placed on the earth". Viimane rida (standardveas) loeb kaardid kokku ja nimetab installid.

![list sünteetilisel installil](../assets/img/list.svg)

Pilt on käivitus installil, mis on ehitatud testide kirjutajatest
(`tests/synth.py`), mitte mängul.

## Kust installid leitakse {#where-the-installs-are-found}

Steami kaudu; muidu `--game <folder>` (korduv, üks iga install) või
keskkonnamuutuja `HEAT3D_IL2_GAME`. Install on kaust, mille `data`
hoiab `Maps*.gtp` arhiive.

| Valik | Teeb |
|---|---|
| `--game FOLDER` | IL-2 kaust; korda seda mitme installi jaoks |

Väljumisolek: 0 valmis, 2 installi ei leitud.
