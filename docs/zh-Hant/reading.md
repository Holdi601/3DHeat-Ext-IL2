---
title: "檔案如何被讀取"
nav_order: 5
lang: zh-Hant
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# 檔案如何被讀取 {#how-the-files-are-read}

| 部分 | 狀態 |
|---|---|
| 封存檔（`data/*.gtp`，Great Battles） | 檔案表（`S16R`、`STRMFAT?`、`DIR!`/`FILE` 記錄）與各項目（`STRMFILE` 標頭，資料以原樣儲存）；測試安裝中的每個 `Maps*.gtp` |
| `height.hini` | `height_map`、`water_map`、`heightMul`、`SeaLevel`、遊玩範圍與 `MapNW/NE/SE/SW`；測試安裝中的每一個 |
| 高度圖（`height.dat`） | 以下的編碼方式；在推導過程中被完整解碼的地圖扇區，其位元串流都被精確使用（最多只有位元組填充剩下的部分），其餘的則依標頭檢查。已與遊戲隨附於 `distlod.dat` 旁的未壓縮 `distlod.raw` 檔案逐位元比對，並與某張地圖自身的遠距 LOD 高度圖比對（相關係數 0.999） |
| 高度 | 公尺 = 原始值 x heightMul / 256 - SeaLevel x heightMul。某張地圖的海面解碼後會正好等於其 hini 註解所給的高度；另一張地圖的邊界則等於其 `bounds_level` |
| 放置 | 在 hini 的四個角落之間做雙線性內插，第 0 列朝北，第 0 行朝西。已在某張地圖上以已知的城鎮、海岸與海洋檢驗（城鎮高度與真實高度相差約 10 公尺以內，海洋位於海平面以下）。這些角落構成的是四邊形，而非遊戲自己的投影，因此在大型地圖的中央，預期會有數百公尺的誤差。某一地圖系列的 hini 帶有另一張地圖的角落（它們所涵蓋的範圍只佔其真實大小的一部分）；這一點會被偵測到，而該系列改以地標擬合來放置：遊戲自己的位置資料庫（`*.ldfbin`）中的城鎮與機場，與其真實位置相比，均方根誤差約為兩公里（城鎮與以其命名的機場相比，真實地點的座標則約為一公里以內）；JSON 會列出每個地標及其殘差 |
| 水域遮罩（`water.wtr`：四層金字塔式的圖塊，每個圖塊是一張 400 公尺區塊的表，每個區塊為陸地、全水或部分水域，其形狀以位元串流表示） | 每張地圖都會讀取其容器（在完整解碼的檔案上沒有剩餘位元組）；部分水域區塊內的形狀**未被解碼**。全水區塊即為水域；在部分水域區塊中，當水域圖（`height_w.dat`，與高度圖相同的編碼）高於地面時，取樣即為水域，或在湖泊旁邊，地面不高於湖面時也為水域；陸地區塊則為乾燥地。這樣就能去除僅憑水域圖會被判定為水域的沼澤。比輸出網格更窄的河流，會被切成數段 |
| 城鎮輪廓（`textures.tini` 所列的貼花網格：`towns.mesh`、`cities.mesh`、`city_*.mesh`、`roads_fields.mesh` 等：25.6 公里的圖塊，由平面的貼圖三角形組成） | 每張地圖都會讀取；保留其貼圖為城鎮、村莊或工業用地的面。已在數張地圖上與真實城鎮相比對（河流兩岸的城鎮、交匯處）。它們是輪廓：遊戲在執行時才放置建築，檔案中並沒有建築 |
| 機場、橋樑、建築 | **未讀取**：機場是任務物件，建築則來自遊戲自身的放置 |
| 森林（`forest_map.wtr`） | 其區塊的讀取方式相同，但幾乎每個區塊都是「部分森林」，因此若沒有位元串流，就沒有可用的森林遮罩；未繪製 |
| 地面的材質 | 未讀取 |

## 高度圖編碼 {#the-heightmap-codec}

僅根據資料檔案推導出來；未讀取或反組譯任何遊戲程式碼。小端序：

```text
u32 width, u32 height, u32 sectorsX, u32 sectorsY, u32 sectorSize, f32 cellSize
u32 offset[sectorsX * sectorsY]            from the start of the file, row-major, top row first
sector: u16 count (bytes that follow), u16 mode ((log2 sectorSize) << 4 | LW, LW = 4),
        then a bitstream read MSB first:
  PRE   2 * (log2(sectorSize) - 5) bits, always 0 so far
  LIT   the first sample: sign (1), n (LW bits), magnitude (n + 1 bits)
  then until the sector is full:
    0 LIT       next = previous + LIT
    1 RUN LIT   the previous sample repeats RUN times (k: 3 bits, m: k + 1 bits, RUN = m + 1),
                then (unless the sector is full) next = previous + LIT
  values are 16-bit: read them modulo 65536
```

右邊緣與下邊緣的不完整扇區會被填充後再裁切。同一套編碼也適用於水域圖與遠距 LOD 高度圖。

## 地標擬合 {#landmark-fits}

當無法使用地圖的角落時，`landmarks.py` 會以最小平方法，擬合出一個從遊戲公尺到地球的仿射映射：遊戲中的位置來自使用者自己的檔案（任務中的 `Airfield` 區塊、生涯位置資料庫），真實位置則來自程式碼中所列出的各地點公布座標表。JSON 的 `georeference` 會記錄矩陣、原點、每個地標及其殘差，以及均方根誤差。
