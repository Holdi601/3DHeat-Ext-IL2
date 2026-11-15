---
title: "속도, 테스트, 약관"
nav_order: 7
lang: "ko"
source: terms.md
source_hash: "5f420f7d2d05"
nav_exclude: true
search_exclude: true
---
# 속도, 테스트, 약관 {#speed-tests-terms}

## 속도 {#speed}

numba가 설치되어 있지 않으면 해독은 순수 Python으로 합니다(`python -m pip install -e .[fast]`로 설치). 중간 크기의 맵은 numba 없이 약 15초, 있으면 약 1초가 걸립니다. 가장 큰 맵(샘플 수억 개)은 numba가 있을 때 약 7초입니다(첫 실행은 컴파일도 합니다). 메모리는 섹터 한 줄과 출력 격자만큼만 씁니다.

## 테스트 {#tests}

```bash
python -m pytest -q
```

`tests/synth.py`는 아카이브, 높이 맵(위 코덱의 인코더), `height.hini` 파일, 그리고 파일 표가 없는 아카이브를 코드로 만듭니다.

## 약관 {#the-terms}

IL-2 Sturmovik: Great Battles와 IL-2 Series(1C Game Studios / 777 Studios)의 라이선스 계약서는 **찾지 못했습니다**. 설치본(그 `data/Licenses.txt`에는 제3자 라이선스만 있습니다)에도, 퍼블리셔의 사이트에도 없었고, Steam EULA 페이지도 열리지 않았습니다. 이것에 의존하기 전에 직접 확인하세요. 이 도구는 아카이브를 읽기만 하고 절대 바꾸지 않습니다. 이 도구가 쓰는 레벨은 본인의 컴퓨터에만 두세요. **절대 게시하지 마세요.** 여기에는 게임 데이터가 전혀 들어 있지 않으며, 테스트는 읽는 모든 파일을 직접 만듭니다.

## 라이선스 {#licence}

MIT입니다. 자세한 내용은 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE)를 보세요. numpy(BSD-3-Clause)를 쓰며, 선택 사항으로 numba(BSD-2-Clause)를 씁니다. `heat3d_update`는 3DHeat 도구들이 함께 쓰는 업데이터입니다.
