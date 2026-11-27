> 

수동으로 조종하는 것과 VLA 모델을 사용하는것의 차이가 무엇일까?
ros에 action 을 보내는건 똑같은데 다른게 있을까?
다른게 없다면 이유가 무엇일까?

-> 액션을 만드는 수단일뿐, 특별한 내용이 없기에 수동으로 조종하는것과는 차이가 없다
......?

피드백이 필요한 이유는 모델이 추론한 결과와 제어기에서 나온 결과가 차이가 있을수도 있다
엑션 내부에서 어떤 행동을 하는지 까지는 알필요없다. 시간이 더 오래걸릴 뿐이다. 

?

벡터화 하는 이유는 '행렬 계산' 을 위해서


VLA 에서 추론한 내용을 제어기에서 한번더 확인을 해야한다. 

# TIL 2026-11-27 (금) — Claude Code 세션 정리

| 항목 | 내용 |
|---|---|
| 기준 | 이 PC의 Claude Code 세션 기록 (`~/.claude/projects/*/*.jsonl`, 시각은 KST). VS Code 확장으로 실행한 세션 3개와 터미널(CLI) 세션 3개를 모두 포함 |
| 작업 시간 | 09:33 ~ 20:53. 14:34 ~ 18:04 에는 Claude 사용 기록이 없음 |
| 주요 디렉토리 | `~/GIT/waffle-mpx-lyrical` (실습 저장소, 작업 공간은 `~/waffle_mpx`), `~/GIT/waffle_rmx52_261127` (새 로봇 모델) |
| 주요 업무 | ① 와플 + OpenMANIPULATOR-X + D435 실습 세팅·텔레옵 점검 ② RM-X52 팔 · LDS-03 라이다 로봇 모델 새로 만들기 ③ OpenCR 부저 · 토크 · 접힘↔준비 자세 ④ 실물 텔레옵 (Wi-Fi DDS, 바퀴 방향) ⑤ 13강 LLM 자연어 명령 (실물 전진·접근, Isaac 블록 집기) |
| 사용 도구 | ROS 2 Lyrical · ros2_control · MoveIt, Gazebo Sim, Isaac Sim, RViz, OpenCR (arduino-cli, Arduino IDE), DYNAMIXEL Wizard, Ollama (qwen2.5:1.5b) |
| 참고 | git (커밋 · push) 은 내가 직접 함. 11:08 부터 Claude 에게 "깃 작업 절대 금지" |

---

## 1. 한눈에 보기: 시간대 × 디렉토리

| # | 시간 (KST) | 디렉토리 | 실행 | 세션 | 한 일 |
|---|---|---|---|---|---|
| 1 | 09:33 ~ 14:34 | `~/GIT/waffle-mpx-lyrical` | VS Code | `1a26b0a5` | 실습 세팅 · 텔레옵 점검 → 새 모델 검증 → 토크 원인 · 끄기 → 부저 펌웨어 → 접힌 자세 ↔ 준비 자세 → PC 실물 시험 → Pi 반영 · `.bashrc` |
| 2 | 10:33 ~ 12:18 | `~` 에서 시작 → `~/Desktop/waffle_rmx52_261127` → `~/GIT/waffle_rmx52_261127` → `~/GIT/waffle-mpx-lyrical` | CLI | `69619228` | RM-X52 CAD · URDF 찾기 → 새 로봇 모델 제작 (Gazebo · RViz · Isaac) → 상대 경로로 바꿈 → 팀 저장소 작업 트리에 반영 |
| 3 | 11:12 ~ 11:14 | `~/GIT/waffle_rmx52_261127` | VS Code | `8f7fb593` | push 가 꼬인 원인 분석 (읽기만) |
| 4 | 18:04 ~ 20:46 | `~/GIT/waffle-mpx-lyrical` | VS Code | `dda9e729` | 실물 텔레옵 · Pi 동기화 → Wi-Fi 에서 `/scan` 안 옴 → 바퀴 방향 보정 → 13강 자연어 명령 (실물 · Isaac) |
| 5 | 20:25 ~ 20:29 | `~/GIT/waffle-mpx-lyrical` | CLI | `d5a0096e` | PC 에서 로봇 노드가 안 보임 → 도메인 번호 |
| 6 | 20:53 ~ | `~` | CLI | `299c3246` | 이 TIL 작성 |

**흐름**

```
09:33 ─ 세션1 점검 보고 (09:50)
10:33 ─ 세션2 RM-X52 모델 제작 ──────────┐
11:12 ─ 세션3 git 분석                    │ (세션1 대기)
11:23 ─ 세션2 팀 저장소에 모델 반영 ──────┘
11:24 ─ 세션1 새 모델 검증 → 토크 → 부저 → 접힘/준비 자세 → 실물 시험 → Pi 반영
12:55 ─ 점심
14:22 ─ 세션1 배터리로 켠 뒤 토크 질문 → 토크 끄는 스크립트 (14:34)
        (14:34 ~ 18:04 Claude 사용 없음)
18:04 ─ 세션4 실물 텔레옵 → Wi-Fi DDS → 바퀴 방향 → 자연어 명령 (실물)
20:25 ─ 세션5 (CLI, 병행) 노드 안 보임
20:33 ─ 세션4 Isaac 블록 집기 성공 (20:41) → 실물 퍽 잡기 질문 (20:45)
20:53 ─ 세션6 TIL
```

