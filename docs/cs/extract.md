---
title: "Sestavení úrovní: extract"
nav_order: 3
lang: cs
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Sestavení úrovní: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Krok za krokem {#step-by-step}

Nikdy jste nepracovali s příkazovým řádkem? Nejdřív si přečtěte [Než začnete](before-you-start.md).

1. Zjistěte název mapy pomocí [`list`](list.md).
2. Spusťte `heat3d-il2-level extract <map> -o levels`. Názvy mohou obsahovat zástupné znaky
   v uvozovkách (`"<family>_*"`); `--all` vezme každou mapu.
3. Chcete-li umístit záznam na úroveň bez kroku umísťování, zadejte jeho počátek:
   `--origin <lat> <lon>` nastavený na `geo` záznamu (referenční bod jeho relace).
   Bez něj je počátkem střed mapy a `geo` v `.json` říká, který to je.
4. Příkaz vypisuje řádek na každou mapu, jak ji dekóduje, pak
   `ok <glb> <triangles> (<frame> frame)` nebo `failed <map>: <why>`.
5. Načtěte `<folder>/<map>/<map>.glb` do panelu Pozadí / úroveň v prohlížeči.

![extract na syntetické instalaci](../assets/img/extract.svg)

V metrech samotné hry, bez vody:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Druhé spuštění nad již zapsanými mapami:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Možnosti {#options}

| Možnost | Výchozí | Co dělá |
|---|---|---|
| `maps` | - | názvy map tak, jak je vypisuje `list`; zástupné znaky jsou povolené |
| `--all` | vypnuto | každou mapu; ročníky, které sdílejí výškovou mapu a mapu vody, se zapíšou jednou |
| `-o`, `--out` | povinné | výstupní složka; každá mapa jde do `<out>/<map>/` |
| `--game FOLDER` | nalezeno | složka IL-2 (lze opakovat) |
| `--max-grid N` | `1024` | nejvýše tolik vzorků výškové mapy na stranu (1024: asi 2 miliony trojúhelníků); mapa se vzorkuje po každých *k* vzorcích, aby se vešla |
| `--frame` `enu` nebo `game` | `enu` | `enu`: metry na východ, nadmořská výška, metry na sever od `--origin`, jako tabulky Tacview u Watcheru; `game`: vlastní metry hry (x na sever, y nahoru, z na východ). Mapa, kterou nelze umístit na Zemi, se zapíše v `game`, ať je požadováno cokoli |
| `--origin LAT LON` | střed mapy | počátek rámce `enu` (`geo` záznamu) |
| `--no-water` | vypnuto | vynechá vodu |
| `--no-towns` | vypnuto | vynechá půdorysy měst |
| `--skip-existing` | vypnuto | vynechá mapy, jejichž `.glb` už existuje |

Každá možnost tak, jak ji program vypisuje: [Přehled příkazů](../cli-reference.md).

Nastavte `HEAT3D_DEBUG`, aby se vypsal celý výpis chyby u selhané mapy. Soubor `.glb`
se zapisuje do `<map>.glb.part` a po dokončení se přejmenuje.

Stavový kód: 0 každá mapa zapsána; 1 některá selhala (ostatní se přesto zapíší);
2 instalace nenalezena nebo žádná mapa neodpovídá.

## Příklady {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Co je v souborech: [Soubory úrovní a rámce](output.md).
