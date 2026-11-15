---
title: "Karttojen etsiminen: list"
nav_order: 2
lang: fi
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Karttojen etsiminen: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          sama ilman asennusta
```

Uusi komentorivin kanssa? Lue ensin [Ennen aloittamista](before-you-start.md).

1. Asenna kerran: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, avaa pääte
   kyseisessä kansiossa ja suorita `python -m pip install -e .` (Python 3.10 tai uudempi;
   se tuo mukanaan numpy-kirjaston; `python -m pip install -e .[fast]` lisää numban).
2. Suorita `heat3d-il2-level list`.
3. Jokainen kartta tulostaa yhden rivin, sarkaimilla erotettuna: sen nimen (nimen, jonka `extract`
   ottaa), pelin (`Great Battles` tai `Korea` [toiselle pelille](archives-without-table.md)), korkeuskartan,
   jonka se lukee, ja sen, missä se on maapallolla – sen leveys- ja pituusasteen laatikon kartan kulmista,
   tai maamerkkisovituksen, joka sen sijoittaa, tai tekstin "not placed on the earth" (ei sijoitettu maapallolle).
   Viimeinen rivi (vakiovirheeseen) laskee kartat ja nimeää asennukset.

![list synteettisessä asennuksessa](../assets/img/list.svg)

Kuva on ajo asennuksella, jonka testit rakentavat (`tests/synth.py`), ei itse pelillä.

## Mistä asennukset löytyvät {#where-the-installs-are-found}

Steamin kautta; muuten `--game <folder>` (toistettavissa, yksi jokaista asennusta kohden) tai
ympäristömuuttuja `HEAT3D_IL2_GAME`. Asennus on kansio, jonka `data`-kansiossa on `Maps*.gtp`-arkistoja.

| Asetus | Tekee |
|---|---|
| `--game FOLDER` | IL-2-kansio; toista se useille asennuksille |

Poistumistila: 0 valmis, 2 asennusta ei löytynyt.
