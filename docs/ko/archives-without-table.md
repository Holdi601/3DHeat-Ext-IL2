---
title: 파일 표가 없는 아카이브
nav_order: 6
lang: ko
source: archives-without-table.md
source_hash: "58c4c46721e5"
nav_exclude: true
search_exclude: true
---
# 아카이브에 파일 표가 없는 게임 {#a-game-whose-archives-have-no-file-table}

IL-2 Series: Korea는 아카이브 안에 읽을 수 있는 파일 표를 두지 않습니다(파일 이름은 각 아카이브 끝의 블록에 해시되어 있습니다). 그리고 설정 파일도 읽을 수 있는 형태로 저장되어 있지 않습니다. `list`는 이 게임의 지도를 `Korea` 게임으로 보여 줍니다. 그래서 다음과 같이 처리합니다:

- 높이 지도와 물 지도는 헤더로 찾습니다(`height.dat` 구조, 128 샘플 단위의 섹터. 매우 큰 격자이며 셀 크기가 작습니다).
- 지도는 지구상에 놓이는데, 미션이 배치한 비행장(`data/Missions/**/*.Mission`, 본인의 컴퓨터에서 읽습니다)을 실제 비행장의 공개 좌표(`korea.py`)에 맞춰 정합니다. 잔차는 수십 미터에서 몇백 미터입니다. JSON에 각 랜드마크와 그 잔차가 나열됩니다.
- heightMul과 SeaLevel은 추정합니다. 미션의 배들은 바다 위에 있으므로, 그 높이를 물 지도에서 가장 흔한(바다) 값과 비교해 비율을 얻습니다. 높이는 그럴듯하게 나옵니다(바다는 해수면 아래, 해안 마을은 몇 미터). 더 확인하지는 않았습니다. JSON에는 추정값이라고 표시됩니다.
