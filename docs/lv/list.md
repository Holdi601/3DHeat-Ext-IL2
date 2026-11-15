---
title: "Karšu meklēšana: list"
nav_order: 2
lang: "lv"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Karšu meklēšana: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          tas pats, bez uzstādīšanas
```

Nekad neesat strādājis ar komandrindu? Vispirms izlasiet [Pirms sākat](before-you-start.md).

1. Uzstādiet vienreiz: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, atveriet
   termināli šajā mapē un palaidiet `python -m pip install -e .` (Python 3.10
   vai jaunāks; tas atnes numpy; `python -m pip install -e .[fast]` pievieno numba).
2. Palaidiet `heat3d-il2-level list`.
3. Katra karte izdrukā vienu rindu, atdalītu ar tabulācijas zīmi: tās nosaukumu (nosaukumu, ko pieņem `extract`), spēli (`Great Battles` vai `Korea` [otrajai spēlei](archives-without-table.md)), augstuma karti, ko tā nolasa, un to, kur tā atrodas uz zemes - tās platuma/garuma kasti no kartes stūriem, orientieru pieskaņojumu, kas to novieto, vai "not placed on the earth".
   Pēdējā rindā (standarta kļūdu izvadā) ir kartu skaits un uzstādījumu nosaukumi.

![list uz sintētiska uzstādījuma](../assets/img/list.svg)

Attēls ir palaišana uz uzstādījuma, kas veidots no testu rakstītājiem (`tests/synth.py`), nevis uz pašas spēles.

## Kur tiek atrasti uzstādījumi {#where-the-installs-are-found}

Caur Steam; citādi `--game <folder>` (var atkārtot, vienu katram uzstādījumam) vai vides mainīgais `HEAT3D_IL2_GAME`. Uzstādījums ir mape, kuras `data` mapē ir `Maps*.gtp` arhīvi.

| Iespēja | Ko dara |
|---|---|
| `--game FOLDER` | IL-2 mape; atkārto to vairākiem uzstādījumiem |

Izejas statuss: 0 pabeigts; 2 uzstādījums nav atrasts.
