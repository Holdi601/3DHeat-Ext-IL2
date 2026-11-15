---
title: "Arkistot ilman tiedostotaulukkoa"
nav_order: 6
lang: "fi"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Peli, jonka arkistoissa ei ole tiedostotaulukkoa {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea ei säilytä arkistoissaan luettavaa tiedostotaulukkoa (nimet on tiivistetty
jokaisen arkiston lopussa olevaan lohkoon), eikä sen asetustiedostoja ole tallennettu luettavina.
`list` näyttää sen kartan pelillä `Korea`. Joten:

- sen korkeuskartta ja vesikartta löytyvät otsikkonsa perusteella (`height.dat`-asettelu, lohkot
  128 näytteen sektoreina; hyvin suuri ruudukko hienolla solukoolla);
- se sijoitetaan maapallolle sovittamalla lentokentät, jotka sen tehtävät asettavat
  (`data/Missions/**/*.Mission`, luettuna omalla koneellasi), todellisten lentokenttien julkaistuihin
  koordinaatteihin (`korea.py`): jäännökset kymmenistä muutamaan sataan metriin. JSON luettelee jokaisen
  maamerkin ja sen jäännöksen;
- heightMul ja SeaLevel arvioidaan: tehtävien laivat ovat merellä, joten niiden korkeus vesikartan yleisimpään
  (meri-) arvoon antaa mittakaavan. Korkeudet ovat uskottavia (meri merenpinnan alapuolella, rannikon kaupungit
  muutaman metrin korkeudella), ei tarkistettu pidemmälle. JSON merkitsee ne arvioiduiksi.
