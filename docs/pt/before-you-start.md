---
title: Antes de começar
nav_order: 1.5
lang: pt
source: before-you-start.md
source_hash: "9e62d9ba2baa"
nav_exclude: true
search_exclude: true
---
# Antes de começar {#before-you-start}

Nunca usou a linha de comando? Esta página leva você do zero à primeira execução.
Leva cerca de dez minutos, uma única vez.

## 1. Instalar o Python {#install-python}

Esta ferramenta precisa do **Python 3.10 ou mais recente**.

- **Windows:** baixe o Python em [python.org/downloads](https://www.python.org/downloads/)
  e execute o instalador. Na primeira tela, marque **Add python.exe to PATH**,
  depois clique em **Install Now**.
- **macOS e Linux:** o Python 3 costuma já estar instalado. Onde estas páginas
  dizem `python`, digite `python3`.

## 2. Obter esta ferramenta {#get-this-tool}

Abra [github.com/Holdi601/3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2), clique no
botão verde **Code** e depois em **Download ZIP**, e descompacte em uma pasta à sua escolha. Se usa o git:
`git clone https://github.com/Holdi601/3DHeat-Ext-IL2`.

## 3. Abrir um terminal nessa pasta {#open-a-terminal-in-that-folder}

Um terminal é uma janela onde você digita comandos.

- **Windows:** abra a pasta no Explorador de Arquivos, clique na barra de endereço, digite
  `powershell` e pressione Enter. Abre uma janela azul ou preta, já nessa pasta.
- **macOS:** abra o **Terminal**, digite `cd ` (com um espaço), arraste a pasta para
  a janela e pressione Enter.

`cd` significa "mudar de pasta": `cd C:\Ferramentas\3DHeat-Ext-IL2` vai para essa pasta.

## 4. Instalar a ferramenta {#install-the-tool}

Digite isto e pressione Enter:

```bash
python -m pip install -e .
```

No final, você deve ver: `Successfully installed heat3d-ext-il2-...`.

## 5. Executar {#run-it}

```bash
heat3d-il2-level list
```

Você deve ver algo como:

```text
<mapa>	Great Battles	height /graphics/<mapa>/height.dat	<lat>..<lat> N, <lon>..<lon> E
<n> mapas em C:\Games\IL-2 Sturmovik Great Battles
```

Próximo: [Encontrar mapas: list](list.md), depois [Montar níveis: extract](extract.md).

## Como ler os comandos destas páginas {#how-to-read-the-commands-on-these-pages}

| Você vê | Significa |
|---|---|
| `<pasta>` | um marcador: digite o seu próprio valor no lugar, sem os `< >` |
| `[--force]` | opcional: deixe de fora, ou digite exatamente como mostrado |
| `a\|b` | uma escolha: digite `a` ou `b` |
| `# uma nota` | um comentário para você: não digite |
| `"C:\Meus Arquivos\x"` | coloque entre aspas um caminho que tenha espaços |
| `D:\Demos` | um exemplo de pasta do Windows: use a sua |

## Quando algo dá errado {#when-something-goes-wrong}

| A mensagem | O que fazer |
|---|---|
| `'python' is not recognized` | O Python não está instalado, ou a caixa PATH não foi marcada: instale de novo e marque (ou digite `py` em vez de `python`). |
| `'heat3d-il2-level' is not recognized` | Execute o passo 4 de novo na pasta da ferramenta, ou digite `python -m heat3d_ext_il2` em vez de `heat3d-il2-level`: faz o mesmo. |
| `No module named heat3d_ext_il2` | Você não está na pasta da ferramenta, ou o passo 4 falhou: use `cd` para ir até lá e execute o passo 4. |
| `No module named pip` | Execute `python -m ensurepip` e depois o passo 4. |
| qualquer outra coisa | Leia a última linha da mensagem e abra um issue no GitHub com ela. |

Todo comando também termina com um **código de saída**: 0 significa que deu certo. Para vê-lo,
digite `echo $LASTEXITCODE` no PowerShell ou `echo $?` no macOS e no Linux.
