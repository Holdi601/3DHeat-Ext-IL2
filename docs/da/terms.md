---
title: Hastighed, tests, vilkår
nav_order: 7
lang: "da"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Hastighed, tests, vilkår {#speed-tests-terms}

## Hastighed {#speed}

Afkodning er ren Python, medmindre numba er installeret (`python -m pip install -e .[fast]`):
et mellemstort kort tager cirka 15 s uden det og cirka et sekund med det; det
største kort, flere hundrede millioner prøver, cirka 7 s med det (den første
kørsel kompilerer også). Hukommelsen holder sig til én række sektorer plus outputgitteret.

## Tests {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` bygger arkiver, højdekort (en encoder for kodeken ovenfor),
`height.hini`-filer og arkiver uden filtabel i kode.

## Vilkårene {#the-terms}

Licensaftalen for IL-2 Sturmovik: Great Battles og IL-2 Series (1C Game
Studios / 777 Studios) blev **ikke fundet**: ikke i installationen (hvis
`data/Licenses.txt` kun holder tredjepartslicenser), ikke på udgiverens side,
og Steam-EULA-siden indlæstes ikke. Tjek den selv, før du stoler på dette.
Dette værktøj læser kun arkiverne og ændrer dem aldrig. De baner, det skriver, bliver
på din maskine: **offentliggør dem aldrig**. Intet her udgiver spildata, og
testene bygger hver fil, de læser.

## Licens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Bruger numpy (BSD-3-Clause) og, valgfrit,
numba (BSD-2-Clause). `heat3d_update` er 3DHeat-værktøjernes fælles opdaterer.
