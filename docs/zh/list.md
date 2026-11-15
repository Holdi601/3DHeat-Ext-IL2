---
title: "查找地图：list"
nav_order: 2
lang: "zh"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# 查找地图：`list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          同上，无需安装
```

第一次使用命令行？请先阅读 [开始之前](before-you-start.md)。

1. 安装一次：`git clone https://github.com/Holdi601/3DHeat-Ext-IL2`，在该文件夹中打开终端并运行 `python -m pip install -e .`（需要 Python 3.10 或更高版本；它会安装 numpy；`python -m pip install -e .[fast]` 还会加装 numba）。
2. 运行 `heat3d-il2-level list`。
3. 每张地图输出一行，以制表符分隔：它的名称（`extract` 使用的名称）、游戏（`Great Battles`，或者对于[第二款游戏](archives-without-table.md)为 `Korea`）、它所读取的高度图，以及它在地球上的位置：即根据地图角点得出的纬度/经度范围，或者用来定位它的地标拟合，或者“not placed on the earth”（未在地球上定位）。最后一行（输出到标准错误）统计地图数量并列出安装位置。

![在合成安装上运行 list](../assets/img/list.svg)

图片是在由测试程序的写入器构建的一个安装（`tests/synth.py`）上的运行结果，而不是在游戏上的运行结果。

## 安装位置如何被找到 {#where-the-installs-are-found}

通过 Steam 查找；否则使用 `--game <folder>`（可重复使用，每个安装一次），或者环境变量 `HEAT3D_IL2_GAME`。安装目录是指其 `data` 文件夹中含有 `Maps*.gtp` 归档的文件夹。

| 选项 | 作用 |
|---|---|
| `--game FOLDER` | 一个 IL-2 文件夹；有多个安装时重复使用此选项 |

退出状态：0 表示完成；2 表示未找到安装。
