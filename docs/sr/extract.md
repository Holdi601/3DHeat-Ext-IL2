---
title: "Прављење нивоа: extract"
nav_order: 3
lang: sr
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Прављење нивоа: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Корак по корак {#step-by-step}

Први пут у командној линији? Прво прочитајте [Пре почетка](before-you-start.md).

1. Нађите име мапе помоћу [`list`](list.md).
2. Покрените `heat3d-il2-level extract <map> -o levels`. Имена могу да садрже џокере,
   у наводницима (`"<family>_*"`); `--all` узима сваку мапу.
3. Да снимак поставите на ниво без корака постављања, дајте његов почетак:
   `--origin <lat> <lon>` постављен на `geo` снимка (референтна тачка његове
   сесије). Без тога је центар мапе почетак, а `geo` у `.json`-у каже који.
4. Команда исписује ред за сваку мапу док је декодује, па
   `ok <glb> <triangles> (<frame> frame)` или `failed <map>: <why>`.
5. Учитајте `<folder>/<map>/<map>.glb` на панел Позадина / ниво приказивача.

![extract над синтетичком инсталацијом](../assets/img/extract.svg)

У игриним сопственим метрима, без воде:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Друго покретање над мапама које су већ написане:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Опције {#options}

| Опција | Подразумевано | Шта ради |
|---|---|---|
| `maps` | - | имена мапа онако како их `list` исписује; џокери дозвољени |
| `--all` | искључено | свака мапа; сезоне које деле исту висинску мапу и мапу воде пишу се једном |
| `-o`, `--out` | обавезно | излазна фасцикла; свака мапа иде у `<out>/<map>/` |
| `--game FOLDER` | пронађено | IL-2 фасцикла (може више пута) |
| `--max-grid N` | `1024` | највише узорака висинске мапе по страни (1024: око два милиона троуглова); мапа се узоркује на сваких *k* узорака да стане |
| `--frame` `enu` или `game` | `enu` | `enu`: метри источно, висина, метри северно од `--origin`, као Watcher-ове Tacview табеле; `game`: игрини сопствени метри (x север, y навише, z исток). Мапа која не може да се смести на Земљу пише се у `game`, шта год да се тражи |
| `--origin LAT LON` | центар мапе | почетак `enu` оквира (`geo` снимка) |
| `--no-water` | искључено | изоставите воду |
| `--no-towns` | искључено | изоставите отиске градова |
| `--skip-existing` | искључено | оставите мапе чији `.glb` већ постоји |

Свака опција, онако како је програм исписује: [Референца команди](../cli-reference.md).

Поставите `HEAT3D_DEBUG` да исписује пун траг грешке неуспеле мапе. `.glb` се пише у
`<map>.glb.part` и преименује се кад је готов.

Излазни статус: 0 свака мапа написана; 1 нека није успела (остале се ипак пишу);
2 инсталација није нађена или ниједна мапа не одговара.

## Примери {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # једна мапа, enu оквир око њеног центра
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # у равној мапи снимка с том geo вредношћу
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # финије, више мапа
heat3d-il2-level extract --all --skip-existing -o levels         # свака мапа, само нове
heat3d-il2-level extract <map> --frame game -o levels            # игрини сопствени метри, као што их имају датотеке мисија
```

Шта је у датотекама: [Датотеке нивоа и оквири](output.md).
