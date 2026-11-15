---
title: "速度、測試與條款"
nav_order: 7
lang: "zh-Hant"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# 速度、測試與條款 {#speed-tests-terms}

## 速度 {#speed}

除非安裝了 numba（`python -m pip install -e .[fast]`），否則解碼是純 Python 執行：
中等大小的地圖在沒有 numba 時約需 15 秒，有 numba 時約一秒；最大的地圖（數億個取樣）有 numba 時約需 7 秒（第一次執行還會進行編譯）。記憶體僅保留一列扇區加上輸出網格。

## 測試 {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` 會以程式碼建立封存檔、高度圖（上述編碼的編碼器）、`height.hini` 檔案，以及沒有檔案表的封存檔。

## 條款 {#the-terms}

IL-2 Sturmovik: Great Battles 與 IL-2 Series（1C Game Studios / 777 Studios）的授權合約 **未能找到**：不在安裝目錄中（其 `data/Licenses.txt` 只含第三方授權），也不在發行商的網站上，而 Steam 的 EULA 頁面也無法載入。在依賴本工具之前，請自行查核。
本工具只讀取封存檔，從不修改它們。它所寫出的關卡只應留在你的電腦上：**請勿發布**。本工具不附帶任何遊戲資料，而測試會建立它們讀取的每一個檔案。

## 授權 {#licence}

MIT——見 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE)。使用 numpy（BSD-3-Clause），並可選用 numba（BSD-2-Clause）。`heat3d_update` 是 3DHeat 工具共用的更新程式。