---

## 2. 세션별 내용

### 2-1. 09:33 ~ 14:34 · `~/GIT/waffle-mpx-lyrical` (VS Code)

#### 실습 세팅 · 텔레옵 점검 (09:34 ~ 09:50)

- 요청: TurtleBot3 Waffle Pi + OpenMANIPULATOR-X + 앞쪽 D435 실습. Pi 세팅과 OpenCR 연결은 끝났으니, 사전 세팅과 텔레옵이 제대로 됐는지 분석하고 고칠 것을 보여 달라.
- 방법: Pi (`windforce08-rbp4.local`) 에 SSH 로 읽기만 함, `~/.ros/log` 실행 로그 분석. 센서는 모터 없이 따로 띄워 측정 (도메인 77), PC 에서는 mock 텔레옵에 실제 키 입력 (도메인 78). 모터는 켜지 않음.
- 정상: Pi 4B · Ubuntu 26.04.1 · ROS 2 Lyrical, `dialout` · `video` · `plugdev` 그룹, OpenCR `/dev/ttyACM0` · LDS-03 `/dev/ttyUSB0` · D435 USB 3.2, 빌드 (Pi 7 개 · PC 8 개, Pi 의 Cartographer 는 실패하지만 안 씀), `/scan` 10 Hz, 카메라 30 Hz, 두 기기 시계 차이 약 42 ms.
- 고칠 것 세 가지:

| # | 증상 | 원인 | 처리 |
|---|---|---|---|
| ① | 그리퍼 `Command out of limits` 1 초마다 | 닫힌 그리퍼가 −0.0138 m 로 URDF 하한 −0.010 보다 더 닫힘. 켤 때 현재 위치를 그대로 첫 명령으로 넣음 | 12:42 첫 명령을 범위 안으로 자름 → 해결 |
| ② | Overrun: 50 Hz 설정인데 실제 약 19 Hz | `write()` 가 주기마다 OpenCR 와 왕복 6 번 (한 번에 7 ~ 8 ms) | 미해결 |
| ③ | (커밋 전 텔레옵) MoveIt 등이 움직인 관절이 텔레옵의 옛 목표로 되돌아감 | 텔레옵이 스스로 기억한 `commanded` 기준 | 수정 제안만 (컨트롤러 `reference.positions` 기준, `rclpy.spin` 스레드) |

- 그 밖: 도메인은 README 42, 실제 31 → 두 기기 `.bashrc` 에 넣기 권장. PC 에서 카메라 `hz` 를 재면 Wi-Fi 로 약 220 Mbps 를 끌어옴. D435 `MIPI error` 는 반복되면 케이블 · 전원 의심.

#### 새 모델 검증 (11:24 ~ 11:47) — 세션 2 에서 만든 모델

- URDF 펼치기 (실기 · mock · Isaac) · `check_urdf` 통과, 메시 닫힘 · 단위 정상, 관절 위치 · 질량은 예전과 같음.
- MoveIt: 기본 자세 4 개 충돌 없음, 무작위 1500 자세 중 충돌 판정 옛 486 · 새 476.
- Isaac teacher 집기 · 놓기: 옛 8/8 · 새 8/8. 그리퍼 개폐 정상.
- **문제:** 새 손가락 충돌 메시 (`collision/gripper_left|right.stl`) 에 반대쪽까지 뻗은 가는 막대가 들어 있음. Isaac 은 링크마다 볼록 껍질 하나로 감싸서 두 손가락 사이가 쐐기로 메워짐 (완전히 열림 간격 56 → 32 mm, 닫힘 겹침 1.8 → 20 mm). 지금은 자기 충돌이 꺼져 있고 평가 때 고무 패드를 붙여서 괜찮지만, 손가락으로 직접 잡는 실습에서는 문제. → `make_rmx52_meshes.py` 에서 충돌 메시에서만 막대 빼기 권장.
- color 정책 평가는 Isaac Lab 환경에 `num2words` 가 없어 실패 (저녁 세션 4 에서 해결).

#### 토크 (11:30 ~ 12:27)

