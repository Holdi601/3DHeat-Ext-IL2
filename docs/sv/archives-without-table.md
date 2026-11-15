---
title: Arkiv utan filtabell
nav_order: 6
lang: "sv"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Ett spel vars arkiv saknar filtabell {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea behåller ingen läsbar filtabell i sina arkiv (namnen är hashade i ett block i slutet av varje arkiv), och dess inställningsfiler lagras inte läsbart. `list` visar dess karta med spelet `Korea`. Så:

- dess höjdkarta och vattenkarta hittas från deras huvud (layouten i `height.dat`, sektorer med 128 prov; ett mycket stort rutnät med en fin cellstorlek);
- den placeras på jorden genom att anpassa de flygfält dess uppdrag placerar (`data/Missions/**/*.Mission`, läst på din dator) till de riktiga flygfältens publicerade koordinater (`korea.py`): avvikelser på tiotals till några hundra meter. JSON-filen listar varje landmärke och dess avvikelse;
- heightMul och SeaLevel uppskattas: fartyg i uppdragen ligger på havet, så deras höjd över vattenkartans vanligaste (havs-) värde ger skalan. Höjderna blir rimliga (havet under havsnivån, kuststäder några meter upp), inte kontrollerat närmare. JSON-filen markerar dem som uppskattade.
