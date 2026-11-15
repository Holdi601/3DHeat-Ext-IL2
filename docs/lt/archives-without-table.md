---
title: "Archyvai be failų lentelės"
nav_order: 6
lang: lt
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Žaidimas, kurio archyvuose nėra failų lentelės {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea archyvuose nėra skaitomos failų lentelės (pavadinimai sumaišyti bloke
kiekvieno archyvo pabaigoje), o jo nustatymų failai nesaugomi skaitomai. `list` rodo jo žemėlapį su žaidimu
`Korea`. Taigi:

- jo reljefo ir vandens žemėlapiai randami pagal antraštę (`height.dat` išdėstymas, 128 mėginių sektoriai; labai
  didelis tinklelis smulkiu ląstelės dydžiu);
- jis įdedamas į Žemę pritaikant oro uostus, kuriuos įdeda jo misijos (`data/Missions/**/*.Mission`, skaitoma jūsų
  kompiuteryje), prie tikrų oro uostų paskelbtų koordinačių (`korea.py`): paklaidos – dešimtys ar keli šimtai metrų.
  JSON išvardija kiekvieną orientyrą ir jo paklaidą;
- heightMul ir SeaLevel įvertinami: misijų laivai stovi ant jūros, todėl jų aukštis virš dažniausios vandens žemėlapio
  (jūros) reikšmės duoda mastelį. Aukščiai atrodo pagrįsti (jūra žemiau jūros lygio, pakrantės miestai keliais metrais),
  daugiau netikrinta. JSON jie pažymėti kaip įvertinti.
