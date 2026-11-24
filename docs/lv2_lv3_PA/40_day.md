> 작성일 : Oct.2.2026 

오늘의 학습 : 월드 점이 픽셀이 되기까지의 변환 사슬 
> 

희우님, 현재 조건을 기준으로 보면 **3일 안에 모든 문제를 동시에 완성하려고 하기보다, 문제 1→2→3→4→5의 의존관계를 끊지 않는 방향**으로 진행하는 게 핵심입니다.

현재 **RealSense + Dynamixel 2대가 구동 가능한 상태**이므로, 하드웨어 세팅 자체보다 **인지 → `/target` → 제어 → 상태/안전 → 기록/재현**을 먼저 연결하는 것이 좋습니다.

# 1. 전체 과제 구조

```text
                    ┌─────────────────┐
                    │ 문제 1. 인지     │
                    │ HSV + Contour   │
                    └────────┬────────┘
                             │
                         /target
                    PointStamped
                             │
                             ▼
                    ┌─────────────────┐
                    │ 문제 2. 인터페이스 │
                    │ ROS2 Topic/Node  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ 문제 3. 제어     │
                    │ P Control       │
                    │ Dynamixel × 2   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ 문제 4. 검증     │
                    │ 상태/정지/복구   │
                    │ 성능 측정        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ 문제 5. 재현/협업 │
                    │ rosbag / README │
                    └─────────────────┘
```

핵심은 **각 문제를 별개 과제로 보지 않는 것**입니다.

> **문제 1에서 만든 검출값이 문제 2의 `/target`이 되고 → 문제 3의 제어 입력이 되고 → 문제 4의 검증 대상이 되고 → 문제 5에서 bag으로 재현되어야 합니다.**

---

# 2. 문제별 목차 및 분석

## 문제 1 — HSV + Contour 기반 목표 검출

### 1.1 목표

RealSense 카메라 영상에서

```text
영상
 ↓
HSV 변환
 ↓
색상 Mask
 ↓
Noise 제거
 ↓
Contour
 ↓
목표 선택
 ↓
중심점 계산
```

까지 구현합니다.

최종적으로 필요한 값은 사실 많지 않습니다.

```text
target detected
target center x
target center y
target area
```

그리고 이것을 문제 2에서

```text
/target
geometry_msgs/msg/PointStamped
```

로 전달합니다.

---

### 1.2 인지 파트

인지 담당의 핵심 업무입니다.

- RealSense RGB 영상 입력
- HSV 변환
- HSV threshold 설정
- Mask 생성
- Morphology / Noise 제거
- Contour 검출
- 최소 면적 필터
- 후보 Contour 중 목표 선택
- 중심점 계산
- `ex`, `ey` 계산
- `area_ratio` 계산
- 검출 실패 시 `detected=false`

중요한 출력값:

```text
detected
ex
ey
area_ratio
```

---

### 1.3 제어 파트

인지가 보내는 값을 받아서 실제 제어에 사용할 수 있는지 확인합니다.

예:

```text
ex > 0
→ 목표가 오른쪽
→ 오른쪽 방향 보정

ex < 0
→ 목표가 왼쪽
→ 왼쪽 방향 보정

ex ≈ 0
→ 중앙
→ 회전 명령 없음
```

즉 문제 1부터 제어팀이 참여해야 합니다.

---

### 1.4 통합 파트

ROS2 노드 연결을 담당합니다.

```text
RealSense
   ↓
camera_node
   ↓
detection_node
   ↓
/target
```

그리고 다음 문제에서 이 `/target`을 그대로 사용할 수 있도록 해야 합니다.

---

### 1.5 검증 파트

다음 조건을 준비합니다.

| 조건 | 확인 |
|---|---|
| 목표 중앙 | `ex ≈ 0` |
| 목표 오른쪽 | `ex > 0` |
| 목표 왼쪽 | `ex < 0` |
| 목표 없음 | `detected=false` |
| 배경만 존재 | 오검출 여부 |
| 목표 일부 가림 | 검출 여부 |
| 조명 변화 | 검출 안정성 |

