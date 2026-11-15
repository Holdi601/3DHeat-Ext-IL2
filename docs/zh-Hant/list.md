---
title: "尋找地圖：list"
nav_order: 2
lang: "zh-Hant"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# 尋找地圖：`list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          the same, without installing
```

第一次使用命令列？請先閱讀[開始之前](before-you-start.md)。

1. 安裝一次：`git clone https://github.com/Holdi601/3DHeat-Ext-IL2`，在該資料夾中開啟終端機，然後執行 `python -m pip install -e .`（Python 3.10 或更新版本；它會帶入 numpy；`python -m pip install -e .[fast]` 則會加入 numba）。
2. 執行 `heat3d-il2-level list`。
3. 每張地圖印出一行，以定位字元分隔：它的名稱（`extract` 所使用的名稱）、所屬遊戲（`Great Battles`，或 [第二款遊戲](archives-without-table.md) 的 `Korea`）、它所讀取的高度圖，以及它在地球上的位置——地圖角落所構成的經緯度方框、擬合它位置的地標，或「not placed on the earth」（未放置在地球上）。最後一行（輸出到標準錯誤）會計算地圖數量，並列出安裝位置。

![在合成安裝上執行 list](../assets/img/list.svg)

此圖是在由測試的寫入程式所建立的安裝（`tests/synth.py`）上執行的結果，不是在遊戲上。

## 安裝位置的尋找方式 {#where-the-installs-are-found}

透過 Steam 尋找；若找不到，則使用 `--game <folder>`（可重複指定，每個安裝一個）或 `HEAT3D_IL2_GAME` 環境變數。安裝位置是一個資料夾，其 `data` 中含有 `Maps*.gtp` 封存檔。

| 選項 | 作用 |
|---|---|
| `--game FOLDER` | IL-2 資料夾；若有多個安裝，請重複指定 |

結束狀態：0 完成；2 找不到安裝。
