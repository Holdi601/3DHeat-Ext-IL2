---
title: Cómo se leen los archivos
nav_order: 5
lang: es
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# Cómo se leen los archivos {#how-the-files-are-read}

| Parte | Estado |
|---|---|
| Archivos (`data/*.gtp`, Great Battles) | la tabla de ficheros (registros `S16R`, `STRMFAT?`, `DIR!`/`FILE`) y las entradas (cabecera `STRMFILE`, datos guardados tal cual); cada `Maps*.gtp` de la instalación de prueba |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, los límites de juego y `MapNW/NE/SE/SW`; cada uno de la instalación de prueba |
| Mapas de altura (`height.dat`) | el códec de abajo; cada sector de los mapas decodificado por completo mientras se descubría la forma usa su flujo de bits exactamente (como mucho el relleno de bytes sobrante), el resto se comprueba por la cabecera. Comprobado bit a bit contra los archivos `distlod.raw` sin comprimir que el juego incluye junto a sus `distlod.dat`, y contra el mapa de altura de nivel de detalle lejano de un mapa (correlación 0,999) |
| Alturas | metros = x crudo × heightMul / 256 - SeaLevel × heightMul. El mar de un mapa se decodifica exactamente a la altura que indican los comentarios de su hini; el borde de otro, a su `bounds_level` |
| Colocación | bilineal entre las cuatro esquinas del hini, fila 0 al norte, columna 0 al oeste. Comprobada en un mapa con pueblos, costas y mares conocidos (alturas de pueblos a unos 10 m de las reales, los mares bajo el nivel del mar). Las esquinas forman un cuadrilátero, no la proyección propia del juego, así que espera algunos cientos de metros de error en el centro de un mapa grande. El hini de una familia de mapas lleva las esquinas de otro mapa (abarcan una fracción de su tamaño real); esto se detecta, y esa familia se coloca en su lugar mediante un ajuste por puntos de referencia: pueblos y aeródromos de las bases de datos de ubicación propias del juego (`*.ldfbin`) frente a sus posiciones reales, con un error cuadrático medio de un par de kilómetros (pueblos frente a los aeródromos que llevan su nombre, y coordenadas de los lugares reales a un kilómetro aproximadamente); el JSON lista cada punto de referencia y su residuo |
| Máscara de agua (`water.wtr`: cuatro niveles de pirámide de teselas, cada tesela una tabla de bloques de 400 m, cada bloque tierra, lleno o parcialmente con agua, con su forma en un flujo de bits) | el contenedor se lee en cada mapa (sin ningún byte sobrante en los archivos decodificados por completo); la forma dentro de un bloque parcialmente con agua **no se decodifica**. Los bloques llenos son agua; en los bloques parcialmente con agua, una muestra es agua donde el mapa de agua (`height_w.dat`, mismo códec que el mapa de altura) está por encima del suelo, o, junto a un lago, donde el suelo no es más alto que el lago; los bloques de tierra están secos. Eso quita el pantano que el mapa de agua por sí solo marca como agua. Los ríos más estrechos que la cuadrícula de salida salen rotos en trozos |
| Huellas de pueblos (las mallas de calcomanía que lista `textures.tini`: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh`, ...: teselas de 25,6 km de triángulos planos con textura) | se leen en cada mapa; se conservan las caras cuya textura es de pueblo, aldea o terreno industrial. Comprobadas contra los pueblos reales de algunos mapas (un pueblo en las dos orillas de un río, una confluencia). Son huellas: el juego coloca los edificios en tiempo de ejecución, y los archivos no contienen edificios |
| Aeródromos, puentes, edificios | **no se leen**: los aeródromos son objetos de misión, los edificios vienen de la colocación propia del juego |
| Bosques (`forest_map.wtr`) | sus bloques se leen igual, pero casi todo bloque es "parcialmente bosque", así que sin el flujo de bits no hay una máscara de bosque utilizable; no se dibuja |
| Las texturas del terreno | no se leen |

## El códec del mapa de altura {#the-heightmap-codec}

Descubierto solo a partir de los archivos de datos; no se leyó ni desensambló código del juego.
Little-endian:

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            desde el inicio del archivo, por filas, la fila superior primero
sector: u16 count (bytes que siguen), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        luego un flujo de bits leído MSB primero:
  PRE   2 * (log2(sectorSize) - 5) bits, siempre 0 hasta ahora
  LIT   la primera muestra: signo (1), n (LW bits), magnitud (n + 1 bits)
  luego hasta llenar el sector:
    0 LIT       siguiente = anterior + LIT
    1 RUN LIT   la muestra anterior se repite RUN veces (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                luego (salvo que el sector esté lleno) siguiente = anterior + LIT
  los valores son de 16 bits: léelos módulo 65536
```

Los sectores parciales en los bordes derecho e inferior se rellenan y se recortan. El mismo códec sirve
para el mapa de agua y para el mapa de altura de nivel de detalle lejano.

## Ajustes por puntos de referencia {#landmark-fits}

Cuando las esquinas de un mapa no sirven, `landmarks.py` ajusta una transformación afín de los metros
del juego a la tierra por mínimos cuadrados: las posiciones del juego salen de los archivos propios del
usuario (bloques `Airfield` de las misiones, las bases de datos de ubicación de la carrera), y las
posiciones reales de tablas con las coordenadas publicadas de los lugares, en el código. El
`georeference` del JSON contiene la matriz, el origen, cada punto de referencia con su residuo, y el
error cuadrático medio.