- 11:30 "로봇에 토크가 계속 들어가 있는데 문제가 뭐야" → 고장 아님. **OpenCR 펌웨어가 부팅할 때 바퀴 · 팔 토크를 스스로 켬** (`turtlebot3.cpp` 532 · 548 행). 플러그인은 launch 를 Ctrl+C 로 정상 종료할 때만 끔. 하트비트 타임아웃은 바퀴만 멈추고 토크는 안 끔.
- 11:47 · 12:27 "팔 잡고 있으니 토크 꺼줘" → 끄고 다시 읽어 확인 (`torque_joints=0`). 접힌 자세 joint2 −119.5°, joint3 +86.5° 는 당시 범위 (−102° ~, ~ +79°) 밖이었음.

#### 부저 소리 바꾸기 (12:08 ~ 12:26)

- 요청: 켤 때 음이 올라가는 짧은 '삐빅', 끌 때 내려가는 '삐빅'.
- 부저는 Pi 코드가 아니라 **OpenCR 펌웨어 안** → Arduino OpenCR 보드 패키지의 `~/.arduino15/packages/OpenCR/hardware/OpenCR/1.5.3/libraries/turtlebot3_ros2/src/turtlebot3/turtlebot3_sensor.cpp` 수정 (원본 `.orig` 백업).
- 솔 392 Hz 71 ms → 도 523 Hz 90 ms, 약 0.2 초 (예전 8 음 약 2.6 초). 부팅음도 같이 바뀜. arduino-cli 1.5.1 로 빌드 (138,572 바이트).
- 12:22 Arduino IDE AppImage 가 `SUID sandbox helper ... not configured correctly` 로 죽음 → Ubuntu 보안 설정 문제. `--no-sandbox` 를 붙이거나 arduino-cli 로 바로 업로드.
- 12:26 내가 업로드 완료 → 모델 0x5000, 펌웨어 버전 5 그대로.
- 주의: 보드 패키지를 다시 설치하거나 업데이트하면 이 수정은 사라짐.

#### 접힌 자세에서 시작 → 준비 자세 (12:34 ~ 12:48)

- 요청: 지금 접힌 자세를 초기 자세로, bringup 하면 준비 자세로.
- 고른 것: 준비 자세 = MoveIt `home` (0, −1.0, 0.7, 0.3), Ctrl+C 때 준비 자세를 거쳐 접힌 자세로 간 뒤 토크 끔, 실물 (`mode:=hardware`) 에서만.
- 바꾼 것:
  - 하드웨어 플러그인: `arm_ready_positions` · `arm_rest_positions` 파라미터, 50 ms 간격으로 관절 목표를 조금씩 보냄 (평균 0.6 rad/s), 이동 중 하트비트 유지, 첫 명령 범위 자르기 (①).
  - 관절 범위: joint2 하한 −102.6° → −122.4°, joint3 상한 +79.2° → +90°. 접힌 자세 값은 (0, −2.05, 1.50, 0.62).
  - SRDF: 범위를 넓혀 위팔이 몸체에 닿을 수 있으므로 몸체–위팔 충돌 검사 다시 켬.
  - `robot.launch.py`: 접는 동안 강제 종료되지 않게 종료 대기 20 초. README 에 동작 설명.
- 12:45 PC 에서 실물 시험 성공: 접힘 → 2.1 초 만에 `home` (목표와 1.4° 안쪽) → 컨트롤러 5 개 active, `out of limits` 0 회 → Ctrl+C → 2.1 초 만에 접힘 → 토크 꺼짐. Overrun 은 20 초에 32 회로 그대로.

#### Pi 반영 · 마무리 (12:49 ~ 14:34)

- 12:49 Pi 에 rsync (hardware · description · moveit_config · bringup) → Pi 빌드 4 패키지 27 초, 설치 폴더의 옛 메시 깨진 링크 7 개 정리.
- 12:52 Pi 에서 `ros2: command not found` → `.bashrc` 에 ROS 환경이 없음. 12:53 Pi `~/.bashrc` 에 `source ~/waffle_mpx/src/tools/lyrical_env.bash; export ROS_DOMAIN_ID=31` 추가. 내가 직접 돌린 bringup 은 정상 (home 이동 · Ctrl+C 접힘).
- Pi 종료는 sudo 암호가 필요해서 Claude 가 못 함 → 내가 직접.
- 14:22 배터리로 다시 켰더니 '삐빅' 과 함께 토크가 걸리고 움직이지 않음 → 정상. 부팅 토크는 펌웨어 동작이고, `home` 이동은 bringup 때 플러그인이 함. (부팅 토크를 끄는 펌웨어 수정은 제안만)
- 14:34 "그냥 토크 끄는 명령어" → Pi `~/opencr_torque.py` 를 넣어 둠 (실행은 안 함).

  ```bash
  python3 ~/opencr_torque.py off        # Pi 에서. on 으로 다시 켬
  ssh windforce08@windforce08-rbp4.local python3 ~/opencr_torque.py off   # PC 에서
  ```

  bringup 실행 중에는 쓰지 말 것 (같은 포트).

### 2-2. 10:33 ~ 12:18 · `~` → `~/GIT/waffle_rmx52_261127` (CLI) — RM-X52 · LDS-03 모델

