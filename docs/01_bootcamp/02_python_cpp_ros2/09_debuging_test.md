>작성일: 2026-08-14
>
>최종 수정일: 2026-08-14
>
> wlvlxl rowhgdk sjdjqtdl ahttkfdk
>

# 16강. 디버깅·시각화·테스트
## RViz2 · rqt · rosbag2 · pytest · gtest

> **학습 목표**
> - ROS2의 보이지 않는 분산 시스템을 목적에 맞는 도구로 관찰한다.
> - RViz2로 센서·TF·로봇 상태를 3D로 시각화한다.
> - rqt와 ROS2 CLI로 노드·토픽·수치·로그를 추적한다.
> - rosbag2로 현장 데이터를 기록하고 재생하여 문제를 재현한다.
> - pytest·gtest와 테스트 피라미드를 이용해 로봇 SW의 회귀 버그를 줄인다.

---

## 0. 한눈에 보는 핵심

ROS2 디버깅의 핵심은 **"보이지 않는 것을 보이게 만드는 것"**이다.

| 궁금한 것 | 주 도구 | 핵심 용도 |
|---|---|---|
| 노드와 토픽이 어떻게 연결됐나? | `rqt_graph` | 연결 구조 시각화 |
| 센서·TF·로봇이 공간상 어디에 있나? | `RViz2` | 3D 시각화 |
| 숫자가 어떻게 변하나? | `rqt_plot` | 실시간 수치 그래프 |
| 토픽이 존재하고 데이터가 오나? | `ros2 CLI` | 빠른 확인 |
| 현장에서 발생한 문제를 다시 재현하고 싶나? | `rosbag2` | 기록·재생 |
| 로그가 어디서 발생했나? | `rqt_console` | 로그 필터·확인 |
| 함수 로직이 맞나? | `pytest` / `gtest` | 단위 테스트 |
| 여러 노드가 함께 정상 동작하나? | `launch_test` | 통합 테스트 |
| 실제 환경에서 제대로 동작하나? | Gazebo / 실기 | 시스템 수준 검증 |

### 핵심 사고방식

```text
연결 문제 → rqt_graph
공간/좌표 문제 → RViz2
수치 문제 → rqt_plot
빠른 확인 → ros2 CLI
재현 문제 → rosbag2
로그 문제 → rqt_console
코드 회귀 문제 → pytest / gtest
노드 간 상호작용 → 통합 테스트
실제 로봇 동작 → 시뮬레이션 / 실기 테스트
```

---

# 1. ROS2 디버깅 도구 상자

ROS2는 여러 노드가 토픽·서비스·액션으로 연결되는 **분산 시스템**이다.

따라서 문제가 발생했을 때 코드에 `print()`를 추가하는 것만으로는 부족하다.

예를 들어:

> "인지 노드가 장애물을 놓친다."

이 경우 한 번에 코드를 뜯어보기보다 데이터 흐름을 단계적으로 확인한다.

```text
센서 데이터가 들어오는가?
        ↓
ros2 topic hz /scan

센서 토픽 내용이 정상인가?
        ↓
ros2 topic echo /scan

인지 노드가 토픽을 구독하고 있는가?
        ↓
rqt_graph / ros2 node info

인지 결과가 발행되는가?
        ↓
ros2 topic echo /obstacles

결과의 위치가 올바른가?
        ↓
RViz2
```

## 자주 쓰는 ROS2 CLI

```bash
# 토픽 목록
ros2 topic list

# 토픽 내용 확인
ros2 topic echo /topic_name

# 토픽 발행 주기 확인
ros2 topic hz /topic_name

# 토픽의 타입/QoS/Publisher/Subscriber 정보
ros2 topic info /topic_name

# 노드 목록
ros2 node list

# 특정 노드 정보
ros2 node info /node_name

# 직접 메시지 발행
ros2 topic pub ...
```

### CLI + rqt 조합

```bash
ros2 topic list
ros2 topic echo /obstacles
ros2 topic hz /scan
ros2 node info /perception_node
```

그리고 전체 연결 관계는:

```bash
rqt_graph
```

---

# 2. RViz2 — 로봇의 상태를 3D로 보기

## 2.1 RViz2가 하는 일

RViz2는 ROS2의 대표적인 **3D 시각화 도구**다.

숫자와 메시지로만 존재하는 데이터를 공간 속에 표현한다.

### 주요 시각화 대상

