---
title: "Greitis, testai, sąlygos"
nav_order: 7
lang: "lt"
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

Šis įrankis skaito tavo paties IL-2 Sturmovik: Great Battles diegimo archyvus tavo kompiuteryje ir niekada jų nekeičia.

Iš žaidimo niekas nepateikiama ir neplatinama: jokių žaidimo failų, jokio žaidimo kodo, jokių DLL; testai patys sukuria kiekvieną skaitomą failą. Jo įrašyti lygiai lieka tavo kompiuteryje.

3DHeat IL-2 nėra susijęs su 1C Game Studios / 777 Studios ir nėra jo patvirtintas. IL-2 Sturmovik ir susiję pavadinimai bei prekių ženklai priklauso jų savininkams.

Teisių turėtojai: sukurkite pranešimą adresu [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - atsakome greitai ir paprašius pašaliname bet ką.

## Licencija {#licence}

MIT – žr. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Naudoja numpy (BSD-3-Clause) ir, neprivalomai,
numba (BSD-2-Clause). `heat3d_update` yra 3DHeat įrankių bendras atnaujintuvas.