- 10:33 RM-X52 파일 찾기:
  - STEP `~/GIT/FreeCAD/TeamRobot/Assembly/rm-x52.stp` (10-19 받음, ROBOTIS CREO 원본 조립품)
  - 치수 도면 `~/Downloads/rm-x52.pdf`
  - URDF · xacro 3 개 `~/Downloads/open_manipulator_x*.urdf(.xacro)` (오늘 10:23 받음). 메시 STL 은 받지 않았음.
- 10:40 분석 (설치된 팔은 구형 모델, LDS-03 이 없음 → COIN 라이다로):
  - **관절 위치는 STEP = 지금 URDF** (J2 바닥에서 76.5 mm, 128/24, 124 mm, 손가락 81.7 mm, PDF 와도 일치). 다른 건 겉모양 메시뿐 (옛 메시 둥근 덮개 ↔ 실물 평평한 브래킷, 최대 약 10 mm).
  - 받은 새 xacro 는 joint1 높이가 0 (지금 0.017) 이라 쓰지 않음 → 그대로 쓰면 팔이 17 mm 내려앉음.
  - 라이다는 LDS-03 대신 검은 상자, 그것도 9.3 mm 높게 그려져 있었음 → LDS-03 = COIN-D4 이므로 예전에 만든 `lds03.stl` 로 바꿈.
- 10:48 · 10:51 바탕화면 새 폴더에 바로 시뮬레이션 가능한 모델 + 눈으로 확인:
  - STEP 을 링크별로 잘라 보기용 메시 + 단순화한 충돌 메시 생성 (link1 은 옛것과 정확히 일치).
  - `~/Desktop/waffle_rmx52_261127/` 에 만들고 RViz (관절 슬라이더) · Gazebo 창 띄움. Isaac 가져오기도 성공 (`waffle.usda` 41 MB).
- 11:00 ~ 11:02 공유하려면 절대 경로 (`/home/pa31/...`) 문제 → 상대 경로로. Claude 는 팀 저장소 새 브랜치 + PR 을 추천.
- 11:06 내가 폴더를 `~/GIT/waffle_rmx52_261127` 로 옮기고, 팀 GitHub 에 새 저장소 (`SpartaPA/waffle_rmx52_261127`) 로 따로 올리기로 함.
  - Isaac URDF 는 상대 경로, RViz/Gazebo URDF 는 `package://`, Gazebo 월드는 `model://` + `run_gazebo.sh` 가 `GZ_SIM_RESOURCE_PATH` 지정, `run_rviz.sh` 는 처음 실행 때 `tools/build_overlay.sh` 로 `install/` 자동 빌드.
  - `cad/` 에 STEP · PDF, `.gitignore` (build · install · log · isaac · .vscode), 옛 경로를 가리키던 `.vscode/settings.json` 삭제.
  - 복사본에서 시험: Gazebo `/scan` 400 점 · 실시간 비율 1.0 · 메시 오류 없음, RViz 정상, Isaac exit 0. 공유 파일 안 절대 경로 0 개, 약 40 MB.
- **git 관련 사실:** 11:08:41 Claude 가 이 폴더에서 `git init -b main` + `git add -A` 를 실행함. 같은 시각 (11:08) 보낸 "아니다 깃 작업은 내가 할게", "깃 작업 절대 금지" 를 읽기 직전이었음. 그 뒤로 git 명령은 없고, 금지 규칙을 메모리에 저장함.
- 11:20 "다 했고, `~/GIT/waffle-mpx-lyrical` 작업 공간의 모델을 오늘 모델로 바꾸고 마무리" (git 없이 파일만):

| 구분 | 파일 (`turtlebot3_manipulation_description/` 안) |
|---|---|
| 추가 | `meshes/rm_x52/` (보기용 7 + `collision/` 7 + `meshes_info.json`), `meshes/lds03/` |
| 삭제 | `meshes/open_manipulator_x/` (옛 메시 7 개, 다른 곳에서 안 씀) |
| 수정 | `urdf/open_manipulator_x.urdf.xacro` (메시 출처 주석), `urdf/turtlebot3_waffle_pi.urdf.xacro` (LDS-03 메시), `launch/model.launch.py` (Lyrical 실행 오류) |

  - `~/waffle_mpx` 에서 이 패키지만 다시 빌드, `simulation/waffle.urdf` · `waffle.usda` · `scene.usda` 를 새 모델로 다시 만듦.
  - 시험: mock + MoveIt 컨트롤러 4 개 active, 자세별 충돌 검사, cuMotion `prepare_planner.py` 정상 (라이다 충돌 모양이 원기둥이 되어 충돌 구 약 80 → 152 개), RViz 확인.
  - LDS-03 실제 장착 위치는 아직 재지 않음 (저장소 값 그대로).

