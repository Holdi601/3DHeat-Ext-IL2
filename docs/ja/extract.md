---
title: "レベルを作る: extract"
nav_order: 3
lang: "ja"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# レベルを作る: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## 手順ごとの説明 {#step-by-step}

コマンドラインは初めてですか？ まず [始める前に](before-you-start.md) を読んでください。

1. [`list`](list.md) で、マップの名前を調べます。
2. `heat3d-il2-level extract <map> -o levels` を実行します。名前には、引用符で囲めばワイルドカードを使えます（`"<family>_*"`）。`--all` はすべてのマップを対象にします。
3. 記録を、配置の手順なしにレベルに重ねるには、原点を指定します: `--origin <lat> <lon>` に、記録の `geo`（そのセッションの基準点）を入れます。指定しなければ、マップの中心が原点になります。`.json` の `geo` がどちらかを示しています。
4. コマンドは、デコードしながらマップごとに1行を表示し、最後に `ok <glb> <triangles> (<frame> frame)` または `failed <map>: <why>` を表示します。
5. `<folder>/<map>/<map>.glb` を、ビューアの背景/レベルパネルで読み込みます。

![合成インストールでの extract](../assets/img/extract.svg)

ゲーム自身のメートルで、水を除いた場合:

![extract --frame game --no-water](../assets/img/extract-game.svg)

すでに書き出したマップがある状態での2回目の実行:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## オプション {#options}

| オプション | 既定値 | 働き |
|---|---|---|
| `maps` | - | `list` が表示する通りのマップ名。ワイルドカード可 |
| `--all` | オフ | すべてのマップ。ハイトマップと水のマップを共有する季節は一度だけ書き出されます |
| `-o`, `--out` | 必須 | 出力フォルダー。各マップは `<out>/<map>/` に入ります |
| `--game FOLDER` | 自動検出 | IL-2のフォルダー（複数指定可） |
| `--max-grid N` | `1024` | ハイトマップの一辺の最大サンプル数（1024: 約200万の三角形）。マップは、収まるように *k* サンプルごとに間引かれます |
| `--frame` `enu` または `game` | `enu` | `enu`: `--origin` を原点とした、東へのメートル、高度、北へのメートル。3DHeat WatcherのTacviewの表と同じです。`game`: ゲーム自身のメートル（x が北、y が上、z が東）。地球上に置けないマップは、何を指定されても `game` で書き出されます |
| `--origin LAT LON` | マップの中心 | `enu` 座標系の原点（記録の `geo`） |
| `--no-water` | オフ | 水を除く |
| `--no-towns` | オフ | 町の範囲を除く |
| `--skip-existing` | オフ | `.glb` がすでにあるマップは残す |

プログラムが表示する通りのすべてのオプション: [コマンドリファレンス](../cli-reference.md)。

失敗したマップの完全なトレースバックを表示するには、`HEAT3D_DEBUG` を設定します。`.glb` は `<map>.glb.part` に書かれ、完成したら名前が変わります。

終了ステータス: 0 すべてのマップを書き出した。1 どれかが失敗（ほかは書き出されます）。2 インストールがない、またはどのマップも一致しなかった。

## 例 {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # 一つのマップ。中心の周りの enu 座標系
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # その geo を持つ記録の平らなマップに
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # より細かく、複数のマップ
heat3d-il2-level extract --all --skip-existing -o levels         # すべてのマップ。新しいものだけ
heat3d-il2-level extract <map> --frame game -o levels            # ミッションファイルが持つ、ゲーム自身のメートル
```

ファイルの中身: [レベルのファイルと座標系](output.md)。