- LiDAR 점군
- Camera/Image
- Depth 데이터
- TF 좌표계
- RobotModel(URDF)
- 경로(Path)
- 장애물
- Marker / MarkerArray

특히 **TF 좌표 변환 디버깅**에서 매우 중요하다.

---

# 3. Marker — 내가 계산한 결과를 RViz2에 표시하기

RViz2는 **토픽에 실제로 발행된 데이터만 그린다.**

따라서 프로그램 내부에서 계산한 좌표나 장애물 정보를 눈으로 보고 싶다면 `Marker` 메시지로 만들어 토픽에 발행해야 한다.

사용 메시지:

```python
from visualization_msgs.msg import Marker
```

## 기본 Marker 예제

```python
from visualization_msgs.msg import Marker

m = Marker()

# 기준 좌표계
m.header.frame_id = 'world'
m.header.stamp = self.get_clock().now().to_msg()

# 식별자
m.ns = 'waypoints'
m.id = 0

# 형태
m.type = Marker.SPHERE
m.action = Marker.ADD

# 위치
m.pose.position.x = 2.0
m.pose.position.y = 3.0
m.pose.position.z = 0.0

# 회전 없음
m.pose.orientation.w = 1.0

# 크기 [m]
m.scale.x = 0.2
m.scale.y = 0.2
m.scale.z = 0.2

# 색상 + 불투명도
m.color.r = 1.0
m.color.g = 0.0
m.color.b = 0.0
m.color.a = 1.0

self.marker_pub.publish(m)
```

## Marker 주요 필드

| 필드 | 의미 |
|---|---|
| `header.frame_id` | 어느 좌표계 기준인지 |
| `header.stamp` | 메시지 시간 |
| `ns` | Marker namespace |
| `id` | Marker 식별 번호 |
| `type` | Sphere, Cube, Arrow, Line 등 |
| `pose` | 위치·회전 |
| `scale` | 크기 |
| `color.r/g/b/a` | 색상 및 투명도 |
| `action` | ADD, DELETE 등 |

### 여러 점을 표시할 때

```text
Marker.SPHERE_LIST
MarkerArray
```

등을 활용한다.

---

# 4. RViz2에서 Marker가 안 보일 때

Marker가 보이지 않을 때 가장 먼저 확인할 것은 세 가지다.

## 체크리스트

### 1) `scale`이 0인가?

```python
m.scale.x = 0.2
m.scale.y = 0.2
m.scale.z = 0.2
```

`scale = 0`이면 사실상 보이지 않는다.

### 2) `color.a`가 0인가?

```python
m.color.a = 1.0
```

`alpha = 0`이면 완전히 투명하다.

### 3) RViz2의 Fixed Frame과 `frame_id`가 맞는가?

예:

```text
Marker:
frame_id = world

RViz2:
Fixed Frame = world
```

좌표계가 맞지 않으면 Marker가 정상적으로 존재해도 화면에 나타나지 않을 수 있다.

## RViz2 설정

```text
RViz2
 └─ Add
     └─ By topic
         └─ /markers
```

### 핵심

> **RViz2는 토픽에 있는 데이터만 그린다.**

내가 계산한 결과를 RViz2에서 보고 싶다면:

```text
계산
 ↓
Marker 생성
 ↓
Marker 토픽 publish
 ↓
RViz2 Add → By topic
 ↓
3D 화면에서 확인
```

---

# 5. RViz2의 진짜 장점 — 여러 정보를 겹쳐 보기

RViz2는 하나의 공간에 여러 데이터를 동시에 표시할 수 있다.

예:

```text
LiDAR 장애물
      +
인지 결과
      +
RobotModel
      +
TF
      +
Path
```

이렇게 겹쳐 보면 다음과 같은 문제를 빠르게 찾을 수 있다.

- 센서 위치가 잘못됨
- TF 변환이 잘못됨
- 장애물 좌표가 틀림
- 로봇 기준 좌표와 월드 좌표가 뒤섞임
- 경로가 예상 위치와 다름

따라서 **TF 디버깅에서 RViz2는 사실상 필수 도구**다.

---

# 6. rosbag2 — 기록하고 재생하기

## 6.1 왜 rosbag이 필요한가?

로봇 문제의 가장 큰 어려움 중 하나는 **재현성**이다.

예:

> "야외에서 오후 3시에 한 번 발생한 오작동"

로봇을 다시 같은 장소에 가져가 같은 상황을 만들기 어렵다.

