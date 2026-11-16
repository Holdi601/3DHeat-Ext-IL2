---
title: "Kiirus, testid, tingimused"
nav_order: 7
lang: "et"
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

See tööriist loeb sinu enda IL-2 Sturmovik: Great Battles paigalduse arhiive sinu arvutis ega muuda neid kunagi.

Mängust ei tarnita ega levitata midagi: ei mängufaile, ei mängu koodi, ei DLL-faile; testid ehitavad iga loetava faili ise. Tema kirjutatud tasemed jäävad sinu arvutisse.

3DHeat IL-2 ei ole seotud ettevõttega 1C Game Studios / 777 Studios ega selle poolt heaks kiidetud. IL-2 Sturmovik ja sellega seotud nimed ning kaubamärgid kuuluvad nende omanikele.

Õiguste omajad: avage pöördumine aadressil [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - vastame kiiresti ja eemaldame soovi korral mida tahes.

## Litsents {#licence}

MIT - vaata [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Kasutab numpy'd (BSD-3-Clause) ja valikuliselt
numba'd (BSD-2-Clause). `heat3d_update` on 3DHeati tööriistade ühine uuendaja.