---

# 3. 문제 2 — ROS2 인터페이스 및 연결

이 문제는 **팀 프로젝트의 핵심 연결부**입니다.

## 3.1 권장 Node 구조

현재 RealSense가 Raspberry Pi에 장착되는 조건을 반영하면:

```text
┌─────────────────────────────┐
│        Raspberry Pi         │
│                             │
│  ┌───────────────┐          │
│  │ RealSense     │          │
│  │ Camera Node   │          │
│  └───────┬───────┘          │
│          │ image             │
│          ▼                   │
│  ┌───────────────┐           │
│  │ Detection     │           │
│  │ Node          │           │
│  └───────┬───────┘           │
│          │                   │
│       /target                │
│          │                   │
│          ▼                   │
│  ┌───────────────┐           │
│  │ Control Node  │           │
│  └───────┬───────┘           │
│          │                   │
│          │ motor command      │
│          ▼                   │
│  ┌───────────────┐           │
│  │ Dynamixel      │          │
│  │ Node           │          │
│  └───────┬───────┘           │
│          │                   │
│       DXL #1                 │
│       DXL #2                 │
└─────────────────────────────┘
```

여기에 상태와 기록을 추가합니다.

```text
Detection Node
      │
      ├── /target
      │
      ▼
Control Node
      │
      ├── /motor_command
      │
      ▼
Dynamixel Node
      │
      └── /motor_state

Control Node
      │
      └── /tracking_status
```

---

## 3.2 핵심 Topic

### `/target`

```text
geometry_msgs/msg/PointStamped
```

의미:

```text
point.x = ex
point.y = ey
point.z = area
```

주의할 점은 과제에서 명시했듯이 이것을 **일반적인 3차원 위치 좌표로 해석하지 않는 것**입니다.

---

### `/tracking_status`

예:

```text
IDLE
TRACKING
LOST
```

상태를 관리합니다.

---

### 모터 명령

팀에서 정한 인터페이스가 있다면 그것을 우선하고, 없다면 최소한 다음 정보를 명확히 해야 합니다.

```text
left/right
speed
direction
enable/stop
```

---

# 4. 문제 3 — 객체 중심 기반 추적 제어

여기가 **희우님이 제어 파트라면 가장 중요한 영역**입니다.

## 4.1 목표

목표 중심 오차:

```text
ex
```

를 이용해서 Dynamixel 2대를 제어합니다.

기본 P 제어:

```text
command = Kp × ex
```

그리고 제한:

```text
command = clamp(Kp × ex,
                -speed_limit,
                +speed_limit)
```

---

## 4.2 제어 파트 업무

### ① 방향 확인

먼저 모터를 낮은 속도로 돌려서 확인합니다.

```text
목표가 오른쪽
→ 실제로 어느 방향으로 회전해야 하는가?

목표가 왼쪽
→ 반대 방향인가?
```

여기서 부호를 결정합니다.

```text
direction = +1 또는 -1
```

---

### ② Deadband

중앙 근처에서 모터가 계속 떨리는 것을 방지합니다.

예:

```text
if abs(ex) < deadband:
    command = 0
```

---

### ③ 속도 제한

```text
command = clamp(command, -speed_limit, speed_limit)
```

---

### ④ P Gain 실험

예를 들어:

```text
Kp = 0.5
Kp = 1.0
Kp = 2.0
```

처럼 단계적으로 증가시킵니다.

한 번에 높은 Kp를 넣으면:

```text
목표
 ↓
큰 오차
 ↓
큰 모터 명령
 ↓
과도한 회전
 ↓
목표를 지나침
 ↓
반대 방향
 ↓
진동
```

이 발생할 수 있습니다.

---

## 4.3 제어 검증 데이터

