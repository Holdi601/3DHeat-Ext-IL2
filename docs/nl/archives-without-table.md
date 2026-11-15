---
title: Archieven zonder bestandstabel
nav_order: 6
lang: nl
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Een spel waarvan de archieven geen bestandstabel hebben {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea bewaart geen leesbare bestandstabel in zijn archieven (de namen
staan in een gehasht blok aan het eind van elk archief), en zijn instellingenbestanden
zijn niet leesbaar opgeslagen. `list` toont zijn kaart met het spel `Korea`. Dus:

- zijn hoogtekaart en watermap worden gevonden aan de hand van hun kop (de indeling van `height.dat`,
  sectoren van 128 monsters; een zeer groot raster met een fijne celgrootte);
- het wordt op de aarde geplaatst door de vliegvelden die zijn missies plaatsen
  (`data/Missions/**/*.Mission`, gelezen op jouw computer) te passen op de gepubliceerde
  coördinaten van de echte vliegvelden (`korea.py`): afwijkingen van tientallen tot enkele honderden
  meters. De JSON somt elk oriëntatiepunt en zijn afwijking op;
- heightMul en SeaLevel zijn geschat: schepen in de missies liggen op zee, dus hun hoogte boven de
  meest voorkomende (zee)waarde van de watermap geeft de schaal. De hoogten komen plausibel uit
  (de zee onder zeeniveau, kuststeden op enkele meters), verder niet gecontroleerd. De JSON markeert ze als geschat.
