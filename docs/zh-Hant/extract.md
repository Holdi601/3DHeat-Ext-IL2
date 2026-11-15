---
title: "建立關卡：extract"
nav_order: 3
lang: "zh-Hant"
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# 建立關卡：`extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## 逐步說明 {#step-by-step}

第一次使用命令列？請先閱讀[開始之前](before-you-start.md)。

1. 用 [`list`](list.md) 找出地圖的名稱。
2. 執行 `heat3d-il2-level extract <map> -o levels`。名稱可以使用萬用字元，並以引號括起來（`"<family>_*"`）；`--all` 會處理每一張地圖。
3. 若要在不需擺放步驟的情況下，把錄製放到關卡上，請指定其原點：`--origin <lat> <lon>`，設為該錄製的 `geo`（其工作階段的參考點）。若未指定，地圖的中心即為原點，而 `.json` 中的 `geo` 會說明是哪一點。
4. 此指令會在解碼每張地圖時印出一行，然後是 `ok <glb> <triangles> (<frame> frame)` 或 `failed <map>: <why>`。
5. 在檢視器的背景／關卡面板中載入 `<folder>/<map>/<map>.glb`。

![在合成安裝上執行 extract](../assets/img/extract.svg)

以遊戲自身的公尺、不含水域：

![extract --frame game --no-water](../assets/img/extract-game.svg)

對已寫出的地圖再執行一次：

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## 選項 {#options}

| 選項 | 預設 | 作用 |
|---|---|---|
| `maps` | - | 以 `list` 所印出的地圖名稱；允許使用萬用字元 |
| `--all` | 關閉 | 每一張地圖；共用同一高度圖與水域圖的季節只寫入一次 |
| `-o`、`--out` | 必填 | 輸出資料夾；每張地圖放入 `<out>/<map>/` |
| `--game FOLDER` | 自動尋找 | IL-2 資料夾（可重複指定） |
| `--max-grid N` | `1024` | 每邊最多的高度圖取樣數（1024：約 200 萬個三角形）；地圖每 *k* 個取樣取一次，以符合此上限 |
| `--frame` `enu` 或 `game` | `enu` | `enu`：以 `--origin` 為中心的東向公尺、海拔高度、北向公尺，與 Watcher 的 Tacview 表格相同；`game`：遊戲自身的公尺（x 朝北、y 朝上、z 朝東）。無法放置在地球上的地圖，無論要求為何，都會以 `game` 寫出 |
| `--origin LAT LON` | 地圖的中心 | `enu` 座標系的原點（錄製的 `geo`） |
| `--no-water` | 關閉 | 不包含水域 |
| `--no-towns` | 關閉 | 不包含城鎮的輪廓 |
| `--skip-existing` | 關閉 | 略過已存在 `.glb` 的地圖 |

程式列出的每個選項：[指令參考](../cli-reference.md)。

設定 `HEAT3D_DEBUG` 可印出失敗地圖的完整追蹤資訊。`.glb` 會先寫入 `<map>.glb.part`，完成後再更名。

結束狀態：0 所有地圖都已寫出；1 有任何一張失敗（其他的仍會寫出）；2 找不到安裝，或沒有任何地圖符合。

## 範例 {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # one map, enu frame round its centre
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # in the flat map of a recording with that geo
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # finer, several maps
heat3d-il2-level extract --all --skip-existing -o levels         # every map, only the new ones
heat3d-il2-level extract <map> --frame game -o levels            # the game's own metres, as mission files have them
```

檔案中有什麼內容：[關卡檔案與座標系](output.md)。
