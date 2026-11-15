---
title: "Arhivi brez tabele datotek"
nav_order: 6
lang: sl
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Igra, katere arhivi nimajo tabele datotek {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea v svojih arhivih ne hrani berljive tabele datotek (imena so zgoščena v bloku na koncu
vsakega arhiva), njene nastavitvene datoteke pa niso shranjene berljivo. `list` njen zemljevid prikaže z
igro `Korea`. Torej:

- njena višinska karta in karta vode se najdeta po glavi (zgradba `height.dat`, odseki po 128 vzorcev; zelo
  velika mreža pri fini velikosti celice);
- postavljena je na Zemljo s prilagajanjem letališč, ki jih njene misije postavijo (`data/Missions/**/*.Mission`,
  prebrano na tvojem računalniku), objavljenim koordinatam pravih letališč (`korea.py`): odstopanja od deset do
  nekaj sto metrov. JSON navaja vsak orientir in njegovo odstopanje;
- heightMul in SeaLevel sta ocenjena: ladje v misijah stojijo na morju, zato njihova višina nad najpogostejšo
  (morsko) vrednostjo karte vode daje merilo. Višine so verjetne (morje pod morsko gladino, obalna mesta na
  nekaj metrih), nadalje niso preverjene. JSON jih označi kot ocenjene.
