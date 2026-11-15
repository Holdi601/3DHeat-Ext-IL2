---
title: Archivos sin tabla de archivos
nav_order: 6
lang: "es"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Un juego cuyos archivos no tienen tabla de archivos {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea no conserva en sus archivos una tabla de archivos legible (los nombres están
ocultos en un bloque al final de cada archivo), y sus archivos de ajustes no se guardan legibles.
`list` muestra su mapa con el juego `Korea`. Así que:

- su mapa de altura y su mapa de agua se encuentran por su cabecera (la disposición de `height.dat`,
  sectores de 128 muestras; una cuadrícula muy grande con una celda fina);
- se coloca sobre la tierra ajustando los aeródromos que colocan sus misiones
  (`data/Missions/**/*.Mission`, leídos en tu propio equipo) a las coordenadas publicadas de los
  aeródromos reales (`korea.py`): residuos de decenas a unos pocos cientos de metros. El JSON lista
  cada punto de referencia y su residuo;
- heightMul y SeaLevel se estiman: los barcos de las misiones están sobre el mar, así que su altura
  sobre el valor más común (el del mar) del mapa de agua da la escala. Las alturas salen plausibles
  (el mar bajo el nivel del mar, los pueblos de costa a unos pocos metros), sin comprobar más. El
  JSON las marca como estimadas.
