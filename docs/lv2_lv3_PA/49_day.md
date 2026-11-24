> 작성일 : Oct.19.2026 (Mon)

> 아이작심, 엔비디아의 생태계에 대해서 배워보자. 
> 강화 학습이란 무엇일까

# 개인 업무일지 - 2026-10-15 (목)

| 항목 | 내용 |
|---|---|
| 작업 시간 | 11:57 ~ 16:11 (개발 PC 복구), 19:19 ~ 20:56 (TeamRobot 3D 모델) |
| 주요 업무 | ① 개발 PC 패키지 관리자 고장 진단·복구 ② TeamRobot 4륜 섀시 FreeCAD 3D 모델 작성 (v2 ~ v5) |
| 사용 도구 | Ubuntu apt/dpkg, FreeCAD 1.1.4, Claude Code |

## 1. 요약
- 개발 PC의 apt 설치·업그레이드가 전부 막힌 문제를 진단함. 원인은 패키지 1개의 파일 충돌이었고, 그 패키지 하나를 지워 복구함 (OS 재설치 불필요).
- 재부팅 후 점검까지 마치고, 같은 문제가 다시 생기지 않도록 apt 핀을 걸어 둠.
- FreeCAD로 TeamRobot 섀시 3D 모델을 처음 만들기 시작함. 모터 장착 방식을 비교해 정하고 v5까지 진행함.

## 2. 상세 내용

### 2.1 개발 PC 진단 (읽기 전용)
- 증상: dpkg 미설정 패키지 27개 + 트리거 대기 7개로 apt 설치·업그레이드가 모두 막힘. 자동 보안 업데이트도 10/14 이후 멈춤.
- 원인: NVIDIA 저장소의 `python3-rich`가 `/usr/bin/markdown-it` 파일 충돌을 일으켜 `apt --fix-broken`이 3회 실패함.
- 정상 동작 확인: 부팅·systemd, GPU 드라이버 595.91.07, Docker 컨테이너 GPU, ROS 2 노드 실행.
- 덤으로 VS Code의 `code` 명령이 사라진 원인도 확인함. 업그레이드가 설정 단계 전에 멈춰 링크만 지워진 상태였음.
- 공유용 진단 문서를 정리하고, 복구 방법을 바꾼 새 문서를 따로 만듦 (기존 문서는 유지).

### 2.2 복구
- 방법: 문제 패키지 `python3-rich` 하나만 제거. 시뮬레이션으로 "제거 1개 + 멈춰 있던 26개 자동 설정"을 먼저 확인한 뒤 실행함.
- 결과 (재부팅 전): dpkg·apt 오류 0, `which code` 정상, `netplan status` 정상, 실패 서비스 0, 컨테이너 GPU(RTX 5060), ROS 2 talker 정상.
- 작업 기록 `~/system-recovery-2026-10-15.md` 작성 (원인, 한 일, 재부팅 후 점검 명령, 성공 기준).
- 재부팅 후 점검: `sudo dpkg --audit`, `sudo apt-get check` 모두 정상 → 복구 완료.

### 2.3 재발 방지
- `rich`는 9/14 우분투 설치 때 딸려 들어온 부가 패키지로, 수업에서는 쓰지 않음.
- 다른 패키지를 설치할 때 NVIDIA판 rich가 다시 끌려오는 것을 막기 위해 apt 핀을 적용함 (`/etc/apt/preferences.d/90-no-isaac-rich.pref`).
- 확인: rich 설치 시 우분투판 13.7.1이 선택되고, `apt upgrade` 시뮬레이션에 rich 관련 패키지가 없음.

### 2.4 TeamRobot 섀시 3D 모델 (FreeCAD)
- FreeCAD로 모델 제작이 가능한지 확인함. 1.1 형식 파일이라 1.1.4 AppImage를 사용함 (`/usr/bin/freecad` 0.21은 사용 불가).
- STEP 분석: 받아 둔 다이나믹셀 파일이 XM430이 아니라 방수형 **XW430**임을 발견함. Jetson Orin Nano는 개발 키트 전체 STEP.
- 버전별 진행:

| 버전 | 내용 |
|---|---|
| v2 | 모터 장착 후보 A(눕힘)·B(세움) 비교 모델, Jetson 배치 |
| v3 | 후보 B 채택, 모터 상하 반전, Ø65 일반 바퀴 4개, Jetson 하부 프레임째 고정. 전체 폭 296, 축간 200, 지상고 16.25 |
| v4 | 개조형 모터(뒤편 평면) 반영. 밑판 모터 나사홀 M2.5 16개, 기둥판 2장 + 나사홀 장당 8개, Jetson 가이드 블록(L자) 4개 |
| v5 | 기둥판–밑판 L브라켓 6개와 나사홀 추가 |

