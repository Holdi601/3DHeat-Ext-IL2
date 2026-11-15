---
title: "速度、テスト、利用条件"
nav_order: 7
lang: "ja"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# 速度、テスト、利用条件 {#speed-tests-terms}

## 速度 {#speed}

numbaが入っていなければ、デコードは純粋なPythonで行われます（`python -m pip install -e .[fast]` で入ります）。中くらいのマップは、numbaなしで約15秒、ありで約1秒かかります。最大のマップ（数億のサンプル）は、ありで約7秒です（最初の実行ではコンパイルも行われます）。メモリは、セクターの一列と出力の格子の分だけです。

## テスト {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` は、アーカイブ、ハイトマップ（上の符号化のエンコーダー）、`height.hini` のファイル、そしてファイル表のないアーカイブを、コードの中で作ります。

## 利用条件 {#the-terms}

IL-2 Sturmovik: Great Battles と IL-2 Series（1C Game Studios / 777 Studios）の使用許諾契約は、**見つかりませんでした**。インストールの中（その `data/Licenses.txt` にあるのは第三者のライセンスだけ）にも、発行元のサイトにも、Steamのエンドユーザー使用許諾契約のページにもなく、Steamのページは読み込めませんでした。頼る前に、ご自身で確認してください。このツールはアーカイブを読むだけで、変更は決してしません。書き出されるレベルはあなたのマシンに残ります。**決して公開しないでください**。ここにはゲームのデータは一切含まれず、テストはそれらが読むすべてのファイルを作ります。

## ライセンス {#licence}

MIT。[`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE) を参照してください。numpy（BSD-3-Clause）を使い、任意でnumba（BSD-2-Clause）を使います。`heat3d_update` は、3DHeatツールが共有するアップデーターです。
