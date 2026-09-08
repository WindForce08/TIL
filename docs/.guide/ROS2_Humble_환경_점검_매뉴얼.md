# ROS 2 Humble 설치 후 환경 점검 매뉴얼

> 목적: Ubuntu 22.04 환경에서 ROS 2 Humble 설치가 정상적으로 되었는지 단계적으로 확인하고, 이후 Physical AI / 로봇 개발을 시작하기 전에 기본 환경을 검증한다.

---

## 1. ROS 2 배포판 확인

### 명령어

```bash
echo $ROS_DISTRO
```

### 정상 결과

```text
humble
```

### 판단

- `humble` 출력 → ROS 2 Humble 환경이 현재 터미널에 적용된 상태
- 아무것도 출력되지 않음 → ROS 2 환경 설정이 현재 터미널에 적용되지 않았을 가능성

---

## 2. ROS 2 CLI 확인

### 명령어

```bash
ros2 --help
```

### 정상 판단

다음과 같이 `ros2` 명령어의 도움말과 여러 하위 명령어가 출력되면 정상이다.

예:

```text
usage: ros2 [-h] [--use-python-default-buffering]
...
Commands:
  action
  bag
  component
  daemon
  launch
  node
  param
  pkg
  run
  topic
  ...
```

---

## 3. ROS 2 패키지 인식 확인

### 명령어

간단히 확인:

```bash
ros2 pkg list | head
```

또는 전체 목록 확인:

```bash
ros2 pkg list
```

### 정상 결과 예시

```text
ackermann_msgs
action_msgs
action_tutorials_cpp
action_tutorials_interfaces
action_tutorials_py
actionlib_msgs
ament_cmake
ament_cmake_auto
ament_cmake_copyright
ament_cmake_core
```

### 참고: BrokenPipeError

다음과 같이 실행했을 때:

```bash
ros2 pkg list | head
```

마지막에 아래 메시지가 나타날 수 있다.

```text
BrokenPipeError: [Errno 32] Broken pipe
```

이는 `head`가 앞부분만 읽고 종료하면서 ROS 2가 계속 출력하려다가 발생하는 메시지다.

**ROS 2 설치 오류가 아니므로 걱정할 필요가 없다.**

---

## 4. ROS 2 Doctor 기본 검사

### 명령어

```bash
ros2 doctor
```

### 정상 결과

```text
All 5 checks passed
```

### 판단

`All 5 checks passed`가 나오면 ROS 2 기본 환경 검사가 모두 통과한 것이다.

---

## 5. ROS 2 Doctor 상세 검사

### 명령어

```bash
ros2 doctor --report
```

다음 항목을 중심으로 확인한다.

### 5-1. Platform Information

예:

```text
system           : Linux
platform info    : Linux-6.8.0-...-x86_64-with-glibc2.35
processor        : x86_64
```

---

### 5-2. RMW Middleware

예:

```text
middleware name    : rmw_fastrtps_cpp
```

현재 ROS 2가 어떤 DDS/RMW 구현을 사용하는지 확인한다.

---

### 5-3. ROS 2 Information

정상적인 Humble 환경에서는 다음과 같이 확인한다.

```text
distribution name      : humble
distribution type      : ros2
distribution status    : active
release platforms      : {'rhel': ['8'], 'ubuntu': ['jammy']}
```

특히 다음 2개를 확인한다.

```text
distribution name      : humble
distribution status    : active
```

---

### 5-4. Topic List

`ros2 doctor --report` 실행 당시 ROS 2 노드가 실행되고 있지 않다면 다음처럼 나오는 것이 정상이다.

```text
topic               : none
publisher count     : 0
subscriber count    : 0
```

이것은 ROS 2가 고장났다는 의미가 아니다.

실행 중인 ROS 2 노드가 없기 때문이다.

---

## 6. 설치된 주요 패키지 확인

`ros2 doctor --report`의 PACKAGE VERSIONS 항목을 이용하여 주요 개발 패키지가 설치되어 있는지 확인한다.

### Navigation

```text
navigation2
nav2_bringup
nav2_amcl
nav2_controller
nav2_planner
nav2_map_server
```

### SLAM

```text
slam_toolbox
cartographer_ros
```

### Gazebo

```text
gazebo_ros
gazebo_ros2_control
gazebo_plugins
gazebo_ros_pkgs
```

### RViz

```text
rviz2
rviz_common
rviz_default_plugins
```

