---
title: Luas, tástálacha, téarmaí
nav_order: 7
lang: "ga"
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

Léann an uirlis seo cartlanna do shuiteála féin de IL-2 Sturmovik: Great Battles ar do ríomhaire agus ní athraíonn sí riamh iad.

Ní sheoltar ná ní athdháiltear aon rud ón gcluiche: gan comhaid chluiche, gan cód cluiche, gan DLLanna; tógann na tástálacha féin gach comhad a léann siad. Fanann na leibhéil a scríobhann sé ar do mheaisín.

Níl baint ag 3DHeat IL-2 le 1C Game Studios / 777 Studios agus níl sé formhuinithe acu. Is lena n-úinéirí IL-2 Sturmovik agus na hainmneacha agus na trádmharcanna gaolmhara.

Sealbhóirí ceart: oscail saincheist ag [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - freagraímid go tapa agus bainimid aon rud ar iarratas.

## Ceadúnas {#licence}

MIT - féach [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Úsáideann sí numpy (BSD-3-Clause) agus, go roghnach,
numba (BSD-2-Clause). Is `heat3d_update` nuashonraí comhroinnte uirlisí 3DHeat.