최소한 CSV를 다음처럼 남기는 것을 권장합니다.

```csv
time_s,ex,ey,detected,kp,command,state
0.00,0.32,0.01,1,1.0,0.32,TRACKING
0.10,0.25,0.01,1,1.0,0.25,TRACKING
0.20,0.12,0.01,1,1.0,0.12,TRACKING
...
```

그러면 나중에

```text
Kp별 오차 그래프
Kp별 진동 정도
Kp별 수렴 시간
```

을 비교할 수 있습니다.

---

# 5. 문제 4 — 성능 / 안전 / 목표 소실 복구

이 부분은 단순히 "잘 따라간다"를 보는 것이 아닙니다.

**망가졌을 때 안전하게 멈추는가**를 검증합니다.

## 5.1 상태 머신

최소:

```text
          목표 검출
IDLE ──────────────→ TRACKING
                       │
                       │ 목표 소실
                       ▼
                     LOST
                       │
                  3 frame 검출
                       │
                       ▼
                   TRACKING
```

그리고 시작/정지 시:

```text
IDLE
→ 모터 명령 없음

TRACKING
→ 제어 명령 발생

LOST
→ 반드시 정지
```

---

## 5.2 제어 파트

제어팀에서는 특히 다음을 책임져야 합니다.

### 정상

```text
/target 수신
→ command 생성
→ Dynamixel 출력
```

### 검출 실패

```text
/target detected=false
→ command = 0
```

### Timeout

```text
마지막 입력 이후 0.5초 이상
→ command = 0
```

### 통신 끊김

```text
Control Node 종료
→ Dynamixel 측에서도 안전 정지
```

여기가 중요합니다.

**ROS2 노드가 죽었다고 모터가 마지막 속도로 계속 움직이면 안 됩니다.**

---

# 6. 문제 4의 검증 항목

| 시험 | 조건 | 측정 |
|---|---|---|
| 정상 추적 | 30초 | FPS, 검출률, RMSE |
| 가림 | 약 2초 × 5회 | 정지/복귀 |
| 목표 소실 | 1회 이상 | timeout |
| 인지 중단 | 1회 이상 | 정지 |
| 제어 중단 | 1회 이상 | 모터 정지 |
| 중앙 목표 | `ex≈0` | 정지 안정성 |

특히 **실제 모터를 움직이는 검증은 마지막에 해야 합니다.**

순서는:

```text
Mock / 가짜 입력
↓
실제 /target
↓
모터 제한속도
↓
정상속도
↓
고장/소실 시험
```

이게 안전합니다.

---

# 7. 문제 5 — bag 재현 및 협업

문제 5는 마지막에 갑자기 시작하는 게 아니라 **오늘부터 로그를 남겨야 합니다.**

## 7.1 기록해야 하는 것

```text
영상
/target
/tracking_status
/motor command
/motor state
```

가능하면:

```text
parameter
Kp
speed_limit
HSV threshold
실행 시간
Git commit
```

까지 연결합니다.

---

## 7.2 재현 구조

```text
[실제 RealSense]
       ↓
    rosbag
       ↓
 ┌─────────────┐
 │ Offline     │
 │ Replay      │
 └──────┬──────┘
        ↓
     /target
        ↓
   Control Node
        ↓
   Motor OFF
```

중요한 것은 **bag 재생 시 실제 모터가 움직이지 않게 하는 것**입니다.

즉,

```text
Replay = 검출/제어 검증
Real Robot = 실제 동작 검증
```

으로 분리하는 것이 좋습니다.

---

# 8. 담당 파트별 전체 업무표

## 🧠 인지

```text
[문제 1]
RealSense
→ RGB
→ HSV
→ Mask
→ Contour
→ Target 선택
→ ex/ey/area
→ /target

[문제 2]
Detection ROS2 Node

[문제 4]
검출률
오검출
FPS
목표 소실

[문제 5]
rosbag 재생 가능한 입력 제공
```