### 2-3. 11:12 ~ 11:14 · `~/GIT/waffle_rmx52_261127` (VS Code) — push 꼬임 분석

- 요청: SpartaPA 저장소로 push 하려는데 꼬였다. git 은 직접 하지 말고 상태만 분석하고 할 일을 알려 달라.
- 원인: **`/home/pa31/GIT` 자체가 git 저장소 (개인 백업 PA-Backup)**. 폴더에 `.git` 이 없을 때 친 git 명령이 오류 없이 상위 저장소에 적용됨.

| 시각 | PA-Backup reflog | 추정 명령 |
|---|---|---|
| 11:09:54 | 로컬 브랜치 `master` → `main` | `git branch -M main` |
| 11:09:58 | 원격에 `main` 새로 생김 | `git push -u origin main` |
| 11:11 | `waffle_rmx52_261127/.git` 생성 | `git init` |

  - 이 두 명령은 Claude 세션 기록에는 없음. 분석 당시 `waffle_rmx52_261127` 은 `master` · 커밋 0 · 스테이징 0 이었으므로, 11:08:41 Claude 가 만든 `.git` 은 그 사이 다시 만들어진 것으로 보임.
  - 데이터 손실 · 잘못된 커밋은 없음. 원격에 `master` 와 `main` 이 같은 커밋 (`9e20943`) 으로 둘 다 있음.
- 안내받은 되돌리기 (실행 여부는 기록에 없음):

  ```bash
  cd /home/pa31/GIT
  git branch -m main master
  git branch -u origin/master master
  git push origin --delete main
  ```

### 2-4. 18:04 ~ 20:46 · `~/GIT/waffle-mpx-lyrical` (VS Code) — 실물 텔레옵 · 13강 자연어 명령

#### 실물 텔레옵 준비 (18:04 ~ 18:47)

- 터미널 2 개 (+ 상태 확인 1 개): Pi 에서 `robot.launch.py mode:=hardware`, PC 에서 `ros2 run turtlebot3_manipulation_bringup teleop`. 둘 다 `ROS_DOMAIN_ID=31`.
- 18:44 Pi 에 변경 옮기고 빌드 (커밋 없이): 하드웨어 · 모델은 12:50 에 이미 들어가 있었고, 다른 파일은 5 개뿐 (`README.md`, `lessons/13-react/` 3 개, `sim/ros_io.py`) → 덮어씀. 빌드 7 패키지 6 초, 새 코드 · 두 자세 값 · 새 메시가 들어간 것 확인.

#### 13강 LLM 자연어 명령 (18:54 ~ 19:06)

- PC: Ollama `qwen2.5:1.5b` 해석 점검 3 문장 통과. 촬영 정책에 필요한 `num2words` 는 Isaac Lab 환경을 건드리지 않고 `~/waffle_mpx/.learning-deps` 에만 설치.
- 실물에서 되는 것: 전진 (≤ 0.15 m), 거리까지 접근 (0.2 ~ 1.5 m, 라이다 정면 ±10°), 조건부 촬영 (SmolVLM). 블록 집기는 Isaac 전용.
- 18:58 "`/scan` 이 발행되지 않아서 대기 중" (19:01 "도메인 아이디 때문인가") → **도메인 문제 아님. Wi-Fi 에서 DDS 멀티캐스트 탐색이 유실됨.** Pi 에서는 10 Hz 로 나가고 PC 에서 토픽 이름은 보이지만 데이터가 안 옴. `ROS_STATIC_PEERS` 로 상대 주소를 지정하니 3 번 모두 약 10 Hz (없으면 3 번 모두 0).
- 카메라 원본 (640×480, 초당 약 27 MB) 은 주소를 지정해도 12 초 동안 한 프레임도 안 옴 → **촬영 명령은 유선 LAN 이나 압축 영상이 필요.**
- 19:17 압축 영상 수정 요청 → 바로 취소. 19:35 "처음부터 다 끄고 다시" → PC · Pi ROS 프로세스 모두 정리, 양쪽에 `ROS_STATIC_PEERS` 를 넣는 순서로 다시 안내.

#### 바퀴 방향 (19:38 ~ 20:18)

