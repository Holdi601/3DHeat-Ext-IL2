---
title: "파일을 읽는 방법"
nav_order: 5
lang: ko
source: reading.md
source_hash: "3c0d5d19e02e"
nav_exclude: true
search_exclude: true
---
# 파일을 읽는 방법 {#how-the-files-are-read}

| 부분 | 상태 |
|---|---|
| 아카이브 (`data/*.gtp`, Great Battles) | 파일 표(`S16R`, `STRMFAT?`, `DIR!`/`FILE` 기록)와 항목(`STRMFILE` 헤더, 데이터는 있는 그대로 저장됨). 테스트 설치본의 모든 `Maps*.gtp` |
| `height.hini` | `height_map`, `water_map`, `heightMul`, `SeaLevel`, 플레이 한계, `MapNW/NE/SE/SW`. 테스트 설치본의 모든 것 |
| 높이 맵 (`height.dat`) | 아래의 코덱. 이것을 알아내는 동안 전체를 해독한 맵의 모든 섹터는 비트스트림을 정확히 씁니다(남는 것은 바이트 패딩뿐). 나머지는 헤더로 확인함. 게임이 `distlod.dat` 옆에 같이 제공하는 압축되지 않은 `distlod.raw` 파일과 비트 단위로 일치하고, 맵 자체의 먼 거리 LOD 높이 맵과도 일치함(상관 0.999) |
| 높이 | 미터 = 원본 값 x heightMul / 256 - SeaLevel x heightMul. 맵의 바다는 hini 주석이 주는 높이와 정확히 같게 해독되며, 다른 맵의 경계는 `bounds_level`과 같게 해독됨 |
| 위치 | hini의 네 모서리 사이를 쌍선형으로 보간. 0행은 북쪽, 0열은 서쪽. 한 맵을 알려진 마을, 해안, 바다와 대조해 확인했음(마을 높이는 실제와 약 10m 이내, 바다는 해수면 아래). 모서리는 사각형일 뿐 게임 자체의 투영이 아니므로, 큰 맵의 가운데에서는 수백 미터의 오차를 예상하세요. 한 맵 계열의 hini는 다른 맵의 모서리를 담고 있습니다(실제 크기의 일부만 덮습니다). 이것은 감지되며, 그 계열은 대신 랜드마크 맞춤으로 정합니다. 게임 자체의 위치 데이터베이스(`*.ldfbin`)의 마을과 비행장을 실제 위치와 맞추며, 제곱근 평균 오차는 약 2km입니다(마을은 이름이 같은 비행장과 대조하고, 실제 장소의 좌표는 약 1km 정확도). JSON에는 모든 랜드마크와 그 잔차가 나열됩니다 |
| 물 마스크 (`water.wtr`: 타일의 피라미드 네 단계, 각 타일은 400m 블록의 표이며, 각 블록은 육지, 전체가 물, 또는 일부가 물이고 그 모양이 비트스트림에 들어 있음) | 컨테이너는 모든 맵에서 읽음(전체를 해독한 파일에는 남는 바이트가 없음). 일부만 물인 블록 안의 모양은 **해독하지 않음**. 전체가 물인 블록은 물입니다. 일부만 물인 블록에서는, 물 맵(`height_w.dat`, 높이 맵과 같은 코덱)이 지면보다 높은 곳이면 샘플이 물이고, 호수 옆에서는 지면이 호수보다 높지 않은 곳이 물입니다. 육지 블록은 마른 땅입니다. 이것으로 물 맵만으로는 물로 보고되는 습지가 사라집니다. 출력 격자보다 좁은 강은 조각나서 나옵니다 |
| 마을 윤곽 (`textures.tini`가 나열하는 데칼 메시: `towns.mesh`, `cities.mesh`, `city_*.mesh`, `roads_fields.mesh` 등. 25.6km 타일의 평평한 텍스처 삼각형) | 모든 맵에서 읽음. 텍스처가 마을, 촌락, 또는 산업 지대인 면은 남깁니다. 몇 맵의 실제 마을과 대조해 확인했음(강의 양쪽 기슭에 걸친 마을, 합류점). 이것은 윤곽일 뿐입니다. 건물은 게임이 실행 중에 놓으며, 파일에는 건물이 없습니다 |
| 비행장, 다리, 건물 | **읽지 않음**: 비행장은 미션 객체이고, 건물은 게임 자체의 배치에서 옵니다 |
| 숲 (`forest_map.wtr`) | 블록은 같은 방식으로 읽지만, 거의 모든 블록이 "일부가 숲"이므로 비트스트림이 없으면 쓸 수 있는 숲 마스크가 없습니다. 그리지 않음 |
| 지면의 텍스처 | 읽지 않음 |

## 높이 맵 코덱 {#the-heightmap-codec}

데이터 파일만으로 알아냈습니다. 게임 코드는 읽거나 역어셈블하지 않았습니다. 리틀 엔디안:

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

오른쪽과 아래 가장자리의 부분 섹터는 패딩한 뒤 잘라 냅니다. 같은 코덱이 물 맵과 먼 거리 LOD 높이 맵에도 쓰입니다.

## 랜드마크 맞춤 {#landmark-fits}

맵의 모서리를 쓸 수 없을 때, `landmarks.py`가 게임 미터에서 지구로 가는 아핀 변환을 최소 제곱법으로 맞춥니다. 게임 위치는 사용자 본인의 파일(미션의 `Airfield` 블록, 경력 위치 데이터베이스)에서, 실제 위치는 코드 안에 있는 장소들의 공개 좌표 표에서 가져옵니다. JSON의 `georeference`에는 행렬, 원점, 모든 랜드마크와 그 잔차, 그리고 제곱근 평균 오차가 들어 있습니다.
