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

このツールは、あなたのコンピューター上にあるあなた自身の IL-2 Sturmovik: Great Battles のインストールのアーカイブを読み、それらを一切変更しません。

ゲームのものは何も同梱・再配布しません。ゲームのファイルも、ゲームのコードも、DLL もありません。テストは読むファイルをすべて自分で作ります。書き出したレベルはあなたのマシンに残ります。

3DHeat IL-2 は 1C Game Studios / 777 Studios とは提携しておらず、承認も受けていません。IL-2 Sturmovik および関連する名称と商標は、それぞれの所有者に帰属します。

権利者の方へ: [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) で issue を開いてください。迅速に対応し、ご要望があれば何でも削除します。

## ライセンス {#licence}

MIT。[`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE) を参照してください。numpy（BSD-3-Clause）を使い、任意でnumba（BSD-2-Clause）を使います。`heat3d_update` は、3DHeatツールが共有するアップデーターです。
