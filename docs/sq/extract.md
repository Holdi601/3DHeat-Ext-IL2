---
title: "Ndërtimi i niveleve: extract"
nav_order: 3
lang: sq
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Ndërtimi i niveleve: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Hap pas hapi {#step-by-step}

Je i ri me rreshtin e komandave? Lexo së pari [Para se të fillosh](before-you-start.md).

1. Gjej emrin e hartës me [`list`](list.md).
2. Ekzekuto `heat3d-il2-level extract <map> -o levels`. Emrat mund të përdorin
   shenja zëvendësuese, në thonjëza (`"<family>_*"`); `--all` merr çdo hartë.
3. Që një regjistrim të bjerë mbi nivel pa hap vendosjeje, jep origjinën e tij:
   `--origin <lat> <lon>` e vendosur te `geo` i regjistrimit (pika e referencës
   e seancës së tij). Pa të, qendra e hartës është origjina, dhe `geo` i
   `.json` thotë cila.
4. Komanda shtyp një rresht për çdo hartë ndërsa e dekodon, pastaj
   `ok <glb> <triangles> (<frame> frame)` ose `failed <map>: <why>`.
5. Ngarko `<folder>/<map>/<map>.glb` te paneli Sfondi / niveli i shikuesit.

![extract mbi një instalim sintetik](../assets/img/extract.svg)

Në metrat e vetë lojës, pa ujin:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Një ekzekutim i dytë mbi harta të shkruara tashmë:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opsionet {#options}

| Opsioni | Parazgjedhja | Çfarë bën |
|---|---|---|
| `maps` | - | emrat e hartave siç i shtyp `list`; lejohen shenja zëvendësuese |
| `--all` | joaktiv | çdo hartë; stinët që ndajnë një heightmap dhe hartë uji shkruhen një herë |
| `-o`, `--out` | i detyrueshëm | dosja e daljes; çdo hartë shkon te `<out>/<map>/` |
| `--game FOLDER` | gjendet | një dosje IL-2 (i përsëritshëm) |
| `--max-grid N` | `1024` | më së shumti kaq mostra heightmap për anë (1024: rreth 2 milionë trekëndësha); harta mostrohet çdo *k* mostra që të përshtatet |
| `--frame` `enu` ose `game` | `enu` | `enu`: metra drejt lindjes, lartësi, drejt veriut nga `--origin`, si tabelat Tacview të Watcher; `game`: metrat e vetë lojës (x veri, y lart, z lindje). Një hartë që nuk mund të vendoset mbi tokë shkruhet në `game` çfarëdo që kërkohet |
| `--origin LAT LON` | qendra e hartës | origjina e kornizës `enu` (`geo` i një regjistrimi) |
| `--no-water` | joaktiv | lë jashtë ujin |
| `--no-towns` | joaktiv | lë jashtë gjurmët e qyteteve |
| `--skip-existing` | joaktiv | lë harta që `.glb` i tyre ekziston tashmë |

Çdo opsion, ashtu siç e shtyp programi: [Referenca e komandave](../cli-reference.md).

Vendos `HEAT3D_DEBUG` që të shtypet gjurma e plotë e një harte që dështoi. `.glb` shkruhet
te `<map>.glb.part` dhe riemërtohet kur përfundon.

Statusi i daljes: 0 çdo hartë u shkrua, 1 ndonjë dështoi (të tjerat shkruhen
prapë), 2 nuk u gjet instalim ose hartë që përputhet.

## Shembuj {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

Çfarë ka në skedarë: [Skedarët e nivelit dhe kornizat](output.md).
