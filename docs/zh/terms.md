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

此工具读取你电脑上你自己的 IL-2 Sturmovik: Great Battles 安装中的归档文件，且从不修改它们。

不随附也不再分发游戏中的任何东西：没有游戏文件、没有游戏代码、没有 DLL；测试会自行生成它们读取的每个文件。它写出的关卡留在你的电脑上。

3DHeat IL-2 与 1C Game Studios / 777 Studios 无关联，也未获其认可。IL-2 Sturmovik 及相关名称和商标归其各自所有者所有。

权利人：请在 [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues) 提交 issue——我们会迅速回复，并按要求删除任何内容。

## 许可证 {#licence}

MIT：参见 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE)。使用 numpy（BSD-3-Clause），以及可选的 numba（BSD-2-Clause）。`heat3d_update` 是 3DHeat 工具共用的更新程序。
