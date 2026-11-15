---
title: "Lygių kūrimas: extract"
nav_order: 3
lang: lt
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Lygių kūrimas: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Žingsnis po žingsnio {#step-by-step}

Nesate įpratę prie komandinės eilutės? Pirmiausia perskaitykite [Prieš pradedant](before-you-start.md).

1. Raskite žemėlapio pavadinimą su [`list`](list.md).
2. Vykdykite `heat3d-il2-level extract <map> -o levels`. Pavadinimuose galima naudoti pakaitos ženklus kabutėse
   (`"<family>_*"`); `--all` paima kiekvieną žemėlapį.
3. Norėdami įdėti įrašą į lygį be jokio vietos parinkimo, nurodykite jo pradžios tašką:
   `--origin <lat> <lon>`, nustatytą pagal įrašo `geo` (jo sesijos nuorodos tašką). Be jo žemėlapio centras yra pradžios taškas,
   o `.json` `geo` parodo, koks jis.
4. Komanda išveda po eilutę kiekvienam žemėlapiui, kai jį iškoduoja, tada
   `ok <glb> <triangles> (<frame> frame)` arba `failed <map>: <why>`.
5. Įkelkite `<folder>/<map>/<map>.glb` žiūrintojo Lygio skydelyje.

![extract ant sintetinio įdiegimo](../assets/img/extract.svg)

Žaidimo paties metrais, be vandens:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Antras paleidimas ant jau įrašytų žemėlapių:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Parinktys {#options}

| Parinktis | Numatyta | Ką daro |
|---|---|---|
| `maps` | - | žemėlapių pavadinimai, kaip rodo `list`; galima pakaitos ženklai |
| `--all` | išjungta | kiekvienas žemėlapis; sezonai, kurie dalijasi tuo pačiu reljefo ir vandens žemėlapiu, įrašomi vieną kartą |
| `-o`, `--out` | privaloma | išvesties aplankas; kiekvienas žemėlapis eina į `<out>/<map>/` |
| `--game FOLDER` | randama | IL-2 aplankas (kartojamas) |
| `--max-grid N` | `1024` | daugiausia reljefo mėginių vienoje pusėje (1024: apie 2 milijonai trikampių); žemėlapis imamas kas *k* mėginių, kad tilptų |
| `--frame` `enu` arba `game` | `enu` | `enu`: metrai į rytus, aukštis, metrai į šiaurę nuo `--origin`, kaip Watcher Tacview lentelės; `game`: paties žaidimo metrai (x – į šiaurę, y – aukštyn, z – į rytus). Žemėlapis, kurio negalima įdėti į žemės paviršių, įrašomas `game` formatu, kad ir ko būtų prašoma |
| `--origin LAT LON` | žemėlapio centras | `enu` pradžios taškas (įrašo `geo`) |
| `--no-water` | išjungta | nepaisyti vandens |
| `--no-towns` | išjungta | nepaisyti miestų plotų |
| `--skip-existing` | išjungta | praleisti žemėlapius, kurių `.glb` jau yra |

Kiekviena parinktis, kaip ją rodo programa: [Komandų nuoroda](../cli-reference.md).

Nustatykite `HEAT3D_DEBUG`, kad būtų spausdinamas visas nepavykusio žemėlapio klaidos pėdsakas. `.glb` įrašomas į
`<map>.glb.part` ir pervadinamas, kai baigtas.

Išeities kodas: 0 – visi žemėlapiai įrašyti; 1 – bent vienas nepavyko (kiti vis tiek įrašomi); 2 – įdiegimas nerastas arba
nė vienas žemėlapis neatitiko.

## Pavyzdžiai {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # vienas žemėlapis, enu frame aplink jo centrą
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # plokščiame įrašo su tuo geo žemėlapyje
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # smulkiau, keli žemėlapiai
heat3d-il2-level extract --all --skip-existing -o levels         # kiekvienas žemėlapis, tik nauji
heat3d-il2-level extract <map> --frame game -o levels            # žaidimo paties metrais, kaip jas turi misijų failai
```

Kas yra failuose: [Lygio failai ir koordinačių sistemos](output.md).