`rosbag2`는 토픽 데이터를 파일로 기록했다가 나중에 재생할 수 있게 한다.

```text
실제 로봇
   ↓
rosbag2 record
   ↓
.db3 파일
   ↓
rosbag2 play
   ↓
책상에서 데이터 재현
```

---

# 7. rosbag2 기본 명령

## 특정 토픽 기록

```bash
ros2 bag record /scan /image /tf
```

## 전체 토픽 기록

```bash
ros2 bag record -a -o field_test_01
```

## 재생

```bash
ros2 bag play field_test_01
```

## 내용 확인

```bash
ros2 bag info field_test_01
```

`ros2 bag info`에서는 토픽, 메시지 수, 기록 기간 등의 정보를 확인할 수 있다.

---

# 8. rosbag2의 활용

rosbag2는 단순한 디버깅 도구를 넘어 다음에도 사용된다.

### 1) 문제 재현

```text
현장
 ↓
record
 ↓
문제 데이터 확보
 ↓
책상
 ↓
play
 ↓
반복 디버깅
```

### 2) 데이터셋 구축

AI/인지 알고리즘 학습에 필요한 로봇 데이터를 확보할 수 있다.

### 3) 회귀 테스트

같은 입력 데이터를 다시 넣어서 알고리즘이 이전보다 나빠지지 않았는지 확인할 수 있다.

### 핵심 문장

> **현장에서 한 번 기록하고, 책상에서 무한 재생한다.**

이것은 로봇 SW 개발 생산성을 크게 높이는 방법이다.

---

# 9. 예외 처리 — 노드가 죽지 않게 하기

ROS2 노드에서 예외가 콜백 밖으로 새어 나가면 노드의 정상적인 동작이 중단될 수 있다.

특히 로봇은 마지막 명령 상태가 위험할 수 있다.

따라서 **실패할 수 있는 최소한의 코드만 `try`로 감싼다.**

```python
def on_scan(self, msg):
    try:
        d = self.nearest(msg)

    except (ValueError, ZeroDivisionError):
        self.get_logger().warn('스캔 한 프레임 건너뜀')
        return

    self.publish(d)
```

## 좋은 예외 처리 원칙

### 좁게 잡기

좋지 않은 예:

```python
except Exception:
    pass
```

이렇게 하면 `NameError`, `TypeError` 같은 **내 코드의 버그까지 숨겨질 수 있다.**

좋은 방향:

```python
except (ValueError, ZeroDivisionError):
    ...
```

즉, **내가 알고 있고 대응 방법도 알고 있는 예외만 잡는다.**

---

# 10. 복구할 수 없는 오류는 정지시킨다

모터 통신이 끊겼는데 상태를 알 수 없는 상황에서 계속 명령을 내리는 것은 위험하다.

이런 경우에는:

```text
이상 발생
 ↓
안전 정지 명령
 ↓
필요한 자원 정리
 ↓
노드 종료
```

가 더 안전할 수 있다.

## 종료 경로

`finally` 또는 `destroy_node()` 등의 종료 처리에서 다음을 고려한다.

- 정지 명령
- 모터 비활성화
- 통신 포트 정리
- 파일/자원 정리

### 핵심

> **복구할 수 없는 오류를 억지로 숨기는 것보다 안전하게 정지하는 것이 낫다.**

---

# 11. ROS2 Logging

`print()` 대신 ROS2 노드의 logger를 사용한다.

```python
self.get_logger().debug(...)
self.get_logger().info(...)
self.get_logger().warn(...)
self.get_logger().error(...)
self.get_logger().fatal(...)
```

로그는 `rqt_console`에서 확인하고 필터링할 수 있다.

---

# 12. 로그 레벨

| 레벨 | 의미 | 예시 |
|---|---|---|
| `debug` | 개발 중 상세 추적 | 매 주기 중간값 |
| `info` | 정상적인 상태 변화 | "라이다 연결됨" |
| `warn` | 이상하지만 계속 가능 | "스캔 일부 누락" |
| `error` | 기능 하나가 실패 | "지도 저장 실패" |
| `fatal` | 계속할 수 없음 | "모터 통신 단절 — 정지" |

## 실무적인 로그 작성

모든 주기에 `info`를 출력하면 로그가 너무 많아진다.

좋은 기준:

