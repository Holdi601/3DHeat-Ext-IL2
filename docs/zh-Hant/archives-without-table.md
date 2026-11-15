---
title: "沒有檔案表的封存檔"
nav_order: 6
lang: zh-Hant
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# 封存檔沒有檔案表的遊戲 {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea 的封存檔中沒有可讀取的檔案表（檔名以雜湊形式保存在每個封存檔末端的區塊中），其設定檔也不是以可讀形式儲存的。`list` 會以遊戲 `Korea` 顯示它的地圖。因此：

- 其高度圖與水域圖是依據標頭找到的（`height.dat` 的版面，每個扇區為 128 個取樣；網格非常大，單元尺寸很細）；
- 它在地球上的位置，是透過擬合其任務所放置的機場（`data/Missions/**/*.Mission`，在你的電腦上讀取）與真實機場公布的座標（`korea.py`）而得出的：殘差為數十到數百公尺。JSON 會列出每個地標及其殘差；
- heightMul 與 SeaLevel 是估計出來的：任務中的船隻位於海上，因此它們高出水域圖中最常見（海面）數值的高度，即可得出比例。高度看起來合理（海面位於海平面以下，沿海城鎮位於數公尺高），未再進一步檢查。JSON 會將它們標記為估計值。
