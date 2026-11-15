---
title: Conas a léitear na comhaid
nav_order: 5
lang: ga
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Conas a léitear na comhaid {#how-the-files-are-read}

| Cuid | Stádas |
|---|---|
| Cartlanna (`data/*.gtp`, Great Battles) | an tábla comhad (taifid `S16R`, `STRMFAT?`, `DIR!`/`FILE`) agus na hiontrálacha (ceannteideal `STRMFILE`, sonraí stóráilte mar atá); gach `Maps*.gtp` den tsuiteáil tástála |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, teorainneacha súgartha agus `MapNW/NE/SE/SW`; gach ceann den tsuiteáil tástála |
| Léarscáileanna airde (`height.dat`) | an chódóg thíos; úsáideann gach hearnáil de na léarscáileanna a díchódaíodh go hiomlán agus é á oibriú amach a sruth giotán go beacht (padding beart ar a mhéad fágtha), seiceáilte de réir ceannteidil don chuid eile. Seiceáilte giotán ar ghiotán i gcoinne na gcomhad `distlod.raw` neamhchomhbhrúite a sheolann an cluiche lena `distlod.dat`, agus i gcoinne léarscáil airde LOD i bhfad ar shiúl léarscáile (comhghaol 0.999) |
| Airde | méadair = amh x heightMul / 256 - SeaLevel x heightMul. Díchódaíonn farraige léarscáile go beacht go dtí an airde a thugann tuairimí a hini; teorainn ceann eile go dtí a `bounds_level` |
| Cur ar an domhan | dhébhileanach idir ceithre choirnéal an hini, sraith 0 ó thuaidh, colún 0 ó thiar. Seiceáilte ar léarscáil i gcoinne bailte, cóstaí agus farraigí aitheanta (airde bailte laistigh de thart ar 10 m dá n-airde fíor, na farraigí faoi leibhéal na farraige). Is ceathairshleasán iad na coirnéil, ní teilgean an chluiche féin, mar sin bí ag súil le roinnt céad méadar d'earráid i lár léarscáile móire. Iompraíonn hini teaghlaigh léarscáile amháin coirnéil léarscáile eile (clúdaíonn siad cuid bheag dá fíormhéid); braitear é seo, agus cuirtear an teaghlach sin ar an domhan in ionad sin trí fheistiú tírdhreacha: bailte agus aerpháirceanna bunachar sonraí suímh an chluiche féin (`*.ldfbin`) i gcoinne a suíomhanna fíora, fréamh-mheánchearnach cúpla ciliméadar (bailte i gcoinne na n-aerpháirceanna a ainmníodh ina ndiaidh, agus comhordanáidí na n-áiteanna fíora go dtí thart ar chiliméadar); liostaíonn an JSON gach tírdhreach agus a iarmhar |
| Masc uisce (`water.wtr`: ceithre leibhéal pirimide de thíleanna, gach tíl ina tábla de bhlocanna 400 m, gach bloc talamh, lán nó uisce páirteach lena chruth i sruth giotán) | léitear an coimeádán ar gach léarscáil (gan beart fágtha ar na comhaid a díchódaíodh go hiomlán); **ní dhíchódaítear** an cruth taobh istigh de bhloc uisce páirteach. Is uisce blocanna lána; i mblocanna uisce páirteach is uisce sampla nuair atá an léarscáil uisce (`height_w.dat`, an chódóg chéanna leis an léarscáil airde) os cionn na talún, nó, in aice locha, nuair nach bhfuil an talamh níos airde ná an loch; tá blocanna talún tirim. Baineann sé sin an riasc a thuairiscíonn an léarscáil uisce léi féin mar uisce. Tagann aibhneacha níos caoile ná an greille aschuir amach briste ina phíosaí |
| Lorg bailte (na mogaill decal a liostaíonn `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: tíleanna 25.6 km de thriantáin chothroma uigeachta) | léite ar gach léarscáil; coinnítear na haghaidheanna a bhfuil baile, sráidbhaile nó talamh tionsclaíoch mar uigeacht orthu. Seiceáilte i gcoinne fíorbhailte ar chúpla léarscáil (baile ar an dá bhruach d'abhainn, cumar). Is lorg iad: cuireann an cluiche na foirgnimh ar fáil ag am rite, agus níl aon fhoirgnimh sna comhaid |
| Aerpháirceanna, droichid, foirgnimh | **gan léamh**: is rudaí misin iad aerpháirceanna, tagann foirgnimh ó chur an chluiche féin |
| Foraoisí (`forest_map.wtr`) | léitear a bhlocanna ar an mbealach céanna, ach is beagnach gach bloc "foraoise páirteach", mar sin gan an sruth giotán níl aon masc foraoise inúsáidte; gan tarraingt |
| Uigeachtaí na talún | gan léamh |

## Cód na léarscáile airde {#the-heightmap-codec}

Oibrithe amach ó na comhaid sonraí amháin; níor léadh ná níor dhíchomhdhéanadh aon chód cluiche.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            from the start of the file, row-major, top row first
sector: u16 count (bytes that follow), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        then a bitstream read MSB first:
  PRE   2 * (log2(sectorSize) - 5) bits, always 0 so far
  LIT   the first sample: sign (1), n (LW bits), magnitude (n + 1 bits)
  then until the sector is full:
    0 LIT       next = previous + LIT
    1 RUN LIT   the previous sample repeats RUN times (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                then (unless the sector is full) next = previous + LIT
  values are 16-bit: read them modulo 65536
```

Líontar hearnálacha páirteacha ag na himill dheis agus bun agus gearrtar iad. Coinníonn an
chódóg chéanna an léarscáil uisce agus an léarscáil airde LOD i bhfad ar shiúl.

## Feistiú tírdhreacha {#landmark-fits}

Nuair nach féidir coirnéil léarscáile a úsáid, feistíonn `landmarks.py` léarscáil affine ó
mhéadair an chluiche go dtí an domhan leis na cearnóga is lú: suíomhanna cluiche ó chomhaid
an úsáideora féin (bloic `Airfield` misin, bunachair sonraí suímh gairme), fíorshuíomhanna
ó tháblaí de chomhordanáidí foilsithe na n-áiteanna sa chód. Iompraíonn `georeference` an JSON
an mhaitrís, an tionscnamh, gach tírdhreach lena iarmhar
agus an fréamh-mheánchearnach.
