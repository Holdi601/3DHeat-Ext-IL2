---
title: "Līmeņu veidošana: extract"
nav_order: 3
lang: lv
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Līmeņu veidošana: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Soli pa solim {#step-by-step}

Nekad nav strādāts ar komandrindu? Vispirms izlasi [Pirms sākat](before-you-start.md).

1. Atrodi kartes nosaukumu ar [`list`](list.md).
2. Palaid `heat3d-il2-level extract <map> -o levels`. Nosaukumos var lietot aizstājējzīmes pēdiņās (`"<family>_*"`); `--all` ņem katru karti.
3. Lai ierakstu novietotu uz līmeņa bez novietošanas soļa, norādi tā sākumpunktu: `--origin <lat> <lon>` ar ieraksta `geo` (tā sesijas atsauces punktu). Bez tā kartes centrs ir sākumpunkts, un `.json` `geo` norāda, kurš tas ir.
4. Komanda izdrukā rindu katrai kartei, kad to dekodē, tad `ok <glb> <triangles> (<frame> frame)` vai `failed <map>: <why>`.
5. Ielādē `<folder>/<map>/<map>.glb` skatītāja Līmeņa panelī.

![extract uz sintētiska uzstādījuma](../assets/img/extract.svg)

Spēles pašu metros, bez ūdens:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Otrā palaišana pār jau uzrakstītām kartēm:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Iespējas {#options}

| Iespēja | Noklusējums | Ko dara |
|---|---|---|
| `maps` | - | kartes nosaukumi, kā tos izdrukā `list`; aizstājējzīmes atļautas |
| `--all` | izslēgts | katra karte; sezonas, kas dala vienu augstuma karti un ūdens karti, tiek uzrakstītas vienreiz |
| `-o`, `--out` | obligāta | izvades mape; katra karte ir `<out>/<map>/` |
| `--game FOLDER` | atrasts | IL-2 mape (var atkārtot) |
| `--max-grid N` | `1024` | augstuma kartes paraugu skaits malā, ne vairāk (1024: apmēram 2 miljoni trijstūru); karte tiek paraugota ik pēc *k* paraugiem, lai ietilptu |
| `--frame` `enu` vai `game` | `enu` | `enu`: metri uz austrumiem, augstums un ziemeļi no `--origin`, kā Watcher Tacview tabulas; `game`: spēles pašu metri (x ziemeļi, y augšup, z austrumi). Karte, ko nevar novietot uz zemes, tiek rakstīta `game` neatkarīgi no tā, ko pieprasa |
| `--origin LAT LON` | kartes centrs | `enu` sistēmas sākumpunkts (ieraksta `geo`) |
| `--no-water` | izslēgts | neiekļaut ūdeni |
| `--no-towns` | izslēgts | neiekļaut pilsētu laukumus |
| `--skip-existing` | izslēgts | atstāt kartes, kurām `.glb` jau eksistē |

Visas iespējas, kā tās izdrukā programma: [Komandu atsauce](../cli-reference.md).

Iestati `HEAT3D_DEBUG`, lai izdrukātu pilnu kļūdas izsekojumu neizdevušai kartei. `.glb` tiek rakstīts
failā `<map>.glb.part` un pārdēvēts, kad pabeigts.

Izejas statuss: 0 katra karte uzrakstīta; 1 kāda neizdevās (pārējās tomēr tiek uzrakstītas); 2 uzstādījums vai karte netika atrasta.

## Piemēri {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # viena karte, enu sistēma ap tās centru
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # plakanā kartē ierakstam ar šādu geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # smalkāk, vairākas kartes
heat3d-il2-level extract --all --skip-existing -o levels         # katra karte, tikai jaunās
heat3d-il2-level extract <map> --frame game -o levels            # spēles pašu metri, kā tos ir misiju faili
```

Kas ir failos: [Līmeņa faili un sistēmas](output.md).
