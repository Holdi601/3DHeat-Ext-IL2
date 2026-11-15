---
title: "始める前に"
nav_order: 1.5
lang: "ja"
source: before-you-start.md
source_hash: "9e62d9ba2baa"
nav_exclude: true
search_exclude: true
---
# 始める前に {#before-you-start}

コマンドラインは初めてですか？ このページでは、ゼロから最初の実行までを案内します。
一度だけで、約10分かかります。

## 1. Pythonをインストール {#install-python}

このツールには **Python 3.10 以降** が必要です。

- **Windows:** [python.org/downloads](https://www.python.org/downloads/) からPythonをダウンロードし、インストーラーを実行します。最初の画面で **Add python.exe to PATH** にチェックを入れてから、**Install Now** をクリックします。
- **macOS と Linux:** Python 3 はすでに入っていることが多いです。このページで `python` と書いてある所は、`python3` と入力してください。

## 2. このツールを入手 {#get-this-tool}

[github.com/Holdi601/3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) を開き、緑色の **Code** ボタン、次に **Download ZIP** をクリックして、好きなフォルダーに展開します。gitを使うなら: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`。

## 3. そのフォルダーでターミナルを開く {#open-a-terminal-in-that-folder}

ターミナルとは、コマンドを入力するウィンドウのことです。

- **Windows:** エクスプローラーでフォルダーを開き、アドレスバーをクリックして `powershell` と入力し、Enterを押します。そのフォルダーがすでに開かれた、青または黒のウィンドウが開きます。
- **macOS:** **ターミナル** を開き、`cd ` （空白を1つ入れる）と入力し、フォルダーをウィンドウにドラッグしてEnterを押します。

`cd` は「フォルダーを変える」という意味です。`cd C:\Tools\3DHeat-Ext-IL2` と入力すると、そのフォルダーに移動します。

## 4. ツールをインストール {#install-the-tool}

次を入力してEnterを押します:

```bash
python -m pip install -e .
```

最後に次のような表示が出れば成功です: `Successfully installed heat3d-ext-il2-...`

## 5. 実行 {#run-it}

```bash
heat3d-il2-level list
```

次のような表示が出るはずです:

```text
<map>	Great Battles	height /graphics/<map>/height.dat	<lat>..<lat> N, <lon>..<lon> E
<n> maps in C:\Games\IL-2 Sturmovik Great Battles
```

次は: [マップを探す: list](list.md)、その後 [レベルを作る: extract](extract.md)。

## このページのコマンドの読み方 {#how-to-read-the-commands-on-these-pages}

| 表示 | 意味 |
|---|---|
| `<folder>` | 置き換え用の場所。`< >` を付けず、自分の値を入力します |
| `[--force]` | 省略可能。省くか、そのまま入力します |
| `a\|b` | 選択肢。`a` か `b` を入力します |
| `# a note` | あなたへのメモ。入力しません |
| `"C:\My Files\x"` | 空白を含むパスは引用符で囲みます |
| `D:\Demos` | Windowsのフォルダーの例。自分のものを使ってください |

## うまくいかないとき {#when-something-goes-wrong}

| 表示されたメッセージ | 対処 |
|---|---|
| `'python' is not recognized` | Pythonが入っていないか、PATHのチェックを入れ忘れています。もう一度インストールして、チェックを入れてください（または `python` の代わりに `py` と入力）。 |
| `'heat3d-il2-level' is not recognized` | ツールのフォルダーで手順4をもう一度実行するか、`heat3d-il2-level` の代わりに `python -m heat3d_ext_il2` と入力します。同じことをします。 |
| `No module named heat3d_ext_il2` | ツールのフォルダーにいないか、手順4が失敗しています。そのフォルダーに `cd` で移動し、手順4を実行してください。 |
| `No module named pip` | `python -m ensurepip` を実行してから、手順4へ。 |
| それ以外 | メッセージの最後の行を読み、それを書いてGitHubでissueを開いてください。 |

どのコマンドも最後に **終了ステータス** を返します。0なら成功です。確認するには、PowerShellでは `echo $LASTEXITCODE`、macOSとLinuxでは `echo $?` と入力します。