```text
상태가 바뀌는 순간 → info
반복되는 이상 → warn
기능 실패 → error
계속 실행 불가 → fatal
개발 중 상세 정보 → debug
```

예:

```text
좋지 않은 방식
→ 매 10ms마다 "scan received"

좋은 방식
→ "최근 10초간 스캔 37개 누락"
```

---

# 13. 테스트 — 문제가 생기기 전에 잡기

디버깅:

> 이미 발생한 문제를 찾고 고친다.

테스트:

> 문제가 발생하기 전에 발견한다.

로봇 SW에서는 버그가 물리적 사고로 연결될 수 있으므로 테스트의 가치가 크다.

---

# 14. 테스트 피라미드

기본적인 테스트 전략은 **테스트 피라미드**로 생각할 수 있다.

```text
           /\
          /  \
         / 시뮬레이션·실기 \
        /----------------\
       /   통합 테스트      \
      /--------------------\
     /      단위 테스트       \
    /________________________\
```

아래로 갈수록:

- 빠르다
- 많이 실행할 수 있다
- 자동화하기 쉽다

위로 갈수록:

- 현실성이 높다
- 느리다
- 실행 비용이 크다

따라서:

> **빠른 단위 테스트를 두껍게, 느린 실기 테스트를 얇게 만든다.**

---

# 15. pytest — Python 단위 테스트

ROS2와 무관한 순수 함수는 ROS2를 띄우지 않고 테스트하는 것이 좋다.

예:

```python
# test_safety.py

from robot_utils.safety import compute_stop_distance


def test_stop_distance_zero_speed():
    assert compute_stop_distance(0.0) == 0.0


def test_stop_distance_increases_with_speed():
    assert compute_stop_distance(2.0) > compute_stop_distance(1.0)


def test_stop_distance_formula():
    # v=1.0, decel=1.5
    # stop distance = 1.0 / (2 * 1.5)
    assert abs(compute_stop_distance(1.0) - 1/3) < 1e-6
```

실행:

```bash
pytest test_safety.py -v
```

## 좋은 단위 테스트

### 경계값

```text
0
음수
최댓값
최솟값
```

### 불변식

예:

```text
속도가 증가하면 정지거리도 증가한다.
```

### 공식

```text
stop_distance = v² / (2a)
```

제어·안전 로직처럼 물리와 직접 연결되는 함수는 특히 촘촘하게 테스트한다.

---

# 16. gtest — C++ 단위 테스트

C++에서는 GoogleTest(gtest)를 사용한다.

```cpp
#include <gtest/gtest.h>
#include "robot_utils/safety.hpp"

TEST(SafetyTest, ZeroSpeed) {
    EXPECT_DOUBLE_EQ(
        computeStopDistance(0.0),
        0.0
    );
}

TEST(SafetyTest, IncreasesWithSpeed) {
    EXPECT_GT(
        computeStopDistance(2.0),
        computeStopDistance(1.0)
    );
}
```

Python:

```text
pytest
```

C++:

```text
gtest
```

---

# 17. 테스트하기 좋은 코드 구조

ROS2 노드 코드를 테스트하기 쉽게 만들려면 **ROS2에 강하게 묶인 코드와 순수 로직을 분리**하는 것이 좋다.

좋은 구조:

```text
ROS2 Node
 ├─ topic subscribe/publish
 ├─ timer
 └─ parameter
       ↓
   순수 계산 함수
       ↓
   pytest / gtest
```

예:

```python
def compute_stop_distance(speed, decel):
    return speed ** 2 / (2 * decel)
```

이런 함수는 ROS2를 실행하지 않고도 테스트할 수 있다.

### 핵심 원칙

> **입출력이 명확한 순수 로직을 최대한 분리하면 테스트가 쉬워진다.**

---

# 18. 통합 테스트

단위 테스트만으로는 다음 문제를 잡을 수 없다.

> "노드 A가 발행한 메시지를 노드 B가 제대로 받아 처리하는가?"

이런 문제에는 **통합 테스트**가 필요하다.

ROS2에서는 `launch_test` 등을 이용해 여러 노드를 실행하고 실제 토픽 흐름을 검증할 수 있다.

```text
Node A
  ↓ topic
Node B
  ↓ topic
Node C
```

단위 테스트:

```text
A 내부 함수가 맞는가?
```

통합 테스트:

```text
A → B → C 연결과 동작이 맞는가?
```

---

# 19. 시뮬레이션·실기 테스트

