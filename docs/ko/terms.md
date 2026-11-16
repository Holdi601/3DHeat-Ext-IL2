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

이 도구는 여러분의 컴퓨터에 있는 여러분 자신의 IL-2 Sturmovik: Great Battles 설치본의 아카이브를 읽으며, 절대 변경하지 않습니다.

게임의 어떤 것도 함께 배포되거나 재배포되지 않습니다. 게임 파일도, 게임 코드도, DLL도 없습니다. 테스트는 읽는 모든 파일을 직접 만듭니다. 이 도구가 쓰는 레벨은 여러분의 컴퓨터에 남습니다.

3DHeat IL-2은(는) 1C Game Studios / 777 Studios와(과) 제휴 관계가 없으며 승인을 받지 않았습니다. IL-2 Sturmovik 및 관련 이름과 상표는 각 소유자에게 있습니다.

권리자분들께: [github.com/Holdi601/3DHeat-Ext-IL2/issues](https://github.com/Holdi601/3DHeat-Ext-IL2/issues)에서 이슈를 열어 주세요. 빠르게 답하고 요청하시면 무엇이든 삭제합니다.

## 라이선스 {#licence}

MIT입니다. 자세한 내용은 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-IL2/blob/main/LICENSE)를 보세요. numpy(BSD-3-Clause)를 쓰며, 선택 사항으로 numba(BSD-2-Clause)를 씁니다. `heat3d_update`는 3DHeat 도구들이 함께 쓰는 업데이터입니다.
