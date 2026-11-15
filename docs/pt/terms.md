---
title: Velocidade, testes, termos
nav_order: 7
lang: pt
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# Velocidade, testes, termos {#speed-tests-terms}

## Velocidade {#speed}

A decodificação é Python puro, a menos que o numba esteja instalado (`python -m pip install -e .[fast]`):
um mapa de porte médio leva cerca de 15 s sem ele e cerca de um segundo com ele; o
maior mapa, várias centenas de milhões de amostras, cerca de 7 s com ele (a primeira
execução também compila). A memória fica em uma linha de setores mais a grade de saída.

## Testes {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` monta, em código, arquivos, mapas de altura (um codificador do codec acima),
arquivos `height.hini` e arquivos sem tabela de arquivos.

## Os termos {#the-terms}

O acordo de licença do IL-2 Sturmovik: Great Battles e do IL-2 Series (1C Game
Studios / 777 Studios) **não foi encontrado**: nem na instalação (cujo
`data/Licenses.txt` traz só licenças de terceiros), nem no site da editora,
e a página do EULA do Steam não carregou. Confira você mesmo antes de confiar nisto.
Esta ferramenta só lê os arquivos e nunca os altera. Os níveis que ela grava ficam na
sua máquina: **nunca os publique**. Nada aqui distribui dados do jogo, e os
testes montam todo arquivo que lêem.

## Licença {#licence}

MIT - veja [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Usa numpy (BSD-3-Clause) e, opcionalmente,
numba (BSD-2-Clause). `heat3d_update` é o atualizador compartilhado das ferramentas 3DHeat.