- 19:38 전진 · 후진이 반대 (19:40 "모터를 반대로 설치했나").
- 19:44 DYNAMIXEL Wizard 로 바퀴 ID 를 서로 바꾸기로 함 → 순서 안내: ModemManager 끄기 → OpenCR 에 `usb_to_dxl` 올리기 → Wizard 1 Mbps 스캔 → 임시 ID 3 을 거쳐 1 ↔ 2 교환 → `turtlebot3_manipulation` 펌웨어 복구.
- 19:49 Arduino IDE 샌드박스 오류 다시 → `--no-sandbox`.
- 20:04 바꿨는데 여전히 W 가 후진.
- 20:07 "임시로 소프트웨어에서" → 처음엔 `wheels_swapped` (좌우 교환 + 부호 반전).
- 20:15 이번엔 좌우 회전이 반대 → **ID 교환은 실제로 적용됐고, 모터에 저장된 Drive Mode 역방향 비트가 왼쪽 모터에 남아 두 바퀴가 모두 반대로 도는 상태.** → `wheels_reversed` 로 바꿈 (좌우 교환 없이 두 바퀴 명령 · 인코더 부호만 반전, 실물 모드만).
  - 바뀐 파일: `turtlebot3_manipulation_system.cpp` · `.hpp`, `turtlebot3_manipulation_system.ros2_control.xacro`. PC · Pi 빌드 통과.
  - 하드웨어로 바로잡으려면: ID 1 의 역방향 비트 끄고 ID 2 에 켬 → xacro 의 `wheels_reversed` 를 `false`.
- 20:18 방향 맞음.

#### 자연어 명령 실물 · 시뮬레이션 (20:18 ~ 20:46)

- 실물 실행 (PC, 터미널 2):

  ```bash
  source ~/waffle_mpx/src/tools/lyrical_env.bash
  export ROS_DOMAIN_ID=31
  export ROS_STATIC_PEERS=10.2.150.152          # Pi 주소 (DHCP, 바뀔 수 있음)
  export ISAAC_LAB_PYTHON=~/pa-course/IsaacLab-6.1/.venv/bin/python
  export WAFFLE_LEARNING_DEPS=~/waffle_mpx/.learning-deps
  cd ~/waffle_mpx/src/lessons/13-react
  python3 natural_command.py --hardware --output ~/waffle_mpx/real-$(date +%H%M%S)
  ```

  Pi 쪽은 `export ROS_STATIC_PEERS=10.2.150.165` (PC 주소) 를 넣고 `robot.launch.py`.
- 20:23 "앞에 있는 벽과의 거리가 50cm 가 될 때까지 후진해" → LLM 이 `drive 0.5 m` 로 해석 → 상한 0.15 m 초과로 거절, 로봇 안 움직임. **13강 실행기에는 후진이 없음** (접근은 "까지" + "다가/가까이/전진" 이 있어야 인정).
- 20:24 저장소 실습 순서 정리: 설치 → mock MoveIt → 실물 텔레옵 · 지도 · Nav2 → D435 마운트 → Isaac Sim → color 평가 → 학습 (VLA · 모방 · PPO) → Isaac ROS → 13강. 제출물은 13강 슬라이드 25 (실행 조건, 턴별 JSON 로그, `waffle.ppm`, 설명).
- 20:32 자연어로 팔 움직이기 → 실물은 안 됨 (팔 동작은 Isaac 블록 집기뿐).
- 20:33 Isaac 터미널 A: Isaac Sim 은 이 PC 에서 `~/pa-course/.venv-isaacsim`, 도메인 113 + `ROS_LOCALHOST_ONLY=1` 로 실물과 분리.
- 20:36 "블록이 아예 없어" → 정상. 터미널 A 장면 (`scene.py`) 은 촬영 · 전진용이고, 블록 · 작업대는 평가기가 별도 장면을 열 때 생김 (터미널 A 는 꺼야 GPU 메모리가 남음).
- 20:37 ~ 20:40 실패 세 번:
  1. `~/waffle_mpx` 에서 실행 + `--showow` 오타
  2. `evaluate_pick_place.py` 실패 → 장면 기본 경로가 이 PC 와 다름 → `export WAFFLE_SCENE=~/waffle_mpx/simulation/scene.usda`
  3. `FileExistsError` → 실행기는 출력 폴더를 덮어쓰지 않음 → 폴더 이름에 `$(date +%H%M%S)`
- **20:41 빨강 블록 성공** (`~/waffle_mpx/lesson13-red-204026`, 새 RM-X52 모델 장면): `selected` red, `max_lift_m` 0.0597, `wrong_pick` false, `stable_s` 2.22, `success` true (슬라이드 15: 59.3 mm, 2.20 초).
- 20:43 "제출할 필요 없어, 실물로 넘어가야 해" → 20:45 "실물에서 퍽을 잡게 하는 건 여기 없어?" → **이 저장소에는 퍽 · 실물 잡기 코드가 없음.** 퍽은 `~/GIT/lv2_EYE4` (D435 로 파란 퍽을 찾아 카메라로 따라가는 추적, 잡기 없음) 에만 나옴. 실물로 하려면 D435 색 · 깊이 → 3 차원 위치 → IK/MoveIt 집기 → LLM 이 호출하는 구조로 새로 만들어야 함 (퍽 지름 · 두께 · 색 필요).

### 2-5. 20:25 ~ 20:29 · `~/GIT/waffle-mpx-lyrical` (CLI) — 로봇 노드가 안 보임

