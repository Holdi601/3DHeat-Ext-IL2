---
title: "速度、测试与条款"
nav_order: 7
lang: "zh"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# 速度、测试与条款 {#speed-tests-terms}

## 速度 {#speed}

除非安装了 numba（`python -m pip install -e .[fast]`），解码使用纯 Python：中等大小的地图在没有 numba 时约需 15 秒，有 numba 时约需一秒；最大的地图（数亿个采样点）在有 numba 时约需 7 秒（首次运行还会进行编译）。内存只占用一行扇区加上输出网格。

## 测试 {#tests}

```bash
python -m pytest -q
```

`tests/synth.py` 用代码构建归档、高度图（即上面编解码器的编码器）、`height.hini` 文件，以及没有文件表的归档。

## 条款 {#the-terms}

IL-2 Sturmovik: Great Battles 和 IL-2 Series（1C Game Studios / 777 Studios）的许可协议**未能找到**：不在安装目录中（其 `data/Licenses.txt` 只包含第三方许可证），不在发行商的网站上，Steam 的 EULA 页面也未能加载。在依赖本工具之前，请你自己核对一下。
本工具只读取归档，从不修改它们。它生成的关卡只保存在你的电脑上：**切勿发布**。本工具不附带任何游戏数据，测试程序构建了它读取的每一个文件。

## 许可证 {#licence}

MIT：参见 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE)。使用 numpy（BSD-3-Clause），以及可选的 numba（BSD-2-Clause）。`heat3d_update` 是 3DHeat 工具共用的更新程序。
