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

Dette værktøj læser arkiverne i din egen installation af IL-2 Sturmovik: Great Battles på din computer og ændrer dem aldrig.

Intet fra spillet følger med eller videredistribueres: ingen spilfiler, ingen spilkode, ingen DLL'er; testene bygger selv hver fil, de læser. De baner, den skriver, bliver på din maskine.

3DHeat IL-2 er ikke tilknyttet eller godkendt af 1C Game Studios / 777 Studios. IL-2 Sturmovik og tilhørende navne og varemærker tilhører deres ejere.

Rettighedshavere: opret et issue på [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - vi svarer hurtigt og fjerner hvad som helst på anmodning.

## Licens {#licence}

MIT - se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Bruger numpy (BSD-3-Clause) og, valgfrit,
numba (BSD-2-Clause). `heat3d_update` er 3DHeat-værktøjernes fælles opdaterer.