- 원인: PC `~/.bashrc` 에 ROS 설정이 없어 새 터미널은 기본 **도메인 0** → `ros2 node list` 비어 있음. 도메인 31 에서는 로봇 노드 11 개가 다 보임.

  ```
  /arm_controller  /camera  /controller_manager  /diff_drive_controller
  /gripper_controller  /imu_broadcaster  /joint_state_broadcaster  /lidar_node
  /robot_state_publisher  /turtlebot3manipulationsystem  /waffle_keyboard
  ```

- 해결: `export ROS_DOMAIN_ID=31`. 노드는 보이는데 데이터가 안 오면 `ROS_STATIC_PEERS` 도. (PC `.bashrc` 추가는 제안만)

### 2-6. 20:53 ~ · `~` (CLI) — 이 TIL

- 오늘 세션 기록 6 개 (VS Code 3 · CLI 3) 를 모아 시간대 · 디렉토리별로 정리.

---

## 3. 오늘 배운 것

### ROS 2 네트워크

- **노드가 안 보이면 먼저 `ROS_DOMAIN_ID`.** 새 터미널은 기본 0 번이라 31 번 로봇이 안 보임.
- **토픽 이름은 보이는데 데이터가 0 이면 Wi-Fi 의 DDS 멀티캐스트 탐색 유실.** `ROS_STATIC_PEERS=<상대 IP>` 를 양쪽에 넣으면 해결. 이때 `ROS_LOCALHOST_ONLY=1` 은 넣으면 안 됨.
- 카메라 원본 영상 (640×480 약 27 MB/s) 은 Wi-Fi 로 못 넘김 → 유선 LAN, 압축 영상, 또는 Pi 에서 처리.

### ros2_control · OpenCR · DYNAMIXEL

- 하드웨어 플러그인이 켤 때 **현재 위치를 첫 명령으로 넣으면**, 위치가 한계 밖일 때 리미터가 매 주기 잘라 내며 오류를 냄 → 첫 명령을 범위 안으로 자르기.
- 제어 주기 overrun 의 원인은 스케줄링이 아니라 **USB 왕복 횟수** (주기당 6 번 × 7 ~ 8 ms).
- **OpenCR 펌웨어는 부팅하면 토크를 켬.** 플러그인은 정상 종료 때만 끔. 하트비트 타임아웃은 바퀴만 멈춤.
- 부저 멜로디는 OpenCR 보드 패키지 라이브러리 (`turtlebot3_sensor.cpp`) 안에 있어서 펌웨어를 다시 올려야 바뀜. 보드 패키지를 업데이트하면 사라짐.
- **Drive Mode 역방향 비트는 모터에 저장돼 ID 를 바꿔도 따라감.** 바퀴 ID 만 맞바꾸면 두 바퀴가 모두 반대로 돌 수 있음.
- 관절 범위를 넓히면 SRDF 에서 꺼 둔 충돌 검사를 다시 봐야 함.

### 모델 · 시뮬레이션

- 새로 받은 xacro 가 기준 메시와 다르면 관절 높이가 어긋날 수 있음 (joint1 z 0 vs 0.017). 관절 위치는 STEP 으로 확인.
- Isaac 은 충돌 메시를 링크마다 볼록 껍질 하나로 감쌈 → 가는 막대 하나가 손가락 사이를 메움. 충돌 메시는 볼록 부품만.
- 공유할 모델은 `package://` · `model://` · 상대 경로로, 그리고 다른 폴더에 복사해서 시험.

### 도구 · git

- Ubuntu 24.04 이후 Electron AppImage (Arduino IDE) 가 `SUID sandbox` 로 죽으면 `--no-sandbox`.
- 상위 폴더가 git 저장소인 곳 (`~/GIT` = PA-Backup) 에서는 **`git init` 을 먼저**, 명령 전에 `git rev-parse --show-toplevel` 확인.
- 13강 실행기: 실물은 전진 · 접근 · 촬영만 (후진 없음), 블록 집기는 Isaac 전용, 출력 폴더는 매번 새 이름, 이 PC 는 `WAFFLE_SCENE` · `ISAAC_*_PYTHON` 경로를 따로 줘야 함.

---

## 4. 생긴 문제와 해결

