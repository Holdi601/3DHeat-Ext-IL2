---
title: Luas, tástálacha, téarmaí
nav_order: 7
lang: ga
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Luas, tástálacha, téarmaí {#speed-tests-terms}

## Luas {#speed}

Is Python glan é an díchódú mura bhfuil numba suiteáilte (`python -m pip install -e .[fast]`):
tógann léarscáil mheánmhéide thart ar 15 s gan é agus thart ar soicind leis; an
léarscáil is mó, roinnt céad milliún sampla, thart ar 7 s leis (déanann an chéad
rith tiomsú freisin). Fanann an chuimhne ag sraith amháin hearnálacha móide an greille aschuir.

## Tástálacha {#tests}

```bash
python -m pytest -q
```

Tógann `tests/synth.py` cartlanna, léarscáileanna airde (ionchódóir don chódóg thuas),
comhaid `height.hini` agus cartlanna gan tábla comhad i gcód.

## Na téarmaí {#the-terms}

**Níor aimsíodh** comhaontú ceadúnais IL-2 Sturmovik: Great Battles agus IL-2 Series (1C Game
Studios / 777 Studios): ní sa tsuiteáil (nach gcoinníonn `data/Licenses.txt` ach
ceadúnais tríú páirtí), ní ar shuíomh an fhoilsitheora, agus níor lódáil leathanach EULA Steam.
Seiceáil é tú féin sula mbraitheann tú air seo.
Ní léann an uirlis seo ach na cartlanna agus ní athraíonn sí iad choíche. Fanann na leibhéil a scríobhann sí
ar do mheaisín: **ná foilsigh iad choíche**. Ní sheolann aon rud anseo aon sonraí cluiche, agus
tógann na tástálacha gach comhad a léann siad.

## Ceadúnas {#licence}

MIT - féach [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Úsáideann sí numpy (BSD-3-Clause) agus, go roghnach,
numba (BSD-2-Clause). Is `heat3d_update` nuashonraí comhroinnte uirlisí 3DHeat.