---

# 🎮 제어

```text
[문제 2]
/target subscriber
/tracking_status

[문제 3]
방향 부호
P Controller
Kp
Deadband
Speed Limit
Dynamixel 2대 제어

[문제 4]
IDLE
TRACKING
LOST
Timeout
Emergency Stop
복구 조건

[문제 5]
제어 로그
명령 재현
실제 모터 OFF replay
```

---

# 🔗 통합

```text
[문제 1~2]
Node 연결
Topic 연결
QoS
Timestamp

[문제 3]
인지 → 제어 → Dynamixel 연결

[문제 4]
전체 시스템 State Machine
Timeout 경로
정지 경로

[문제 5]
rosbag
launch 파일
parameter
README
실행 환경 통일
```

---

# 📊 검증

```text
[문제 1]
검출 정확성

[문제 2]
Topic / Message 정상 전달

[문제 3]
Kp 비교
오차
진동
응답속도

[문제 4]
정상 추적
가림
소실
통신 중단
복구

[문제 5]
다른 팀원이 README만 보고 재현
```

---

# 9. 3일 작업 순서

## DAY 1 — 연결을 만든다

목표:

> **카메라 → 인지 → `/target` → 제어 → Dynamixel**

까지 한 번이라도 흐르게 만들기.

### 오전

```text
1. Git 브랜치/작업공간 확인
2. ROS2 패키지 구조 생성
3. RealSense Node 확인
4. Dynamixel 2대 연결 확인
5. ROS2 Topic 목록 확정
```

### 오후

```text
6. HSV Detection Node
7. /target Publisher
8. /target Subscriber
9. Mock target으로 제어 테스트
10. 실제 target으로 Dynamixel 저속 테스트
```

### DAY 1 종료 기준

```text
RealSense
   ↓
Detection
   ↓
/target
   ↓
Control
   ↓
Dynamixel
```

이게 **한 번이라도 성공**해야 합니다.

---

# DAY 2 — 제어와 안전을 완성한다

목표:

> **제어가 안정적으로 동작하고 잃어버리면 멈춘다.**

```text
1. 방향 부호 확정
2. Deadband
3. Speed Limit
4. Kp 실험
5. CSV logging
6. IDLE
7. TRACKING
8. LOST
9. Timeout
10. 복구 조건
```

그리고

```text
정상
→ 가림
→ LOST
→ 정지
→ 목표 재검출
→ TRACKING
```

시나리오를 테스트합니다.

---

# DAY 3 — 검증과 재현

목표:

> **누가 실행해도 같은 조건으로 결과를 재현할 수 있게 만든다.**

```text
1. 정상 30초 시험
2. 가림 5회
3. 목표 소실
4. 인지 중단
5. 제어 통신 중단
6. CSV 정리
7. RMSE 계산
8. 복구율 계산
9. rosbag 저장
10. rosbag replay
11. README 작성
12. 최종 시연
```

---

# 10. 그리고 지금 당장 할 TODO

여기가 가장 중요합니다.

**지금은 문제 1~5를 전부 건드릴 시간이 아닙니다.**

현재 상태가

> RealSense 구동 가능 + Dynamixel 2대 구동 가능

이므로 **오늘 첫 목표는 ROS2 연결 골격을 만드는 것**입니다.

## 🔴 지금 바로

### TODO 1 — 팀의 ROS2 인터페이스부터 고정

문서에 다음을 확정합니다.

```text
/target
/tracking_status
/motor_command
/motor_state
```

각 Topic의

```text
Type
Publisher
Subscriber
Data 의미
단위
```

를 표로 만듭니다.

---

### TODO 2 — 패키지 구조 만들기

예:

```text
src/
├── perception/
├── control/
├── motor_driver/
├── tracking_interfaces/
└── bringup/
```

역할을 분리합니다.

