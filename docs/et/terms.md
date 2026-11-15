---
title: "Kiirus, testid, tingimused"
nav_order: 7
lang: et
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Kiirus, testid, tingimused {#speed-tests-terms}

## Kiirus {#speed}

Dekodeerimine on puhas Python, kui numba pole paigaldatud (`python -m pip install -e .[fast]`):
keskmise suurusega kaart võtab ilma selleta umbes 15 s ja koos sellega umbes sekundi;
suurim kaart, mitu sada miljonit proovi, umbes 7 s koos sellega (esimene
käivitus kompileerib ka). Mälu jääb ühele sektorite reale ja väljundruudustikule.

## Testid {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` koostab koodis arhiivid, kõrgustikukaardid (ülal oleva kodeki kodeerija),
`height.hini` failid ja arhiivid ilma failitabelita.

## Tingimused {#the-terms}

IL-2 Sturmovik: Great Battles'i ja IL-2 Series'i (1C Game Studios / 777 Studios)
litsentsileping **ei leitud**: mitte installist (kus `data/Licenses.txt` sisaldab ainult kolmanda osapoole litsentse), mitte kirjastaja saidilt ja Steami EULA leht ei laadinud. Kontrolli seda ise, enne kui sellele toetud. See tööriist ainult loeb arhiive ja ei muuda neid kunagi. Tasemed, mida see kirjutab, jäävad
sinu masinasse: **ära kunagi avalda neid**. Siin ei ole ühtegi mängu andmeid kaasas ja
testid koostavad kõik failid, mida nad loevad.

## Litsents {#licence}

MIT - vaata [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Kasutab numpy'd (BSD-3-Clause) ja valikuliselt
numba'd (BSD-2-Clause). `heat3d_update` on 3DHeati tööriistade ühine uuendaja.