- 모든 버전에서 부품 간 간섭 0, 나사홀 정렬 편차 0을 확인함.
- 작업 정리 문서 `TeamRobot/docs/WORKLOG_2026-10-15.md` 작성 (결정 사항, 좌표, 나사홀 표, 미결 사항).
- 조립 과정을 보여 주는 HTML 시뮬레이션 페이지 초안 작성 (`TeamRobot/web/index.html`). 작업 종료로 확인은 다음으로 미룸.

## 3. 문제와 해결
- FreeCAD 계산 중 메모리 폭증·강제 종료 → 거리 계산을 솔리드 단위로 줄이고 메모리 상한을 조정해 해결.

## 4. 결과물

| 파일 | 내용 |
|---|---|
| `~/system-recovery-2026-10-15.md` | 시스템 복구 기록과 재부팅 후 점검 절차 |
| `/etc/apt/preferences.d/90-no-isaac-rich.pref` | rich 충돌 재발 방지 핀 |
| `TeamRobot/Assembly/TeamRobot_Base_v2 ~ v5_Assembly.FCStd` | 4륜 섀시 조립 모델 (+ 생성 스크립트·로그) |
| `TeamRobot/docs/WORKLOG_2026-10-15.md` | 섀시 작업 정리 |
| `TeamRobot/web/index.html` | 조립 시뮬레이션 HTML 초안 |

## 5. 다음 할 일
- [ ] NVIDIA 드라이버 보안 업데이트 (595.91 → 595.99) 계획.
- [ ] 원격 사본이 없는 데이터 백업.
- [ ] 섀시: L브라켓 규격, 너트/탭 체결 방식, 모터–밑판 나사 길이, 가이드 블록 고정 방식 결정.


# 개인 업무일지 - 2026-10-19 (월)

| 항목 | 내용 |
|---|---|
| 작업 시간 | 09:37 ~ 16:47 (Isaac Sim·Isaac Lab 환경), 12:29 ~ 18:33 (6WD 섀시 설계, 병행) |
| 주요 업무 | ① 수업용 Isaac Sim / Isaac ROS 환경 점검, Isaac Lab 설치와 Cartpole 학습 시험 ② 6WD 섀시를 PLA 3D 프린팅 기준으로 다시 설계하고 팔(RM-X52)까지 장착 |
| 사용 도구 | Isaac Sim 6.1, Isaac Lab v3.0.0-EA, ROS 2 Lyrical, FreeCAD 1.1.4, Claude Code |

## 1. 요약
- 개발 PC의 Isaac Sim·Isaac ROS 설치 상태를 가이드 기준으로 점검함. VRAM 8 GB가 최소 기준(16 GB)에 못 미치는 것 외에는 준비됨.
- Isaac Sim–ROS 브리지가 Lyrical 환경에서 CameraInfo 값을 틀리게 내는 문제를 찾음. 내장 Jazzy 환경에서는 정상임.
- velog 수업 가이드대로 Isaac Lab을 설치하고, Cartpole 무작위 행동 → 학습 → 정책 재생을 모두 실행함.
- 6WD 섀시를 PLA 출력(프린터 256 x 256 x 256) 기준으로 바꾸고, 윗판·버팀벽·프로파일 프레임·D435·RM-X52 매니퓰레이터까지 반영함.

## 2. Isaac Sim / Isaac ROS / Isaac Lab

### 2.1 설치 상태 점검
- 장비: Lenovo Legion Pro 5 (RTX 5060 Laptop 8 GB, RAM 32 GB), Ubuntu 24.04.5, 드라이버 595.91.07.
- 준비된 것: ROS 2 Lyrical(ros-base), Isaac Sim 6.1.0 (pip venv), PyTorch GPU, Docker + NVIDIA Container Toolkit, Isaac ROS CLI.
- 기준 미달: VRAM 8 GB < 16 GB, Compatibility Checker FAILED (VRAM 원인). 헤드리스 개발로 보완하기로 함.

### 2.2 Isaac Sim–ROS 브리지 검증
- 내장 Jazzy 환경으로 실행하면 정상: `/clock` 30 Hz, Image 640x480, CameraInfo K/R/P, 스테레오 baseline 0.1 m, TF, JointState 모두 값 확인.
- Lyrical 환경에서 실행하면 CameraInfo의 K/R/P 값이 한 칸씩 밀림 → 배포판 간 메시지 구조(ABI) 차이. **사용 금지**로 정리함.
- 원인 조사: Isaac Sim 6.1은 humble·jazzy 백엔드만 들어 있고, Lyrical에서는 Jazzy 백엔드로 대체됨. Lyrical 전용 백엔드를 직접 빌드하는 방법을 조사함 (Isaac Sim 소스, GCC 11 필요). 실행은 보류.

### 2.3 개정 설치 가이드 분석 (시스템 변경 없음)
- 새로 할 일은 Isaac Lab 설치 하나뿐임을 확인함.
- 가이드의 `ros-lyrical-desktop`은 Buildfarm 의존성 문제(OpenCV 4.10, PCL 1.15, PySide6)로 이 PC에 설치되지 않음 → ros-base 사용.

