---
title: "Žemėlapių paieška: list"
nav_order: 2
lang: "lt"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Žemėlapių paieška: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

Nesate įpratę prie komandinės eilutės? Pirmiausia perskaitykite [Prieš pradedant](before-you-start.md).

1. Įdiekite vieną kartą: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, atidarykite
   terminalą tame aplanke ir vykdykite `python -m pip install -e .` (Python 3.10 ar naujesnė; kartu
   įdiegiama numpy; `python -m pip install -e .[fast]` prideda numba).
2. Vykdykite `heat3d-il2-level list`.
3. Kiekvienas žemėlapis išveda po vieną eilutę, atskirtą tabuliacija: jo pavadinimą (pavadinimą, kurį priima `extract`),
   žaidimą (`Great Battles` arba `Korea` [antrajam žaidimui](archives-without-table.md)), aukščiau
   nurodytą reljefo failą ir tai, kur jis yra žemės paviršiuje – jo platumos/ilgumos dėžę pagal žemėlapio kampus,
   arba orientyrų pritaikymą, kuris jį patalpina, arba „not placed on the earth“ (neįdėtas į žemės paviršių).
   Paskutinė eilutė (standartinėje klaidų išvestyje) suskaičiuoja žemėlapius ir nurodo įdiegimus.

![list ant sintetinio įdiegimo](../assets/img/list.svg)

Paveikslėlis – paleidimas ant įdiegimo, sukurto testais (`tests/synth.py`), o ne ant žaidimo.

## Kur randami įdiegimai {#where-the-installs-are-found}

Per Steam; kitu atveju `--game <folder>` (kartojama, po vieną kiekvienam įdiegimui) arba aplinkos kintamasis
`HEAT3D_IL2_GAME`. Įdiegimas – tai aplankas, kurio `data` turi `Maps*.gtp` archyvus.

| Parinktis | Ką daro |
|---|---|
| `--game FOLDER` | IL-2 aplankas; kartokite, jei yra keli įdiegimai |

Išeities kodas: 0 – baigta; 2 – įdiegimas nerastas.
