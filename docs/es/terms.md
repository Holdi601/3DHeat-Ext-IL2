---
title: "Velocidad, pruebas y condiciones"
nav_order: 7
lang: es
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Velocidad, pruebas y condiciones {#speed-tests-terms}

## Velocidad {#speed}

La decodificación es Python puro salvo que esté instalado numba (`python -m pip install -e .[fast]`):
un mapa de tamaño medio tarda unos 15 s sin él y alrededor de un segundo con él; el mapa más grande, varios
cientos de millones de muestras, unos 7 s con él (la primera ejecución también compila). La memoria se
mantiene en una fila de sectores más la cuadrícula de salida.

## Pruebas {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` construye en código archivos, mapas de altura (un codificador del códec de arriba),
archivos `height.hini` y archivos sin tabla de archivos.

## Condiciones {#the-terms}

El acuerdo de licencia de IL-2 Sturmovik: Great Battles e IL-2 Series (1C Game Studios / 777 Studios)
**no se encontró**: ni en la instalación (cuyo `data/Licenses.txt` solo contiene licencias de terceros),
ni en el sitio del editor, y la página del EULA de Steam no cargó. Compruébalo tú antes de confiar en
esto. Esta herramienta solo lee los archivos y nunca los cambia. Los niveles que escribe se quedan en tu
equipo: **nunca los publiques**. Nada de esto distribuye datos del juego, y las pruebas construyen
todos los archivos que leen.

## Licencia {#licence}

MIT - ver [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Usa numpy
(BSD-3-Clause) y, opcionalmente, numba (BSD-2-Clause). `heat3d_update` es el actualizador compartido de
las herramientas de 3DHeat.
