---
title: "Tasemete ehitamine: extract"
nav_order: 3
lang: et
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Tasemete ehitamine: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Samm-sammult {#step-by-step}

Pole sul käsurealt kogemust? Loe esmalt [Enne alustamist](before-you-start.md).

1. Leia kaardi nimi käsuga [`list`](list.md).
2. Käivita `heat3d-il2-level extract <map> -o levels`. Nimes võib kasutada metamärke,
   jutumärkides (`"<family>_*"`); `--all` võtab kõik kaardid.
3. Et lindistus paigutada tasemele ilma paigutussammuta, anna sellele algpunkt:
   `--origin <lat> <lon>`, mis on lindistuse `geo` (tema seansi viitepunkt). Ilma selleta on kaardi keskpunkt algpunkt, ja `.json`-i `geo` ütleb, mis see on.
4. Käsk prindib rea kaardi kohta, kui ta seda dekodeerib, seejärel
   `ok <glb> <triangles> (<frame> frame)` või `failed <map>: <why>`.
5. Laadi `<folder>/<map>/<map>.glb` vaataja paneelis **Taust / tase**.

![extract sünteetilisel installil](../assets/img/extract.svg)

Mängu enda meetrites, ilma veeta:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Teine käivitus juba kirjutatud kaartidega:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Valikud {#options}

| Valik | Vaikimisi | Teeb |
|---|---|---|
| `maps` | - | kaardinimed, nii nagu `list` prindib; metamärgid lubatud |
| `--all` | väljas | iga kaart; hooajad, mis jagavad sama kõrgustikukaarti ja veekaarti, kirjutatakse üks kord |
| `-o`, `--out` | nõutud | väljundkaust; iga kaart läheb kausta `<out>/<map>/` |
| `--game FOLDER` | leitakse | IL-2 kaust (korduv) |
| `--max-grid N` | `1024` | kõrgustikukaardi proove külje kohta kõige rohkem (1024: umbes 2 miljonit kolmnurka); kaarti proovitakse iga *k* proovi järel, et mahutada |
| `--frame` `enu` või `game` | `enu` | `enu`: meetrit ida, kõrgus, põhja `--origin`-ist, nagu Watcheri Tacview tabelid; `game`: mängu enda meetrid (x põhja, y üles, z ida). Kaart, mida ei saa maakerale paigutada, kirjutatakse `game`-raamistikus, isegi kui seda ei küsitud |
| `--origin LAT LON` | kaardi keskpunkt | `enu` raamistiku algpunkt (lindistuse `geo`) |
| `--no-water` | väljas | jäta vesi välja |
| `--no-towns` | väljas | jäta linnade jalajäljed välja |
| `--skip-existing` | väljas | jäta vahele kaardid, mille `.glb` on juba olemas |

Iga valik, nii nagu programm selle prindib: [Käsu viide](../cli-reference.md).

Pane `HEAT3D_DEBUG`, et printida ebaõnnestunud kaardi täielik veajälg. `.glb` kirjutatakse
faili `<map>.glb.part` ja nimetatakse ümber, kui see on valmis.

Väljumisolek: 0 iga kaart kirjutatud, 1 mõni ebaõnnestus (teised kirjutatakse ikka), 2 installi ei leitud või ükski kaart ei sobinud.

## Näited {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # üks kaart, enu-raamistik keskpunkti ümber
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # lindistuse tasasel kaardil selle geo-ga
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # peenem, mitu kaarti
heat3d-il2-level extract --all --skip-existing -o levels         # iga kaart, ainult uued
heat3d-il2-level extract <map> --frame game -o levels            # mängu enda meetrid, nagu missioonifailidel
```

Mis failides on: [Tasemefailid ja raamistikud](output.md).
