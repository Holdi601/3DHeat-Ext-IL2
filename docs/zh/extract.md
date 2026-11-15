---
title: "构建关卡：extract"
nav_order: 3
lang: zh
source: extract.md
source_hash: "69fb5c2ddfa7"
nav_exclude: true
search_exclude: true
---
# 构建关卡：`extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## 逐步说明 {#step-by-step}

第一次使用命令行？请先阅读 [开始之前](before-you-start.md)。

1. 用 [`list`](list.md) 找到地图的名称。
2. 运行 `heat3d-il2-level extract <map> -o levels`。名称可以使用通配符，并加上引号（`"<family>_*"`）；`--all` 会处理每一张地图。
3. 要让录制在关卡上正确定位而无需摆放步骤，请指定其原点：将 `--origin <lat> <lon>` 设为录制的 `geo`（其会话的参考点）。如果不指定，地图的中心即为原点，而 `.json` 中的 `geo` 会说明是哪一个。
4. 命令会在解码每张地图时打印一行，然后输出 `ok <glb> <triangles> (<frame> frame)`，或者 `failed <map>: <why>`。
5. 在查看器的 **背景/关卡面板** 中加载 `<folder>/<map>/<map>.glb`。

![在合成安装上运行 extract](../assets/img/extract.svg)

使用游戏自身的米制，并且不包含水域：

![extract --frame game --no-water](../assets/img/extract-game.svg)

对已经写出的地图进行第二次运行：

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## 选项 {#options}

| 选项 | 默认值 | 作用 |
|---|---|---|
| `maps` | - | `list` 打印的地图名称；可以使用通配符 |
| `--all` | 关闭 | 每一张地图；共享同一高度图和水域图的季节版本只写一次 |
| `-o`、`--out` | 必填 | 输出文件夹；每张地图放入 `<out>/<map>/` |
| `--game FOLDER` | 自动查找 | 一个 IL-2 文件夹（可重复使用） |
| `--max-grid N` | `1024` | 每边最多的高度图采样点数（1024：约 200 万个三角形）；地图会每隔 *k* 个采样点取样，以适应该数量 |
| `--frame` `enu` 或 `game` | `enu` | `enu`：以东向米、海拔高度、北向米表示，相对于 `--origin`，与 Watcher 的 Tacview 表格相同；`game`：游戏自身的米制（x 为北，y 为向上，z 为东）。无法在地球上摆放的地图，无论请求什么，都会以 `game` 写出 |
| `--origin LAT LON` | 地图中心 | `enu` 坐标系的原点（录制的 `geo`） |
| `--no-water` | 关闭 | 不包含水域 |
| `--no-towns` | 关闭 | 不包含城镇的占地轮廓 |
| `--skip-existing` | 关闭 | 跳过已经存在 `.glb` 的地图 |

每个选项的完整说明，即程序自己打印的内容：[命令参考](../cli-reference.md)。

设置环境变量 `HEAT3D_DEBUG` 可以打印失败地图的完整回溯信息。`.glb` 会先写入 `<map>.glb.part`，完成后再重命名。

退出状态：0 表示所有地图都已写出；1 表示有任何一张失败（其余仍会写出）；2 表示未找到安装，或没有地图匹配。

## 示例 {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # 一张地图，以其中心为中心的 enu 坐标系
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # 在具有该 geo 的录制的平面地图中
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # 更精细，多张地图
heat3d-il2-level extract --all --skip-existing -o levels         # 每一张地图，只处理新的
heat3d-il2-level extract <map> --frame game -o levels            # 游戏自身的米制，与任务文件中的一致
```

文件中包含什么：[关卡文件与坐标系](output.md)。
