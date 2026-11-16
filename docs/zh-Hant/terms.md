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

此工具讀取你電腦上你自己的 IL-2 Sturmovik: Great Battles 安裝中的封存檔，且從不修改它們。

不隨附也不再散布遊戲中的任何東西：沒有遊戲檔案、沒有遊戲程式碼、沒有 DLL；測試會自行產生它們讀取的每個檔案。它寫出的關卡留在你的電腦上。

3DHeat IL-2 與 1C Game Studios / 777 Studios 無關聯，也未獲其認可。IL-2 Sturmovik 及相關名稱和商標歸其各自所有者所有。

權利人：請在 [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) 提出 issue——我們會迅速回覆，並依要求移除任何內容。

## 授權 {#licence}

MIT——見 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE)。使用 numpy（BSD-3-Clause），並可選用 numba（BSD-2-Clause）。`heat3d_update` 是 3DHeat 工具共用的更新程式。
