---
title: "Construir niveles: extract"
nav_order: 3
lang: es
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# Construir niveles: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Paso a paso {#step-by-step}

¿Nuevo en la línea de comandos? Lee primero [Antes de empezar](before-you-start.md).

1. Busca el nombre del mapa con [`list`](list.md).
2. Ejecuta `heat3d-il2-level extract <map> -o levels`. Los nombres pueden usar comodines,
   entre comillas (`"<family>_*"`); `--all` toma todos los mapas.
3. Para poner una grabación sobre el nivel sin paso de colocación, indica su origen:
   `--origin <lat> <lon>` con el `geo` de la grabación (el punto de referencia de su sesión).
   Sin esto, el centro del mapa es el origen, y el `geo` del `.json` dice cuál es.
4. El comando imprime una línea por mapa según lo decodifica, y después
   `ok <glb> <triangles> (<frame> frame)` o `failed <map>: <why>`.
5. Carga `<folder>/<map>/<map>.glb` en el panel Fondo / nivel del visor.

![extract en una instalación sintética](../assets/img/extract.svg)

En los metros propios del juego, sin el agua:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Una segunda ejecución sobre mapas ya escritos:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opciones {#options}

| Opción | Por defecto | Qué hace |
|---|---|---|
| `maps` | - | nombres de mapa tal como los imprime `list`; se admiten comodines |
| `--all` | desactivada | cada mapa; las temporadas que comparten un mapa de altura y de agua se escriben una sola vez |
| `-o`, `--out` | obligatoria | la carpeta de salida; cada mapa va a `<out>/<map>/` |
| `--game FOLDER` | encontrada | una carpeta de IL-2 (se puede repetir) |
| `--max-grid N` | `1024` | muestras del mapa de altura por lado como máximo (1024: unos 2 millones de triángulos); el mapa se muestrea cada *k* muestras para ajustarse |
| `--frame` `enu` o `game` | `enu` | `enu`: metros al este, altitud y norte de `--origin`, como las tablas de Tacview del Watcher; `game`: los metros propios del juego (x norte, y arriba, z este). Un mapa que no se puede colocar sobre la tierra se escribe en `game` aunque se pida otra cosa |
| `--origin LAT LON` | el centro del mapa | el origen del marco `enu` (el `geo` de una grabación) |
| `--no-water` | desactivada | deja fuera el agua |
| `--no-towns` | desactivada | deja fuera las huellas de los pueblos |
| `--skip-existing` | desactivada | deja los mapas cuyo `.glb` ya existe |

Cada opción, tal como la muestra el programa: [Referencia de comandos](../cli-reference.md).

Define `HEAT3D_DEBUG` para imprimir el rastreo completo de un mapa fallido. El `.glb` se escribe en
`<map>.glb.part` y se renombra cuando termina.

Estado de salida: 0 cada mapa escrito; 1 alguno fallido (los demás se escriben igualmente); 2 no se
encontró ninguna instalación o ningún mapa coincidió.

## Ejemplos {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # un mapa, marco enu alrededor de su centro
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # en el mapa plano de una grabación con ese geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # más fino, varios mapas
heat3d-il2-level extract --all --skip-existing -o levels         # cada mapa, solo los nuevos
heat3d-il2-level extract <map> --frame game -o levels            # los metros propios del juego, como los tienen los archivos de misión
```

Qué hay en los archivos: [Los archivos del nivel y los marcos](output.md).
