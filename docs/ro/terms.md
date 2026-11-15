---
title: "Viteză, teste, condiții"
nav_order: 7
lang: ro
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Viteză, teste, condiții {#speed-tests-terms}

## Viteză {#speed}

Decodarea este în Python pur, dacă nu este instalat numba (`python -m pip install -e .[fast]`):
o hartă de mărime medie durează circa 15 s fără el și circa o secundă cu el; cea mai mare hartă,
câteva sute de milioane de eșantioane, circa 7 s cu el (prima rulare compilează și ea). Memoria
rămâne la un singur rând de sectoare plus grila de ieșire.

## Teste {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` construiește în cod arhive, hărți de înălțimi (un codificator al codecului de mai sus),
fișiere `height.hini` și arhive fără tabel de fișiere.

## Condițiile {#the-terms}

Acordul de licență al IL-2 Sturmovik: Great Battles și IL-2 Series (1C Game Studios / 777 Studios)
**nu a fost găsit**: nici în instalare (al cărei `data/Licenses.txt` conține doar licențe terțe), nici
pe site-ul editorului, iar pagina EULA Steam nu s-a încărcat. Verificați-l singur înainte de a vă baza pe
acest instrument. Instrumentul acesta doar citește arhivele și nu le modifică niciodată. Nivelurile pe care
le scrie rămân pe calculatorul dumneavoastră: **nu le publicați niciodată**. Nimic de aici nu livrează date
de joc, iar testele construiesc fiecare fișier pe care îl citesc.

## Licență {#licence}

MIT - vedeți [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Folosește numpy (BSD-3-Clause) și, opțional,
numba (BSD-2-Clause). `heat3d_update` este programul comun de actualizare al instrumentelor 3DHeat.