### ros2_control

```text
ros2_control
controller_manager
diff_drive_controller
joint_state_broadcaster
```

### Python / C++

```text
rclpy
rclcpp
```

### TF / Robot Description

```text
tf2
tf2_ros
robot_state_publisher
urdf
xacro
```

### TurtleBot3

```text
turtlebot3
turtlebot3_bringup
turtlebot3_gazebo
turtlebot3_navigation2
turtlebot3_description
```

---

## 7. 패키지 업데이트 경고 확인

`ros2 doctor` 실행 시 다음과 같은 경고가 나타날 수 있다.

```text
UserWarning: ... has been updated to a new version.
local: ... < latest: ...
```

예:

```text
imu_sensor_broadcaster
local: 2.53.3 < latest: 2.54.0

diff_drive_controller
local: 2.53.3 < latest: 2.54.0
```

### 판단

이 메시지는 일반적으로 **설치 실패가 아니라 업데이트 가능한 패키지가 있다는 경고**다.

따라서 환경 점검 단계에서 반드시 모든 패키지를 최신 버전으로 올릴 필요는 없다.

특히 ROS 2 + Gazebo + ros2_control 환경에서는 패키지 버전 호환성이 중요하므로, 문제없이 동작하는 환경이라면 무작정 전체 업데이트하지 않는 것을 권장한다.

---

# 8. 실제 ROS 2 통신 테스트

`ros2 doctor`는 ROS 2 환경을 검사하지만, 실제 노드 간 통신까지 확인하려면 간단한 Publisher / Subscriber 테스트를 수행한다.

## Step 1 — Publisher 실행

터미널 1:

```bash
ros2 run demo_nodes_cpp talker
```

정상 예:

```text
[INFO] ... Publishing: 'Hello World: 0'
[INFO] ... Publishing: 'Hello World: 1'
[INFO] ... Publishing: 'Hello World: 2'
```

---

## Step 2 — Topic 확인

새 터미널을 열고:

```bash
ros2 topic list
```

정상적으로 다음 Topic이 나타나는지 확인한다.

```text
/chatter
```

---

## Step 3 — Subscriber 확인

```bash
ros2 topic echo /chatter
```

정상적으로 메시지가 계속 출력되면 ROS 2 노드 간 Topic 통신이 정상이다.

---

# 9. 최종 점검 체크리스트

```text
[ ] echo $ROS_DISTRO
        └─ humble

[ ] ros2 --help
        └─ ROS 2 CLI 정상

[ ] ros2 pkg list
        └─ 패키지 정상 인식

[ ] ros2 doctor
        └─ All 5 checks passed

[ ] ros2 doctor --report
        ├─ distribution name : humble
        ├─ distribution status : active
        └─ RMW middleware 확인

[ ] 주요 패키지 확인
        ├─ Nav2
        ├─ Gazebo
        ├─ RViz2
        ├─ ros2_control
        ├─ SLAM
        └─ TurtleBot3

[ ] demo_nodes_cpp talker
        └─ Publisher 정상 실행

[ ] ros2 topic list
        └─ /chatter 확인

[ ] ros2 topic echo /chatter
        └─ Publisher / Subscriber 통신 확인
```

---

# 10. 현재 PC에서 확인된 기준 상태

이번 점검에서 확인된 환경:

- ROS 2 distribution: **Humble**
- distribution status: **active**
- RMW: **rmw_fastrtps_cpp**
- ROS 2 Doctor: **5/5 checks passed**
- OS 계열: **Ubuntu 22.04 (Jammy)**
- CPU architecture: **x86_64**
- Nav2: 설치 확인
- Gazebo: 설치 확인
- RViz2: 설치 확인
- ros2_control: 설치 확인
- SLAM 관련 패키지: 설치 확인
- TurtleBot3 관련 패키지: 설치 확인
- `rclpy` / `rclcpp`: 설치 확인

## 핵심 판단

```text
ROS 2 Humble 설치 상태
        ↓
      정상
        ↓
ROS 2 CLI
        ↓
      정상
        ↓
패키지 인식
        ↓
      정상
        ↓
ros2 doctor
        ↓
    5/5 통과
        ↓
ROS 2 환경 기본 점검 완료
        ↓
실제 노드/Topic 통신 테스트
        ↓
최종 동작 검증
```

> 이 문서는 ROS 2 Humble 설치 후 환경 점검용 기본 매뉴얼로 사용한다.
