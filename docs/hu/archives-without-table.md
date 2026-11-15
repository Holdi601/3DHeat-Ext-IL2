---
title: "Archívumok fájltáblázat nélkül"
nav_order: 6
lang: "hu"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Egy játék, amelynek archívumai nem tartalmaznak fájltáblázatot {#a-game-whose-archives-have-no-file-table}

Az IL-2 Series: Korea archívumai nem tartanak olvasható fájltáblázatot (a nevek egy blokkba vannak hash-elve
minden archívum végén), a beállítási fájljai pedig nincsenek olvasható formában tárolva. A `list` a térképét
`Korea` játékkal mutatja. Így:

- a magassági térképét és a víztérképét a fejléckük alapján találjuk meg (a `height.dat` elrendezése, 128 mintás
  szektorok; nagyon nagy rács, finom cellamérettel);
- a földön úgy helyezzük el, hogy a küldetései által elhelyezett repülőtereket (`data/Missions/**/*.Mission`,
  a saját gépén olvasva) illesztjük a valódi repülőterek közzétett koordinátáihoz (`korea.py`): maradék hibák
  tíz és néhány száz méter között. A JSON minden tájékozódó pontot és annak maradék hibáját felsorolja;
- a heightMul és a SeaLevel becsült: a küldetések hajói a tengeren ülnek, így a magasságuk a víztérkép leggyakoribb
  (tengeri) értékéhez képest adja a skálát. A magasságok ésszerűnek tűnnek (a tenger a tengerszint alatt, a parti
  városok néhány méterrel), további ellenőrzés nélkül. A JSON becsültként jelöli őket.