| 시각 | 문제 | 원인 | 해결 | 상태 |
|---|---|---|---|---|
| 09:50 | 그리퍼 `out of limits` 1 초마다 | 첫 명령이 한계 밖 | 첫 명령 범위 자르기 | ✓ (12:45 실물 0 회) |
| 09:50 | Overrun (실제 약 19 Hz) | `write()` USB 왕복 6 번 | — | 남음 |
| 11:09 | PA-Backup 브랜치 · 원격 `main` 생김 | `.git` 없는 하위 폴더에서 git 명령 | 되돌리기 명령 안내 | 실행 여부 모름 |
| 11:30 | 토크가 계속 들어감 | 펌웨어 부팅 동작 | 토크 끄기, `~/opencr_torque.py` | ✓ |
| 11:47 | 새 손가락 충돌 메시 쐐기 | 막대 부품 + 볼록 껍질 | 충돌 메시에서 막대 빼기 제안 | 남음 |
| 12:08 | 부저가 길고 큼 | 펌웨어 8 음 멜로디 | 2 음 '삐빅' 펌웨어 | ✓ |
| 12:22 · 19:49 | Arduino IDE 바로 죽음 | AppImage 샌드박스 | `--no-sandbox` / arduino-cli | ✓ |
| 12:34 | 접힌 자세에서 켜면 범위 밖 | 관절 한계 | 범위 넓힘 + 준비 · 접힘 이동 | ✓ |
| 12:52 | Pi `ros2: command not found` | `.bashrc` 에 환경 없음 | Pi `.bashrc` 추가 | ✓ |
| 18:58 | PC 에 `/scan` 안 옴 | Wi-Fi DDS 탐색 유실 | `ROS_STATIC_PEERS` | ✓ |
| 19:06 | 카메라 영상 안 옴 | Wi-Fi 대역폭 | 유선 또는 압축 | 남음 |
| 19:38 | 전진 · 후진 반대 → 회전도 반대 | 바퀴 Drive Mode 비트 | `wheels_reversed` (소프트웨어) | 임시 ✓ |
| 20:23 | "후진해" 거절 | 실행기에 후진 없음 | 접근 문장으로 / `retreat` 제안 | — |
| 20:25 | PC 에서 노드 안 보임 | 도메인 0 | `ROS_DOMAIN_ID=31` | ✓ |
| 20:38 | 블록 집기 실패 3 번 | 위치 · 오타 · 장면 경로 · 폴더 중복 | `WAFFLE_SCENE`, 시각 붙인 폴더 | ✓ (20:41 성공) |

---

## 5. 바뀐 것 · 결과물

| 위치 | 내용 |
|---|---|
| `~/GIT/waffle_rmx52_261127/` | RM-X52 + LDS-03 로봇 모델 (상대 경로, Gazebo · RViz · Isaac 시험 통과). push 는 내가 직접 |
| `~/GIT/waffle-mpx-lyrical/turtlebot3_manipulation_description/` | 새 메시 (`rm_x52`, `lds03`), 옛 메시 삭제, xacro, `model.launch.py`, 관절 범위, 두 자세 값, `wheels_reversed` |
| `~/GIT/waffle-mpx-lyrical/turtlebot3_manipulation_hardware/` | 준비 · 접힘 이동, 첫 명령 자르기, `wheels_reversed` |
| `~/GIT/waffle-mpx-lyrical/` 그 밖 | SRDF 충돌 검사, `robot.launch.py` 종료 대기 20 초, README |
| `~/waffle_mpx/simulation/` | 새 모델로 `waffle.urdf` · `waffle.usda` · `scene.usda` |
| `~/waffle_mpx/.learning-deps/` | `num2words` (지우면 원래대로) |
| `~/waffle_mpx/lesson13-red-204026/` | Isaac 빨강 블록 집기 성공 결과 |
| OpenCR 보드 패키지 `turtlebot3_sensor.cpp` (+ `.orig`) | 부저 '삐빅' (OpenCR 에 업로드됨) |
| Pi `~/.bashrc`, `~/opencr_torque.py`, `~/waffle_mpx` | 환경 자동 로드 · 도메인 31, 토크 끄기 스크립트, PC 와 같은 파일로 빌드 |

모든 저장소 변경은 커밋하지 않은 상태 (git 은 내가 직접).

---

## 6. 다음 할 일

- [ ] `~/GIT/waffle-mpx-lyrical` 변경 확인 후 커밋 · push (모델 · 하드웨어 플러그인 · 바퀴 보정 · SRDF · launch · README)
- [ ] `~/GIT` (PA-Backup) 브랜치를 `master` 로 되돌렸는지 확인
- [ ] 바퀴 모터 Drive Mode 를 하드웨어로 바로잡고 `wheels_reversed` 를 `false` 로
- [ ] Overrun 해결 (실물만 `update_rate` 20, 또는 `write()` 에서 바뀐 값만 보내기)
- [ ] 텔레옵 ③ (다른 도구가 움직인 관절 되돌아감) 수정 여부 결정
- [ ] 손가락 충돌 메시에서 막대 빼기 (`make_rmx52_meshes.py`)
- [ ] LDS-03 실제 장착 위치 재기
- [ ] 실물 촬영 명령: 유선 LAN 연결 또는 압축 영상
- [ ] 실물 퍽 잡기: 퍽 지름 · 두께 · 색 정하고, D435 위치 추정 → MoveIt 집기 → LLM 호출 구조 설계
- [ ] (선택) PC `~/.bashrc` 에 `ROS_DOMAIN_ID=31`, 부팅 토크 끄는 펌웨어, 후진 (`retreat`) 명령