### 2.4 Isaac Lab 설치와 Cartpole 시험
- 설치: `~/pa-course/IsaacLab-6.1`, 태그 `v3.0.0-EA` (고정 커밋 `ae37b028` 일치), uv 0.13.1, `uv sync --frozen --extra isaacsim`.
- 의존성: Isaac Lab lock 때문에 버전 불일치 6건, numba import 실패. Cartpole 경로에서는 쓰이지 않음을 확인함.
- EULA는 직접 동의함 (16:30).
- Cartpole (환경 4개):

| 단계 | 결과 |
|---|---|
| 무작위 행동 | 정상 실행 |
| PPO 학습 300회 | 35초, exit 0. 평균 에피소드 길이 61.5 / 300 → 환경 수가 적어 균형 학습은 실패 |
| 정책 재생 | 약 9분 실행 후 Ctrl+C로 종료, exit 0. GPU 최대 4.8 GB |

## 3. TeamRobot 6WD 섀시 설계

### 3.1 바꾼 내용 (순서대로)

| 순서 | 내용 |
|---|---|
| 1 | ROBOTIS 공식 XM430 STEP으로 교체 (측면 탭이 도면과 같음). 2020 프로파일 450 x 2, 무게중심 계산 |
| 2 | **PLA 3D 프린팅, 출력 크기 256³ 확정**. 하판 250 x 270이 베드에 안 들어가서 앞·뒤 2조각 + 주먹장 이음으로 분할. 출력물의 M3 나사 자리는 열압입 인서트(Ø4.0)로. 출력 크기 검사와 STL 내보내기 자동화 |
| 3 | 가로 2020 프로파일 + 코너 브래킷 + RealSense D435 2대(앞·뒤). 카메라 브래킷은 팀원 제작 |
| 4 | 3D 프린팅이 아닌 체결 부품을 수치까지 정리 (BOM 입력용) |
| 5 | 프로파일 고정: 별도 클립 → **하판과 한 몸인 칼라 + M5 하나** (프로파일 끝 탭) |
| 6 | **윗판 추가**: 하판과 같은 두께·크기·주먹장, 윗판 위에도 프로파일 칼라 |
| 7 | 벽 보강: 별도 리브 브래킷 → **벽과 한 몸인 버팀벽 3개** (아래 발 → 하판, 위 발 → 윗판) |
| 8 | **전체 최적화**: 배터리 크래들·상단 OpenCR 기둥을 하판과 한 몸으로, 윗판 모터 접근 구멍 삭제. 출력 부품 13 → 11, 인서트 50 → 42, 구매 체결 부품 154 → 134. 틈 값 확인용 공차 시험편 3종 작성 (10-20에 쓰지 않기로 하고 삭제) |
| 9 | **RM-X52 매니퓰레이터 장착**: 받은 3MF 브라켓을 분석(구멍 패턴 불일치, 판 휨, 창 여유 부족 등)하고, 윗판 앞 조각과 한 몸인 U자 홀더로 다시 설계. M2.5x6 10개, 팔은 앞 방향. 요축 회전 ±142° (그 너머는 프로파일과 간섭) |
| 10 | 하판·윗판 주먹장 4개 → **3개 (X 0, ±65)**. 가운데 자리의 배터리 크래들 벽 일부를 끊음 |

### 3.2 검사 결과 (마지막 빌드)
- 실제 부품 165개 사이 간섭 0건, 나사 물림 84건 모두 설계 길이와 일치, 독립 검사 46/46 통과.
- 출력 부품 모두 256 x 256 x 256 안에 들어감 (최소 여유 6 mm).
- 팔 자세별 전복각 계산: 팔을 앞으로 뻗고 무거운 짐을 들거나 뒤로 뻗으면 넘어지기 쉬움 → 주행 중에는 팔을 접는 것으로 정리함.

### 3.3 결과물
| 파일 | 내용 |
|---|---|
| `TeamRobot/6WD_Chassis/TeamRobot_6WD_Chassis.FCStd`, `.step` | 조립 모델 |
| `TeamRobot/6WD_Chassis/STL/` | 출력용 STL (권장 출력 자세) |
| `TeamRobot/6WD_Chassis/README.md`, `design_review.md` | 설계·검증 문서 |
| `TeamRobot/6WD_Chassis/archive_2026-10-19_v1 ~ v7/` | 단계별 이전 판 보관 |
| `~/Desktop/TeamRobot_6WD_작업정리_2026-10-19.md` | 작업 정리 |

## 4. 다음 할 일
- [ ] Cartpole을 환경 16개로 다시 학습.
- [ ] Isaac Sim–Lyrical 연결 방식(내장 Jazzy 사용 / 전용 백엔드 빌드)을 강사님과 결정.
- [ ] 섀시: 구매 부품 BOM 정리, 팀원 D435 브래킷 반영, 바퀴·인서트 규격·배선 결정.