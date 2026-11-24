> 작성일: Oct.14.2026

> 학습내용: Cartographer 파라미터 

# 개인 업무일지 - 2026-10-08 (목)

| 항목 | 내용 |
|---|---|
| 작업 시간 | 17:36 ~ 19:41 |
| 주요 업무 | Lv2 모듈 ⑤ 카메라 객체 추적 팀 과제: 발제 분석, 보고서 작성, ROS 2 bag 구성, 프로젝트 검증, 탐색 모드 구현 |
| 대상 저장소 | `~/GIT/Lv2_EYE4_Assignments_test` (팀 저장소, `dev/test1`), `~/GIT/Final_assignment` (현재 `Lv2_EYE4_Final_assignment`) |
| 사용 도구 | ROS 2, Git, Claude Code |

## 1. 요약
- 발제 문서를 분석해 제출물 목차와 보고서 작성 틀을 정리함.
- `report.md`를 발제 형식(문제 1~5, 7단계)에 맞춰 작성함. 실측 근거가 있는 값만 기록하고 나머지는 TODO로 남김.
- ROS 2 bag 기록·재현 가이드를 작성하고, Final_assignment 프로젝트에 bag 기록·재현 도구를 구성함.
- 전체 프로세스를 코드 수정 없이 검증하고 결과 보고서를 작성함. 시급한 결함 2건을 찾음.
- 목표 소실 시 탐색(SEARCHING) 모드, 0.5 rad/s 추적, 경계 정지 시 ARM 유지를 구현하고 라이브 테스트 절차를 정리함.

## 2. 상세 내용

### 2.1 발제 문서 분석 (문서 수정 없음)
- 대상: `lv2_module5/docs/18-08-26.md`.
- 과제 목표: USB 카메라로 단일 색상 목표 검출 → 화면 중심 오차로 다이나믹셀 추적. 목표 소실·통신 단절 시 정지, 다시 보이면 복귀.
- 제출물 목차 정리: 루트 README, 실행 가이드, `report.md`, `team.md`, `presentation.md`, ROS2 코드, OpenCR 펌웨어, 설정, 결과물, bag 안내.
- 문제 1~5별로 보고서에 꼭 들어갈 핵심 항목을 표로 정리함 (HSV·Contour 검출, 인지·제어 연결, P 추적 제어, 성능·소실 복구, bag 기록·재현).

### 2.2 보고서 작성 (`lv2_module5/report.md`)
- 구성: 0절 목표·시험 계획, 문제 1~5 각각 7단계(구현 → 실행 조건 → 결과물 → 측정 → 해석 → 심화 → 한계), 평가표 연결, AI 사용 범위.
- 실측 원본이 있는 값만 기록함: 검출률 30/30, 배경 오검출 0/10, 처리 30.03 fps. 단위 시험 34개 통과.
- 작성 중 발견한 문제:
  - 속도 상한 값이 파일마다 다름 (호스트 0.3, 커밋된 펌웨어 0.05, 작업 트리 펌웨어 0.5 rad/s).
  - Tilt 방향 표기가 문서마다 다름.
  - Kp 0.3은 A/B 비교로 정한 값이 아님.
  - 협업 요건 미충족 (병합된 PR, 리뷰 링크 부족).
- 필수 실기 시험(폐루프 부호, Kp 6회, 30초 추적, 가림 5회, 통신 중단, bag)은 아직 수행 전이라 중간본으로 정리함.

### 2.3 ROS 2 bag 기록·재현 가이드 (`lv2_module5/docs/rosbag_guide.md`)
- 발제 문제 5의 요구사항 11개와 각 증거 위치를 표로 정리함.
- 저장 공간 계산 (영상만 약 27.6 MB/s, 30초에 약 0.83 GB), SSH 끊김 대비(tmux), 기록할 토픽, 기록 직후 확인 방법.
- 재생 시 모터 출력을 막는 3겹 안전 절차 (USB 분리, 노드 종료, 격리 도메인).
- 원본 `/target`과 재처리 결과를 같은 시각으로 맞춰 프레임 단위로 비교하는 방법.

### 2.4 Final_assignment 프로젝트 bag 도구 구성
- 새로 만든 것: `config/bag.yaml`, `tools/bag_record.sh`, `tools/bag_replay.sh`, `tools/bag_tool.py`.
  - 기록 전 점검(필수 토픽, 저장 공간, 저장소 밖 폴더) → 실제 파라미터 저장 → 기록 → 메시지 수 판정·체크섬·기준 커밋 저장.
  - 재생 전 모터 차단 확인 → 재처리/재분석 → 자동 대조 (실패 시 exit 1).
- 기존 파일: `tools/eval_frames.py`에 `--output-dir` 옵션 추가, README·recordings 문서 갱신.
- 이 PC에 ROS가 없어 가짜 ros2 환경으로 검증함: 거부 조건 7가지, 정상 종료, 대조 PASS/FAIL 판정 확인.

### 2.5 전체 프로세스 검증 (`lv2_module5/docs/project_process_verification.md`, 코드 수정 없음)
- 시급한 결함 2건:
  1. 경계 도달 시 펌웨어(`EVENT LIMIT STOPPED`, ARM 유지)와 bridge(FAULT 처리 후 DISARM)가 서로 맞지 않음.
  2. bridge 상태를 10 ms마다 발행해 Pi 부하로 명령 timeout 위험.
- 그 밖에 속도 감시 여유 부족 등 개선 권장 항목을 정리함.

### 2.6 탐색 모드 구현과 라이브 테스트 절차
- 요구 기능:
  - 목표가 없으면 Pan·Tilt 최대 범위로 탐색하고, 찾지 못하면 모터를 멈추고 idle.
  - 목표가 보이면 0.5 rad/s로 추적.
  - 최대 가동 범위를 넘으면 탐색으로 전환.
- 경계 처리는 (a) ARM 유지 방식으로 구현함: bridge가 `EVENT LIMIT STOPPED`를 받으면 대기 중인 응답을 해제하고 정지 완료 후 재개.
- Pi에서 실행할 라이브 테스트 절차를 단계별 통과 기준과 함께 정리함 (단위 시험 50개, host 시험 DRY/LIVE_STUB, DRY 펌웨어 → LIVE 펌웨어 순서).
- 커밋 메시지 작성: `feat: 목표 소실 시 Pan/Tilt 전 범위 탐색(SEARCHING), 0.5 rad/s 추적, 경계 정지 때 ARM 유지(EVENT LIMIT 처리) 추가`

## 3. 결과물

| 파일 | 내용 |
|---|---|
| `Lv2_EYE4_Assignments_test/lv2_module5/report.md` | 최종 보고서 (중간본, 실측 TODO 포함) |
| `Lv2_EYE4_Assignments_test/lv2_module5/docs/rosbag_guide.md` | ROS 2 bag 기록·재현 가이드 |
| `Final_assignment/lv2_module5/config/bag.yaml`, `tools/bag_*.sh`, `tools/bag_tool.py` | bag 기록·재현·대조 도구 |
| `Final_assignment/lv2_module5/docs/project_process_verification.md` | 전체 프로세스 검증 보고서 |

## 4. 다음 할 일
- [ ] Pi·실장비에서 라이브 테스트 진행 (DRY → LIVE, 탐색 모드, 경계 정지).
- [ ] 필수 실기 시험 수행 후 보고서 TODO 채우기.
- [ ] 변경 사항 커밋 범위 정리 (bag 도구, 검증 보고서, 탐색 기능).
- [ ] 협업 요건 (PR 병합, 리뷰 링크) 보완.


