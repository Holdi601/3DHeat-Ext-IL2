---
title: "如何读取文件"
nav_order: 5
lang: "zh"
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# 如何读取文件 {#how-the-files-are-read}

| 部分 | 状态 |
|---|---|
| 归档（`data/*.gtp`，Great Battles） | 文件表（`S16R`、`STRMFAT?`、`DIR!`/`FILE` 记录）和条目（`STRMFILE` 文件头，数据按原样存储）；测试安装中的每个 `Maps*.gtp` 均已读取 |
| `height.hini` | `height_map`、`water_map`、`heightMul`、`SeaLevel`、游戏区域的限制，以及 `MapNW/NE/SE/SW`；测试安装中的每一个都已读取 |
| 高度图（`height.dat`） | 下方的编解码器；在研究过程中完整解码的地图，其每个扇区都精确地使用了其位流（最多剩余字节的填充），其余的通过文件头检查。已与游戏附带在 `distlod.dat` 旁边的未压缩 `distlod.raw` 文件逐位比对一致，并与某张地图自身的远景 LOD 高度图比对（相关系数 0.999） |
| 高度 | 米 = 原始值 x heightMul / 256 - SeaLevel x heightMul。某张地图的海面解码结果，恰好等于其 hini 注释给出的高度；另一张地图的边界则等于其 `bounds_level` |
| 定位 | 在 hini 的四个角点之间进行双线性插值，第 0 行朝北，第 0 列朝西。已在某张地图上，对照已知的城镇、海岸和海洋进行检查（城镇高度与真实高度相差约 10 米以内，海洋位于海平面以下）。这些角点构成的是一个四边形，而不是游戏自身的投影，因此在大型地图的中部，预计会有数百米的误差。某一地图系列的 hini 中保存的是另一张地图的角点（它们只覆盖其真实大小的一小部分）；这一情况会被检测到，此时该系列改为通过地标拟合来定位：使用游戏自身位置数据库（`*.ldfbin`）中的城镇和机场与其真实位置进行比对，均方根误差约为几公里（城镇与以其命名的机场比对，真实地点的坐标精确到约一公里）；JSON 会列出每个地标及其残差 |
| 水域蒙版（`water.wtr`：四级金字塔状的瓦片，每个瓦片是一张 400 米块的表格，每个块为陆地、完全被水覆盖，或部分有水，其形状保存在位流中） | 每张地图都会读取容器（在完整解码的文件中没有剩余字节）；部分有水的块内部的形状**未被解码**。完全有水的块即为水域；在部分有水的块中，当水域图（`height_w.dat`，与高度图相同的编解码器）高于地面时，采样点为水域；或者在湖泊旁边，当地面不高于湖面时，同样为水域；陆地块则是干燥的。这样就去除了仅凭水域图会被当作水域的沼泽。比输出网格还窄的河流会被切成碎片 |
| 城镇占地（`textures.tini` 列出的贴花网格：`towns.mesh`、`cities.mesh`、`city_*.mesh`、`roads_fields.mesh` 等：25.6 公里的瓦片，由平坦的贴图三角形构成） | 每张地图都会读取；保留贴图为城镇、村庄或工业用地的面。已在几张地图上与真实城镇进行比对（河流两岸的城镇、汇流处）。它们只是占地轮廓：游戏在运行时才放置建筑，文件中并不包含建筑 |
| 机场、桥梁、建筑 | **未读取**：机场是任务对象，建筑由游戏自身的放置决定 |
| 森林（`forest_map.wtr`） | 其块的读取方式相同，但几乎每个块都是“部分有森林”，因此没有位流就无法得到可用的森林蒙版；未绘制 |
| 地面的贴图 | 未读取 |

## 高度图编解码器 {#the-heightmap-codec}

仅根据数据文件推导得出；未读取或反汇编任何游戏代码。字节序为小端：

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

右边缘和下边缘的不完整扇区会被填充并裁剪。同一编解码器也适用于水域图和远景 LOD 高度图。

## 地标拟合 {#landmark-fits}

当无法使用地图的角点时，`landmarks.py` 会通过最小二乘法，将游戏米制拟合为地球上的仿射映射：游戏中的位置取自用户自己的文件（任务中的 `Airfield` 块、职业生涯的位置数据库），真实位置则取自代码中按地点公布坐标制成的表格。JSON 的 `georeference` 包含矩阵、原点、每个地标及其残差，以及均方根误差。
