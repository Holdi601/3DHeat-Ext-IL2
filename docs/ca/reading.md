---
title: Com es llegeixen els fitxers
nav_order: 5
lang: "ca"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Com es llegeixen els fitxers {#how-the-files-are-read}

| Part | Estat |
|---|---|
| Arxius (`data/*.gtp`, Great Battles) | la taula de fitxers (registres `S16R`, `STRMFAT?`, `DIR!`/`FILE`) i les entrades (capçalera `STRMFILE`, dades emmagatzemades tal com són); cada `Maps*.gtp` de la instal·lació de prova |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, els límits de joc i `MapNW/NE/SE/SW`; cadascun de la instal·lació de prova |
| Mapes d'alçades (`height.dat`) | el còdec de sota; cada sector dels mapes descodificat sencer mentre s'hi treballava utilitza el seu flux de bits exactament (com a molt el farciment de bytes sobrant), la resta comprovada per la capçalera. Comprovat bit a bit contra els fitxers `distlod.raw` sense comprimir que el joc envia al costat dels seus `distlod.dat`, i contra el mapa d'alçades de llunyania (LOD) propi d'un mapa (correlació 0,999) |
| Alçades | metres = x crua × heightMul / 256 - SeaLevel × heightMul. El mar d'un mapa es descodifica exactament a l'altura que indiquen els comentaris del seu hini; la frontera d'un altre, al seu `bounds_level` |
| Col·locació | bilineal entre les quatre cantonades del hini, fila 0 al nord, columna 0 a l'oest. Comprovat en un mapa contra pobles, costes i mars coneguts (les altures dels pobles a uns 10 m de les reals, els mars per sota del nivell del mar). Les cantonades formen un quadrilàter, no la projecció pròpia del joc, de manera que cal esperar uns quants centenars de metres d'error al centre d'un mapa gran. El hini d'una família de mapes porta les cantonades d'una altra (abasten una fracció de la seva mida real); això es detecta, i aquella família es col·loca en canvi per un ajust per punts de referència: pobles i aeròdroms de les bases de dades d'ubicacions del propi joc (`*.ldfbin`) contra les seves posicions reals, rms d'un parell de quilòmetres (pobles contra els aeròdroms que porten el seu nom, i coordenades dels llocs reals a uns mil metres). El JSON enumera cada punt de referència i el seu residu |
| Màscara d'aigua (`water.wtr`: quatre nivells piramidals de rajoles, cada rajola una taula de blocs de 400 m, cada bloc terra, ple o parcialment aigua amb la seva forma en un flux de bits) | el contenidor es llegeix a cada mapa (cap byte sobrant als fitxers descodificats sencers); la forma dins d'un bloc parcialment aquós **no es descodifica**. Els blocs plens són aigua; en els blocs parcialment aquosos una mostra és aigua on el mapa d'aigua (`height_w.dat`, mateix còdec que el mapa d'alçades) està per sobre del terreny, o, al costat d'un llac, on el terreny no és més alt que el llac; els blocs de terra són secs. Així s'elimina el pantà que el mapa d'aigua sol reporta com a aigua. Els rius més estrets que la quadrícula de sortida surten trencats en trossos |
| Petjades de pobles (les malles de calc que llista `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: rajoles de 25,6 km de triangles plans amb textura) | es llegeixen a cada mapa; es conserven les cares amb una textura de poble, vila o terreny industrial. Comprovat contra els pobles reals en alguns mapes (un poble a les dues ribes d'un riu, una confluència). Són petjades: el joc col·loca els edificis en temps d'execució, i els fitxers no contenen edificis |
| Aeròdroms, ponts, edificis | **no llegits**: els aeròdroms són objectes de missió, els edificis vénen de la col·locació pròpia del joc |
| Boscos (`forest_map.wtr`) | els seus blocs es llegeixen de la mateixa manera, però gairebé cada bloc és «parcialment bosc», de manera que sense el flux de bits no hi ha cap màscara de bosc utilitzable; no es dibuixa |
| Les textures del terreny | no llegides |

## El còdec del mapa d'alçades {#the-heightmap-codec}

Descobert només a partir dels fitxers de dades; no es va llegir ni desensamblar cap codi del joc.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            des de l'inici del fitxer, per files, la fila superior primer
sector: u16 count (bytes que segueixen), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        després un flux de bits llegit primer el MSB:
  PRE   2 * (log2(sectorSize) - 5) bits, sempre 0 fins ara
  LIT   la primera mostra: signe (1), n (bits LW), magnitud (n + 1 bits)
  després fins que el sector és ple:
    0 LIT       següent = anterior + LIT
    1 RUN LIT   la mostra anterior es repeteix RUN vegades (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                després (tret que el sector sigui ple) següent = anterior + LIT
  els valors són de 16 bits: llegeix-los mòdul 65536
```

Els sectors parcials als costats dret i inferior s'emplenen i es retallen. El mateix
còdec serveix per al mapa d'aigua i per al mapa d'alçades de llunyania.

## Ajustos per punts de referència {#landmark-fits}

Quan no es poden usar les cantonades d'un mapa, `landmarks.py` ajusta una transformació afí
dels metres del joc a la Terra pels mínims quadrats: posicions del joc a partir dels fitxers propis
de l'usuari (blocs `Airfield` de les missions, les bases de dades d'ubicacions de la carrera),
posicions reals a partir de taules de les coordenades publicades dels llocs, al codi. El
`georeference` del JSON porta la matriu, l'origen, cada punt de referència amb el seu residu i el rms.
