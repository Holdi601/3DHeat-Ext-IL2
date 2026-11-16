---
title: Брзина, тестови, услови
nav_order: 7
lang: "sr"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Брзина, тестови, услови {#speed-tests-terms}

## Брзина {#speed}

Декодовање је чист Python, осим ако није инсталирана numba (`python -m pip install -e .[fast]`):
средња мапа траје око 15 s без ње и око секунду са њом; највећа мапа, неколико
стотина милиона узорака, око 7 s с њом (прво покретање такође преводи). Меморија остаје на једном реду
сектора плус излазна мрежа.

## Тестови {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` прави архиве, висинске мапе (кодер за кодек изнад),
`height.hini` датотеке и архиве без табеле датотека у коду.

## Услови {#the-terms}

Овај алат чита архиве твоје сопствене инсталације IL-2 Sturmovik: Great Battles на твом рачунару и никад их не мења.

Ништа из игре се не испоручује нити даље дистрибуира: нема датотека игре, нема кода игре, нема DLL-ова; тестови сами праве сваку датотеку коју читају. Нивои које запише остају на твом рачунару.

3DHeat IL-2 није повезан са 1C Game Studios / 777 Studios нити га 1C Game Studios / 777 Studios подржава. IL-2 Sturmovik и повезани називи и жигови припадају својим власницима.

Носиоци права: отворите пријаву на [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - одговарамо брзо и на захтев уклањамо било шта.

## Лиценца {#licence}

MIT - види [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Користите numpy (BSD-3-Clause) и, по избору,
numba (BSD-2-Clause). `heat3d_update` је заједнички ажуриач 3DHeat алата.
