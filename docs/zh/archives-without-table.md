---
title: 没有文件表的归档
nav_order: 6
lang: "zh"
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# 归档没有文件表的游戏 {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea 的归档中不保存可读的文件表（文件名以哈希形式存放在每个归档末尾的一个块中），其设置文件也不以可读形式保存。`list` 会将其地图显示为游戏 `Korea`。因此：

- 其高度图和水域图是通过文件头找到的（`height.dat` 的布局，以 128 个采样点为一个扇区；网格非常大，单元尺寸很小）；
- 它在地球上的位置，是通过将其任务中放置的机场（`data/Missions/**/*.Mission`，在你的电脑上读取）拟合到真实机场公布的坐标上而确定的（`korea.py`）：残差为几十米到几百米。JSON 会列出每个地标及其残差；
- heightMul 和 SeaLevel 是估算出来的：任务中的舰船位于海面上，因此它们在水域图最常见（海面）的数值之上的高度，可以给出比例。高度看起来合理（海面位于海平面以下，沿海城镇位于几米高处），但未作进一步检查。JSON 会将它们标记为估算值。
