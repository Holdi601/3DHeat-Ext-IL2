---
title: "マップを探す: list"
nav_order: 2
lang: ja
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# マップを探す: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          同じ。インストールせずに実行
```

コマンドラインは初めてですか？ まず [始める前に](before-you-start.md) を読んでください。

1. 一度だけインストール: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`、そのフォルダーでターミナルを開き、`python -m pip install -e .` を実行します（Python 3.10 以降。numpyが入ります。`python -m pip install -e .[fast]` を使うとnumbaも入ります）。
2. `heat3d-il2-level list` を実行します。
3. マップごとに、タブで区切られた1行が表示されます。その行には、名前（`extract` が受け取る名前）、ゲーム（`Great Battles`、または [2つ目のゲーム](archives-without-table.md) の `Korea`）、読むハイトマップ、そして地球上での位置が示されます。位置は、マップの四隅からの緯度・経度の範囲、またはそれを配置する目印の位置合わせ、または「地球上に配置されていない」です。最後の行（標準エラー出力）は、マップの数を数え、インストールの場所を示します。

![合成インストールでの list](../assets/img/list.svg)

この図は、テストの作成者が作ったインストール（`tests/synth.py`）での実行です。ゲームでの実行ではありません。

## インストールの場所 {#where-the-installs-are-found}

Steamを通じて探します。そうでなければ `--game <folder>`（繰り返し指定可。インストールごとに1つ）または `HEAT3D_IL2_GAME` 環境変数を使います。インストールとは、その `data` が `Maps*.gtp` のアーカイブを持つフォルダーのことです。

| オプション | 働き |
|---|---|
| `--game FOLDER` | IL-2のフォルダー。複数のインストールがあれば繰り返す |

終了ステータス: 0 完了。2 インストールが見つからなかった。
