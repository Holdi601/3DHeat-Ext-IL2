---
title: Velocidade, testes, termos
nav_order: 7
lang: "pt"
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

Esta ferramenta lê os arquivos compactados da sua própria instalação do IL-2 Sturmovik: Great Battles no seu computador e nunca os altera.

Nada do jogo é incluído nem redistribuído: nenhum arquivo do jogo, nenhum código do jogo, nenhuma DLL; os testes geram cada arquivo que leem. Os níveis que ele escreve ficam na sua máquina.

3DHeat IL-2 não é afiliado a 1C Game Studios / 777 Studios nem endossado por ela. IL-2 Sturmovik e os nomes e marcas relacionados pertencem aos seus donos.

Titulares de direitos: abram uma issue em [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) - respondemos rápido e removemos qualquer coisa a pedido.

## Licença {#licence}

MIT - veja [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE). Usa numpy (BSD-3-Clause) e, opcionalmente,
numba (BSD-2-Clause). `heat3d_update` é o atualizador compartilhado das ferramentas 3DHeat.