테스트 피라미드의 가장 위에는 실제 환경 검증이 있다.

예:

```text
Gazebo
 ↓
가상 로봇
 ↓
장애물 배치
 ↓
정지 알고리즘 실행
 ↓
정말 멈추는가?
```

그 다음 실제 로봇에서 검증한다.

### 현실적인 전략

```text
단위 테스트
   ↓
통합 테스트
   ↓
시뮬레이션
   ↓
실기
```

가능하면 아래 단계에서 최대한 많은 문제를 잡는다.

---

# 20. rosbag + 테스트 = 회귀 테스트

rosbag2를 테스트 전략과 결합하면 강력하다.

```text
현장 데이터
   ↓
rosbag record
   ↓
문제 상황 저장
   ↓
rosbag play
   ↓
인지/제어 알고리즘
   ↓
기대 결과와 비교
```

이후 코드가 변경될 때 같은 데이터를 다시 넣는다.

```text
이전 버전
→ 정상

새 버전
→ 실패

⇒ 회귀 버그 발견
```

즉, **현장에서 확보한 실제 데이터를 반복 가능한 테스트 입력으로 만들 수 있다.**

---

# 21. CI와 테스트

4강에서 배운 GitHub Actions와 연결하면 PR마다 자동으로 테스트할 수 있다.

```text
개발자
 ↓
git push
 ↓
Pull Request
 ↓
CI 실행
 ↓
pytest / gtest
 ↓
통과 → 병합 가능
실패 → 수정
```

특히 안전 로직을 수정했을 때 테스트가 자동으로 실행되도록 하면 회귀 버그를 빠르게 발견할 수 있다.

---

# 22. 문제 상황별 디버깅 순서

## 상황 A. "토픽 데이터가 안 온다"

```text
1. ros2 topic list
        ↓
2. ros2 topic info /topic
        ↓
3. ros2 topic hz /topic
        ↓
4. ros2 topic echo /topic
        ↓
5. ros2 node info /node
        ↓
6. rqt_graph
```

확인할 것:

- 토픽이 존재하는가?
- Publisher가 있는가?
- Subscriber가 있는가?
- 데이터가 실제로 발행되는가?
- 주파수가 정상인가?
- 연결이 끊겼는가?

---

## 상황 B. "데이터는 오는데 화면에서 이상하다"

```text
ros2 topic echo
      ↓
메시지 값 확인
      ↓
RViz2
      ↓
TF 확인
      ↓
Fixed Frame 확인
```

특히 좌표 문제라면:

```text
frame_id
TF
Fixed Frame
```

을 우선 확인한다.

---

## 상황 C. "현장에서만 발생하는 문제"

```text
현장
 ↓
ros2 bag record
 ↓
문제 데이터 확보
 ↓
ros2 bag play
 ↓
책상에서 반복 재현
```

---

## 상황 D. "코드 수정 후 기존 기능이 깨졌다"

```text
pytest / gtest
      ↓
실패한 테스트 확인
      ↓
코드 수정
      ↓
전체 테스트 재실행
```

필요하면 rosbag 기반 회귀 테스트까지 연결한다.

---

# 23. 미니 퀴즈 정답

## 1번

**정답: ③ rosbag2**

기록한 ROS2 토픽 데이터를 나중에 다시 재생하여 문제를 재현할 수 있다.

---

## 2번

**RViz2**

> 센서·TF·로봇·경로 등의 데이터를 3D 공간에서 시각화한다.

**rqt_graph**

> ROS2 노드와 토픽의 연결 관계를 그래프로 보여준다.

---

## 3번

**Python → pytest**

**C++ → gtest**

---

## 4번

> ROS2 통신 코드와 순수 계산·비즈니스 로직을 분리하여, 핵심 로직을 ROS2 없이도 테스트할 수 있도록 구성한다.

---

## 5번

`ros2 topic hz /scan`이 기대보다 낮을 때 의심할 수 있는 원인:

1. 센서/Publisher 자체의 발행 주기가 낮아졌다.
2. CPU 부하나 시스템 지연으로 데이터 처리가 늦어졌다.
3. QoS 설정이 맞지 않아 메시지 전달에 문제가 있다.
4. 네트워크/통신 문제가 있다.
5. Subscriber 또는 Publisher 측의 처리 병목이 있다.

---

# 24. 실습 정리

## 실습 1 — 흐름 추적 디버깅

목표:

> "데이터가 안 오는 문제"를 단계적으로 진단한다.

