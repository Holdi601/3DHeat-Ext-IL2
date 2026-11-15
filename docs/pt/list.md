---
title: "Encontrar mapas: list"
nav_order: 2
lang: "pt"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# Encontrar mapas: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game PASTA ...]
python -m heat3d_ext_il2 list ...          o mesmo, sem instalar
```

Nunca usou a linha de comando? Leia primeiro [Antes de começar](before-you-start.md).

1. Instale uma vez: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, abra
   um terminal nessa pasta e execute `python -m pip install -e .` (Python 3.10
   ou mais recente; ele traz numpy; `python -m pip install -e .[fast]` acrescenta numba).
2. Execute `heat3d-il2-level list`.
3. Cada mapa imprime uma linha, separada por tabulações: o seu nome (o nome que `extract`
   aceita), o jogo (`Great Battles`, ou `Korea` para [o segundo jogo](archives-without-table.md)), o mapa de altura que ele lê, e
   onde ele fica na terra - a sua caixa de latitude/longitude a partir dos cantos do mapa,
   ou o ajuste por marcos que o posiciona, ou "not placed on the earth" (não posicionado na terra).
   A última linha (na saída de erro) conta os mapas e diz quais são as instalações.

![list em uma instalação sintética](../assets/img/list.svg)

A imagem é uma execução em uma instalação montada pelos escritores de teste
(`tests/synth.py`), não no jogo.

## Onde as instalações são encontradas {#where-the-installs-are-found}

Pelo Steam; caso contrário, `--game <pasta>` (pode repetir, uma por instalação) ou a
variável de ambiente `HEAT3D_IL2_GAME`. Uma instalação é uma pasta cuja `data`
contém arquivos `Maps*.gtp`.

| Opção | Faz |
|---|---|
| `--game PASTA` | uma pasta do IL-2; repita para várias instalações |

Código de saída: 0 pronto, 2 nenhuma instalação encontrada.
