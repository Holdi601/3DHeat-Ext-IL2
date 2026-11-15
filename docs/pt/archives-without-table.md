---
title: Arquivos sem tabela de arquivos
nav_order: 6
lang: pt
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# Um jogo cujos arquivos não têm tabela de arquivos {#a-game-whose-archives-have-no-file-table}

O IL-2 Series: Korea não guarda nenhuma tabela de arquivos legível nos seus arquivos (os nomes
ficam em forma de hash em um bloco no fim de cada arquivo), e os seus arquivos de configuração não são
guardados de forma legível. `list` mostra o seu mapa com o jogo `Korea`. Então:

- o seu mapa de altura e o seu mapa de água são encontrados pelo cabeçalho (o layout de `height.dat`,
  setores de 128 amostras; uma grade muito grande com um tamanho de célula fino);
- ele é colocado sobre a terra ajustando os aeródromos que as suas missões colocam
  (`data/Missions/**/*.Mission`, lidos na sua máquina) às coordenadas publicadas dos
  aeródromos reais (`korea.py`): resíduos de dezenas a algumas centenas de
  metros. O JSON lista cada marco e o seu resíduo;
- `heightMul` e `SeaLevel` são estimados: os navios das missões ficam sobre o mar,
  então a altura deles acima do valor mais comum (o mar) do mapa de água dá a escala.
  As alturas saem plausíveis (o mar abaixo do nível do mar, cidades costeiras a alguns
  metros), sem mais verificação. O JSON marca essas grandezas como estimadas.
