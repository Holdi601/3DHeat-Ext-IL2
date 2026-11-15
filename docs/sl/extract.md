---
title: "Gradnja ravni: extract"
nav_order: 3
lang: sl
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Gradnja ravni: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<zemljevid> ... | --all) -o <mapa> [--game MAPA ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Korak za korakom {#step-by-step}

Še nisi vajen ukazne vrstice? Najprej preberi [Preden začneš](before-you-start.md).

1. Poišči ime zemljevida z [`list`](list.md).
2. Zaženi `heat3d-il2-level extract <zemljevid> -o levels`. Imena lahko vsebujejo nadomestne znake v
   narekovajih (`"<družina>_*"`); `--all` vzame vsak zemljevid.
3. Da posnetek postaviš na raven brez koraka postavljanja, podaj njegovo izhodišče:
   `--origin <lat> <lon>` nastavi na `geo` posnetka (referenčna točka njegove seje). Brez tega je izhodišče
   središče zemljevida, `geo` v `.json` pa pove, kateri je.
4. Ukaz izpiše vrstico na zemljevid, ko ga dekodira, nato `ok <glb> <trikotniki> (<okvir> okvir)` ali
   `failed <zemljevid>: <zakaj>`.
5. Naloži `<mapa>/<zemljevid>/<zemljevid>.glb` na plošči Ozadje / nivo pregledovalnika.

![extract na sintetični namestitvi](../assets/img/extract.svg)

V igrinih metrih, brez vode:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Drugi zagon nad zemljevidi, ki so že zapisani:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Možnosti {#options}

| Možnost | Privzeto | Naredi |
|---|---|---|
| `zemljevidi` | - | imena zemljevidov, kot jih izpiše `list`; nadomestni znaki dovoljeni |
| `--all` | izklopljeno | vsak zemljevid; letni časi, ki delijo višinsko karto in karto vode, se zapišejo enkrat |
| `-o`, `--out` | obvezno | izhodna mapa; vsak zemljevid gre v `<out>/<zemljevid>/` |
| `--game MAPA` | najdeno | mapa IL-2 (lahko se ponovi) |
| `--max-grid N` | `1024` | največ vzorcev višinske karte na stranico (1024: približno 2 milijona trikotnikov); zemljevid se vzorči na vsakih *k* vzorcev, da se prilega |
| `--frame` `enu` ali `game` | `enu` | `enu`: metri vzhodno, nadmorska višina, severno od `--origin`, kot tabele Tacview v Watcherju; `game`: igrini lastni metri (x sever, y višina, z vzhod). Zemljevid, ki ga ni mogoče postaviti na Zemljo, se zapiše v `game`, ne glede na to, kaj je zahtevano |
| `--origin LAT LON` | središče zemljevida | izhodišče okvirja `enu` (`geo` posnetka) |
| `--no-water` | izklopljeno | izpusti vodo |
| `--no-towns` | izklopljeno | izpusti odtise mest |
| `--skip-existing` | izklopljeno | pusti zemljevide, katerih `.glb` že obstaja |

Vsaka možnost, kot jo izpiše program: [Priročnik ukazov](../cli-reference.md).

Nastavi `HEAT3D_DEBUG`, da se izpiše celotna sled napake pri zemljevidu, ki ni uspel. `.glb` se zapiše v
`<zemljevid>.glb.part` in se preimenuje, ko je končan.

Izhodna koda: 0 vsak zemljevid zapisan, 1 katerikoli ni uspel (ostali so vseeno zapisani), 2 ni namestitve ali se
ni ujemal noben zemljevid.

## Primeri {#examples}

```bash
heat3d-il2-level extract <zemljevid> -o levels                         # en zemljevid, okvir enu okoli njegovega središča
heat3d-il2-level extract <zemljevid> --origin <lat> <lon> -o levels    # na ravnem zemljevidu posnetka s tem geo
heat3d-il2-level extract "<družina>_*" --max-grid 2048 -o levels       # bolj fino, več zemljevidov
heat3d-il2-level extract --all --skip-existing -o levels               # vsi zemljevidi, samo novi
heat3d-il2-level extract <zemljevid> --frame game -o levels            # igrini lastni metri, kot jih imajo datoteke misij
```

Kaj je v datotekah: [Datoteke ravni in okvirji](output.md).
