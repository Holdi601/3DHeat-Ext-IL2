---
title: "레벨 만들기: extract"
nav_order: 3
lang: ko
source: extract.md
source_hash: "2a45af525c58"
nav_exclude: true
search_exclude: true
---
# 레벨 만들기: `extract` {#building-levels-extract}

```text
heat3d-il2-level extract (<map> ... | --all) -o <folder> [--game FOLDER ...]
                 [--max-grid N] [--frame enu|game] [--origin LAT LON]
                 [--no-water] [--no-towns] [--skip-existing]
```

## 단계별 안내 {#step-by-step}

명령줄이 처음입니까? 먼저 [시작하기 전에](before-you-start.md)를 읽으세요.

1. [`list`](list.md)로 맵의 이름을 찾으세요.
2. `heat3d-il2-level extract <map> -o levels`를 실행하세요. 이름에는 와일드카드를 쓸 수 있으며, 따옴표로 감싸세요(`"<family>_*"`). `--all`은 모든 맵을 가져옵니다.
3. 기록을 레벨 위에 놓을 때 위치 맞추기 단계가 필요 없게 하려면, 기록의 `geo`(세션의 기준점)를 `--origin <lat> <lon>`으로 주세요. 주지 않으면 맵의 가운데가 원점이 되며, `.json`의 `geo`가 어느 쪽인지 알려 줍니다.
4. 명령은 맵을 해독할 때마다 한 줄을 출력하고, 끝에는 `ok <glb> <triangles> (<frame> frame)` 또는 `failed <map>: <why>`를 출력합니다.
5. 뷰어의 배경 / 레벨 패널에서 `<folder>/<map>/<map>.glb`를 불러오세요.

![가상 설치본에 대한 extract](../assets/img/extract.svg)

게임 자체의 미터 단위로, 물을 빼고:

![extract --frame game --no-water](../assets/img/extract-game.svg)

이미 쓴 맵이 있을 때 다시 실행한 경우:

![extract --all --skip-existing](../assets/img/extract-skip.svg)

## 옵션 {#options}

| 옵션 | 기본값 | 하는 일 |
|---|---|---|
| `maps` | - | `list`가 출력하는 맵 이름. 와일드카드 가능 |
| `--all` | 꺼짐 | 모든 맵. 높이 맵과 물 맵을 공유하는 계절들은 한 번만 씁니다 |
| `-o`, `--out` | 필수 | 출력 폴더. 각 맵은 `<out>/<map>/`에 들어갑니다 |
| `--game FOLDER` | 자동으로 찾음 | IL-2 폴더 (여러 번 줄 수 있음) |
| `--max-grid N` | `1024` | 한 변의 높이 샘플 최대 수 (1024: 약 200만 삼각형). 맵은 맞추기 위해 *k* 샘플마다 하나씩 뽑습니다 |
| `--frame` `enu` 또는 `game` | `enu` | `enu`: `--origin`을 기준으로 동쪽 미터, 고도, 북쪽. Watcher의 Tacview 표와 같습니다. `game`: 게임 자체의 미터(x 북쪽, y 위, z 동쪽). 지구상에 놓을 수 없는 맵은 무엇을 요청하든 `game`으로 씁니다 |
| `--origin LAT LON` | 맵의 가운데 | `enu` 좌표계의 원점 (기록의 `geo`) |
| `--no-water` | 꺼짐 | 물을 뺌 |
| `--no-towns` | 꺼짐 | 마을의 지붕 윤곽(footprint)을 뺌 |
| `--skip-existing` | 꺼짐 | `.glb`가 이미 있는 맵은 그대로 둠 |

프로그램이 출력하는 모든 옵션: [명령 참조](../cli-reference.md).

`HEAT3D_DEBUG`를 설정하면 실패한 맵의 전체 추적 정보를 출력합니다. `.glb`는 `<map>.glb.part`로 쓰고, 완료되면 이름을 바꿉니다.

종료 상태: 0은 모든 맵을 씀, 1은 실패한 맵이 하나라도 있음(나머지는 그래도 씁니다), 2는 설치본이 없거나 맞는 맵이 없음입니다.

## 예시 {#examples}

```bash
heat3d-il2-level extract <map> -o levels                         # 맵 하나, 가운데 주변의 enu 좌표계
heat3d-il2-level extract <map> --origin <lat> <lon> -o levels    # 그 geo를 가진 기록의 평면 맵 안에서
heat3d-il2-level extract "<family>_*" --max-grid 2048 -o levels  # 더 세밀하게, 여러 맵
heat3d-il2-level extract --all --skip-existing -o levels         # 모든 맵, 새 것만
heat3d-il2-level extract <map> --frame game -o levels            # 게임 자체의 미터, 미션 파일이 쓰는 그대로
```

파일에 무엇이 들어 있는지: [레벨 파일과 좌표계](output.md).
