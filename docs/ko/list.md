---
title: "맵 찾기: list"
nav_order: 2
lang: "ko"
source: list.md
source_hash: "8c7cf438be16"
nav_exclude: true
search_exclude: true
---
# 맵 찾기: `list` {#finding-maps-list}

```text
heat3d-il2-level list [--game FOLDER ...]
python -m heat3d_ext_il2 list ...          설치 없이 같은 동작
```

명령줄이 처음입니까? 먼저 [시작하기 전에](before-you-start.md)를 읽으세요.

1. 한 번만 설치하세요: `git clone https://github.com/Holdi601/3DHeat-Ext-IL2`, 그 폴더에서 터미널을 열고 `python -m pip install -e .`를 실행합니다 (Python 3.10 이상. numpy가 함께 설치되며, `python -m pip install -e .[fast]`를 쓰면 numba도 추가됩니다).
2. `heat3d-il2-level list`를 실행하세요.
3. 맵마다 탭으로 구분된 한 줄이 출력됩니다. 줄에는 이름(`extract`가 받는 이름), 게임(`Great Battles`, 또는 [두 번째 게임](archives-without-table.md)인 `Korea`), 읽을 높이 맵, 그리고 지구상의 위치가 나옵니다. 위치는 맵 모서리로 본 위도/경도 상자이거나, 그것을 정하는 랜드마크 맞춤이거나, "not placed on the earth"(지구상에 놓이지 않음)입니다. 마지막 줄(표준 오류 출력)은 맵 수를 세고 설치본의 이름을 알려 줍니다.

![가상 설치본에 대한 list](../assets/img/list.svg)

그림은 테스트 작성 도구가 만든 설치본(`tests/synth.py`)에서 실행한 결과이며, 게임에서 실행한 것이 아닙니다.

## 설치본을 찾는 곳 {#where-the-installs-are-found}

Steam을 통해 찾습니다. 그렇지 않으면 `--game <folder>`(설치본마다 한 번씩, 여러 번 가능) 또는 `HEAT3D_IL2_GAME` 환경 변수를 씁니다. 설치본은 `data` 안에 `Maps*.gtp` 아카이브가 있는 폴더입니다.

| 옵션 | 하는 일 |
|---|---|
| `--game FOLDER` | IL-2 폴더. 여러 설치본이면 반복해서 씁니다 |

종료 상태: 0은 완료, 2는 설치본을 찾지 못함입니다.