```text
perception
→ RealSense + HSV

control
→ P Controller + State Machine

motor_driver
→ Dynamixel

tracking_interfaces
→ msg/srv

bringup
→ launch/parameter
```

---

### TODO 3 — Mock `/target` 만들기

**실제 카메라부터 붙이지 마세요.**

먼저:

```text
x = -0.4
x = 0
x = +0.4
```

를 발행하는 테스트 노드를 만듭니다.

그리고 제어 노드가:

```text
x < 0 → 방향 A
x = 0 → 정지
x > 0 → 방향 B
```

로 반응하는지 확인합니다.

이걸 먼저 하면 카메라 문제가 제어 문제로 섞이지 않습니다.

---

### TODO 4 — Dynamixel 2대 저속 테스트

Mock 입력:

```text
x = +0.4
```

를 넣었을 때

```text
Dynamixel #1
Dynamixel #2
```

가 **의도한 방향으로 움직이는지만** 확인합니다.

처음부터 추적 알고리즘을 돌리지 않습니다.

---

### TODO 5 — 실제 RealSense 연결

그 다음:

```text
RealSense
 ↓
Detection
 ↓
/target
```

만 연결합니다.

RViz든 OpenCV 화면이든 **검출 중심점이 실제 목표를 제대로 따라가는지 확인**합니다.

---

### TODO 6 — 첫 통합 테스트

마지막으로:

```text
RealSense
 ↓
HSV Detection
 ↓
/target
 ↓
P Controller
 ↓
Dynamixel × 2
```

를 연결합니다.

**이게 오늘의 1차 완료 기준입니다.**

---

# 11. 오늘 작업 우선순위

지금 당장 기준으로 압축하면:

```text
[1] 인터페이스 확정
       ↓
[2] ROS2 패키지/Node 골격
       ↓
[3] Mock /target
       ↓
[4] Control Node
       ↓
[5] Dynamixel 저속 제어
       ↓
[6] RealSense Detection
       ↓
[7] 실제 /target 연결
       ↓
[8] 전체 통합
```

그리고 **오늘은 여기까지만 해도 충분합니다.**

반대로 지금 하면 안 되는 것:

```text
❌ RMSE 최종 계산
❌ 30초 성능시험
❌ rosbag 최종 재현
❌ 보고서 작성
❌ Kp 최적값 찾기
❌ 복잡한 PID
❌ SEARCHING 기능
```

이것들은 **기본 Tracking Loop가 살아난 다음** 해야 합니다.

---

## 최종적으로 3일 동안 만들어야 하는 형태

```text
                 ┌──────────────┐
                 │   RealSense  │
                 └──────┬───────┘
                        │
                        ▼
               ┌─────────────────┐
               │ Perception Node │
               │ HSV + Contour   │
               └───────┬─────────┘
                       │
                    /target
                       │
                       ▼
               ┌─────────────────┐
               │  Control Node   │
               │ P + State       │
               │ IDLE/TRACK/LOST │
               └───────┬─────────┘
                       │
                motor command
                       │
                       ▼
               ┌─────────────────┐
               │ Dynamixel Node  │
               └───────┬─────────┘
                       │
                 ┌─────┴─────┐
                 ▼           ▼
               DXL #1      DXL #2


       ┌──────────────────────────────┐
       │       Verification           │
       │ FPS / Detection / RMSE       │
       │ Recovery / Timeout / Stop    │
       └──────────────┬───────────────┘
                      │
                      ▼
                   rosbag
                      │
                      ▼
                  Replay
```

**희우님이 제어 담당이라면 오늘 가장 먼저 잡아야 할 것은 `Control Node + /target subscriber + Dynamixel 2대 출력`입니다.** 인지팀이 아직 완성되지 않았더라도 Mock `/target`으로 제어를 먼저 완성할 수 있습니다. 그러면 인지팀이 `/target`만 제대로 넘겨주는 순간 바로 실제 통합이 가능합니다.