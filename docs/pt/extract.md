---
title: "Montar níveis: extract"
nav_order: 3
lang: pt
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# Montar níveis: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<mapa> ... | --all) -o <pasta> [--game PASTA ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## Passo a passo {#step-by-step}

Nunca usou a linha de comando? Leia primeiro [Antes de começar](before-you-start.md).

1. Encontre o nome do mapa com [`list`](list.md).
2. Execute `heat3d-il2-level extract <mapa> -o levels`. Os nomes podem usar curingas,
   entre aspas (`"<família>_*"`); `--all` pega todos os mapas.
3. Para pôr uma gravação no nível sem nenhuma etapa de posicionamento, indique a sua origem:
   `--origin <lat> <lon>` com o `geo` da gravação (o ponto de referência da sua sessão).
   Sem isso, o centro do mapa é a origem, e o `geo` do `.json` mostra qual.
4. O comando imprime uma linha por mapa à medida que o decodifica, depois
   `ok <glb> <triângulos> (<frame> frame)` ou `failed <mapa>: <motivo>`.
5. Carregue `<pasta>/<mapa>/<mapa>.glb` no painel Fundo / nível do visualizador.

![extract em uma instalação sintética](../assets/img/extract.svg)

Nos metros do próprio jogo, sem a água:

![extract --frame game --no-water](../assets/img/extract-game.svg)

Uma segunda execução sobre mapas já gravados:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## Opções {#options}

| Opção | Padrão | Faz |
|---|---|---|
| `maps` | - | nomes de mapas como `list` os imprime; curingas permitidos |
| `--all` | desligada | todos os mapas; as temporadas que compartilham um mapa de altura e um mapa de água são gravadas uma vez |
| `-o`, `--out` | obrigatória | a pasta de saída; cada mapa vai para `<out>/<mapa>/` |
| `--game PASTA` | encontrada | uma pasta do IL-2 (pode repetir) |
| `--max-grid N` | `1024` | no máximo N amostras de altura por lado (1024: cerca de 2 milhões de triângulos); o mapa é amostrado a cada *k* amostras para caber |
| `--frame` `enu` ou `game` | `enu` | `enu`: metros a leste, altitude, e norte de `--origin`, como as tabelas Tacview do Watcher; `game`: os metros do próprio jogo (x norte, y para cima, z leste). Um mapa que não pode ser colocado sobre a terra é gravado em `game` seja o que for pedido |
| `--origin LAT LON` | o centro do mapa | a origem do quadro `enu` (o `geo` de uma gravação) |
| `--no-water` | desligada | deixa a água de fora |
| `--no-towns` | desligada | deixa de fora as pegadas das cidades |
| `--skip-existing` | desligada | deixa de lado os mapas cujo `.glb` já existe |

Todas as opções, como o programa as mostra: [Referência de comandos](../cli-reference.md).

Defina `HEAT3D_DEBUG` para imprimir o rastreamento completo de um mapa que falhou. O `.glb` é
gravado em `<mapa>.glb.part` e renomeado quando fica completo.

Código de saída: 0 todos os mapas gravados, 1 algum falhou (os outros são gravados mesmo assim),
2 nenhuma instalação ou nenhum mapa encontrado.

## Exemplos {#examples}

```bash
heat3d-il2-level extract <mapa> -o levels                         # um mapa, quadro enu em torno do seu centro
heat3d-il2-level extract <mapa> --origin <lat> <lon> -o levels    # no mapa plano de uma gravação com esse geo
heat3d-il2-level extract "<família>_*" --max-grid 2048 -o levels  # mais fino, vários mapas
heat3d-il2-level extract --all --skip-existing -o levels          # todos os mapas, só os novos
heat3d-il2-level extract <mapa> --frame game -o levels            # os metros do próprio jogo, como os arquivos de missão os têm
```

O que há nos arquivos: [Os arquivos do nível e os quadros](output.md).
