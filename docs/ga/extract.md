---
title: "Leibhéil a thógáil: extract"
nav_order: 3
lang: ga
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Leibhéil a thógáil: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Céim ar chéim {#step-by-step}

An bhfuil tú nua leis an líne ordaithe? Léigh [Sula dtosaíonn tú](before-you-start.md) ar dtús.

1. Aimsigh ainm na léarscáile le [`list`](list.md).
2. Rith `heat3d-il2-level extract <map> -o levels`. Féadfaidh ainmneacha cártaí fiáine a úsáid,
   idir comharthaí athfhriotail (`"<family>_*"`); tógann `--all` gach léarscáil.
3. Chun taifeadadh a chur ar an leibhéal gan aon chéim chuir i bhfeidhm, tabhair a thionscnamh:
   `--origin <lat> <lon>` socraithe do `geo` an taifeadta (pointe
   tagartha a sheisiúin). Gan é is é lár na léarscáile an tionscnamh, agus deir
   `geo` an `.json` cé acu.
4. Priontálann an t-ordú líne in aghaidh na léarscáile de réir mar a dhíchódaíonn sé í, ansin
   `ok <glb> <triangles> (<frame> frame)` nó `failed <map>: <why>`.
5. Lódáil `<folder>/<map>/<map>.glb` i bpainéal Cúlra / leibhéal an amharcáin.

![extract ar shuiteáil sintéiseach](../assets/img/extract.svg)

I méadair an chluiche féin, gan an t-uisce:

![extract --frame game --no-water](../assets/img/extract-game.svg)

An dara rith thar léarscáileanna scríofa cheana:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Roghanna {#options}

| Rogha | Réamhshocrú | Cad a dhéanann sí |
|---|---|---|
| `maps` | - | ainmneacha léarscáileanna mar a phriontálann `list` iad; cártaí fiáine ceadaithe |
| `--all` | as | gach léarscáil; scríobhtar séasúir a roinneann léarscáil airde agus léarscáil uisce uair amháin |
| `-o`, `--out` | riachtanach | an fillteán aschuir; téann gach léarscáil in `<out>/<map>/` |
| `--game FOLDER` | aimsithe | fillteán IL-2 (is féidir é a athdhéanamh) |
| `--max-grid N` | `1024` | samplaí léarscáile airde in aghaidh an taoibh ar a mhéad (1024: thart ar 2 mhilliún triantán); samplaítear an léarscáil gach *k* sampla le dul i bhfeidhm |
| `--frame` `enu` nó `game` | `enu` | `enu`: méadair soir, airde, ó thuaidh de `--origin`, cosúil le táblaí Tacview an Watcher; `game`: méadair an chluiche féin (x ó thuaidh, y suas, z soir). Scríobhtar léarscáil nach féidir a chur ar an domhan in `game` is cuma cad a iarrtar |
| `--origin LAT LON` | lár na léarscáile | tionscnamh an fhráma `enu` (`geo` taifeadta) |
| `--no-water` | as | fág an t-uisce ar lár |
| `--no-towns` | as | fág lorg na mbailte ar lár |
| `--skip-existing` | as | fág léarscáileanna a bhfuil a `.glb` ann cheana |

Gach rogha, mar a phriontálann an clár í: [Tagairt orduithe](../cli-reference.md).

Socraigh `HEAT3D_DEBUG` chun lorg iomlán (traceback) léarscáile a theip a phriontáil. Scríobhtar an `.glb` chuig
`<map>.glb.part` agus athainmnítear é nuair a bhíonn sé críochnaithe.

Stádas scoir: 0 gach léarscáil scríofa, 1 aon cheann theip (scríobhtar na cinn eile
fós), 2 gan suiteáil ná léarscáil mheaitseáilte.

## Samplaí {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Cad atá sna comhaid: [Comhaid agus fráma an leibhéil](output.md).
