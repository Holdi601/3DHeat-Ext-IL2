---
title: "Greitis, testai, sąlygos"
nav_order: 7
lang: lt
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Greitis, testai, sąlygos {#speed-tests-terms}

## Greitis {#speed}

Dekodavimas yra gryname Python, nebent įdiegta numba (`python -m pip install -e .[fast]`):
vidutinio dydžio žemėlapis be jos užtrunka apie 15 s, su ja – apie sekundę; didžiausias žemėlapis, kelios šimtai milijonų mėginių,
su ja – apie 7 s (pirmas paleidimas taip pat kompiliuoja). Atmintis lieka viena sektorių eilutė ir išvesties tinklelis.

## Testai {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` kode sukuria archyvus, reljefo žemėlapius (kodeko kodavimo įrankis, aprašytas aukščiau), `height.hini` failus
ir archyvus be failų lentelės.

## Sąlygos {#the-terms}

IL-2 Sturmovik: Great Battles ir IL-2 Series (1C Game Studios / 777 Studios) licencijavimo sutartis **nerasta**: nei
įdiegime (kurio `data/Licenses.txt` turi tik trečiųjų šalių licencijas), nei leidėjo svetainėje, o Steam EULA puslapis
neįsikrovė. Patikrinkite pats, prieš tai pasikliaudami.
Šis įrankis tik skaito archyvus ir jų niekada nekeičia. Lygiai, kuriuos jis įrašo, lieka
jūsų kompiuteryje: **niekada jų neskelbkite**. Čia joks žaidimo duomenų failas nepateikiamas, o testai sukuria visus failus, kuriuos skaito.

## Licencija {#licence}

MIT – žr. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Naudoja numpy (BSD-3-Clause) ir, neprivalomai,
numba (BSD-2-Clause). `heat3d_update` yra 3DHeat įrankių bendras atnaujintuvas.