```bash
# Publisher/Subscriber 실행

rqt_graph

ros2 topic hz /chatter
```

Publisher를 종료한 뒤 `ros2 topic hz`가 어떻게 변하는지 관찰한다.

### 확인 순서

```text
토픽 존재?
 ↓
Publisher 존재?
 ↓
Subscriber 존재?
 ↓
실제 데이터 존재?
 ↓
주파수 정상?
 ↓
rqt_graph 연결 정상?
```

---

## 실습 2 — rosbag 재현

Talker 실행:

```bash
ros2 bag record /chatter
```

기록이 끝난 뒤 Talker를 종료한다.

그 다음:

```bash
ros2 bag play <bag_directory>
```

Listener가 다시 `/chatter` 데이터를 받는지 확인한다.

### 학습 포인트

> 실제 Publisher가 없어도 기록된 데이터의 흐름을 재현할 수 있다.

---

## 실습 3 — RViz2

TurtleBot3 시뮬레이션 또는 정적 TF를 실행하고 RViz2에서:

- TF
- RobotModel
- 센서 데이터
- 좌표계

등을 확인한다.

14강에서 배운 TF 프레임 트리가 실제 3D 공간에서 어떻게 표현되는지 관찰한다.

---

## 실습 4 — pytest

`compute_stop_distance`에 대해 최소 3개의 테스트를 작성한다.

```text
경계값 테스트
불변식 테스트
공식 테스트
```

그리고 일부러 함수를 잘못 수정한다.

```text
정상 코드
 ↓
pytest 통과

잘못된 코드
 ↓
pytest 실패
```

테스트가 실제 오류를 잡는지 확인한다.

---

## 실습 5 — GitHub Actions

pytest/gTest를 GitHub Actions에 연결한다.

목표:

```text
PR 생성
 ↓
CI 자동 실행
 ↓
테스트
 ↓
실패하면 병합 전에 발견
```

---

# 25. 핵심 명령어 치트시트

## ROS2 CLI

```bash
ros2 topic list
ros2 topic echo /topic
ros2 topic hz /topic
ros2 topic info /topic

ros2 node list
ros2 node info /node

ros2 topic pub ...
```

## rqt

```bash
rqt_graph
rqt_plot
rqt_console
```

## rosbag2

```bash
ros2 bag record /scan /image /tf

ros2 bag record -a -o field_test_01

ros2 bag play field_test_01

ros2 bag info field_test_01
```

## pytest

```bash
pytest test_safety.py -v
```

---

# 26. 최종 암기 포인트

### 도구 선택

```text
rqt_graph → 연결
RViz2     → 공간
rqt_plot  → 수치
ros2 CLI  → 빠른 확인
rosbag2   → 기록·재현
rqt_console → 로그
pytest    → Python 단위 테스트
gtest     → C++ 단위 테스트
launch_test → 통합 테스트
Gazebo/실기 → 시스템 검증
```

### RViz2

```text
계산 결과
 ↓
Marker
 ↓
토픽 publish
 ↓
RViz2 Add → By topic
 ↓
Fixed Frame 확인
```

Marker가 안 보이면 먼저:

```text
1. scale == 0 ?
2. color.a == 0 ?
3. Fixed Frame 불일치 ?
```

### rosbag2

```text
현장 기록
 ↓
.db3
 ↓
책상 재생
 ↓
문제 재현
 ↓
반복 디버깅 / 회귀 테스트
```

### 예외 처리

```text
알고 있는 예외만 좁게 잡기
        ↓
warn + return
        ↓
다음 주기 재시도
```

복구 불가능한 오류:

```text
안전 정지
 ↓
자원 정리
 ↓
종료
```

### 테스트 피라미드

```text
        실기
      시뮬레이션
      통합 테스트
     단위 테스트
```

> **아래로 갈수록 빠르고 많이, 위로 갈수록 현실적이고 느리다.**

---

# 27. 이번 강의의 핵심 한 문장

> **ROS2 디버깅은 "보이지 않는 분산 시스템을 보이게 만드는 것"이고, 테스트는 "문제가 발생하기 전에 잡는 것"이다.**

```text
관찰
→ rqt / RViz2 / CLI

재현
→ rosbag2

예외·로그
→ logger + 안전한 예외 처리

검증
→ pytest / gtest

통합
→ launch_test

현실 검증
→ Gazebo / 실기
```
