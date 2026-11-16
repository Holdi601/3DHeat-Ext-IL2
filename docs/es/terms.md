---
title: "Velocidad, pruebas y condiciones"
nav_order: 7
lang: "es"
source: terms.md
source_hash: "3baa9f57ade6"
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

Esta herramienta lee los archivos comprimidos de tu propia instalación de IL-2 Sturmovik: Great Battles en tu ordenador y nunca los modifica.

No se incluye ni se redistribuye nada del juego: ningún archivo del juego, ningún código del juego, ninguna DLL; las pruebas generan cada archivo que leen. Los niveles que escribe se quedan en tu equipo.

3DHeat IL-2 no está afiliado a 1C Game Studios / 777 Studios ni cuenta con su respaldo. IL-2 Sturmovik y los nombres y marcas relacionados pertenecen a sus propietarios.

Titulares de derechos: abrid una incidencia en [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - respondemos rápido y retiramos lo que se nos pida.

## Licencia {#licence}

MIT - ver [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Usa numpy
(BSD-3-Clause) y, opcionalmente, numba (BSD-2-Clause). `heat3d_ext_il2.update` es el actualizador compartido de
las herramientas de 3DHeat.
