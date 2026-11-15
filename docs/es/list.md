---
title: "Buscar mapas: list"
nav_order: 2
lang: "es"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Buscar mapas: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          lo mismo, sin instalar
```

¿Nuevo en la línea de comandos? Lee primero [Antes de empezar](before-you-start.md).

1. Instálala una vez: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, abre una terminal en
   esa carpeta y ejecuta `python -m pip install -e .` (Python 3.10 o posterior; trae numpy;
   `python -m pip install -e .[fast]` añade numba).
2. Ejecuta `heat3d-il2-level list`.
3. Cada mapa imprime una línea, separada por tabuladores: su nombre (el nombre que toma `extract`),
   el juego (`Great Battles`, o `Korea` para [el segundo juego](archives-without-table.md)), el mapa de
   altura que lee, y dónde está sobre la tierra: su caja de latitud/longitud según las esquinas del
   mapa, o el ajuste por puntos de referencia que lo coloca, o "not placed on the earth" (no colocado
   sobre la tierra). La última línea (en stderr) cuenta los mapas y nombra las instalaciones.

![list en una instalación sintética](../assets/img/list.svg)

La imagen es una ejecución sobre una instalación construida con los escritores de las pruebas
(`tests/synth.py`), no sobre el juego.

## Dónde se encuentran las instalaciones {#where-the-installs-are-found}

Por Steam; si no, `--game <folder>` (se puede repetir, una por instalación) o la variable de entorno
`HEAT3D_IL2_GAME`. Una instalación es una carpeta cuya `data` contiene archivos `Maps*.gtp`.

| Opción | Qué hace |
|---|---|
| `--game FOLDER` | una carpeta de IL-2; repítela para varias instalaciones |

Estado de salida: 0 terminado; 2 no se encontró ninguna instalación.
