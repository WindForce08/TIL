# TIL — SSH 원격 운용과 udev 센서 장치 경로 고정

> 학습 범위: 템플릿 4번부터 마지막 디버깅까지  
> 핵심 주제: `udev`, 장치 식별, 심볼릭 링크, 재연결 검증, ROS2 센서 운용 관점

---

## 1. 오늘 배운 것

이번 실습의 목표는 IMU와 LiDAR에 고정된 이름을 부여하는 것이었다.

```text
IMU   → /dev/robot_imu
LiDAR → /dev/robot_lidar
```

처음에는 `udevadm info --attribute-walk /dev/loopN`에서 서로 다른 값을 하나 찾고 그 값을 udev 규칙에 넣으면 장치 이름이 고정될 것이라고 생각했다.

실제로 처음에는 다음 규칙이 정상적으로 동작했다.

```udev
ATTR{diskseq}=="39", SYMLINK+="robot_lidar"
ATTR{diskseq}=="41", SYMLINK+="robot_imu"
```

초기 확인 결과:

```text
/dev/robot_imu   -> loop18
/dev/robot_lidar -> loop17
```

그러나 장치를 해제하고 다시 연결하는 테스트에서 규칙이 깨졌다.

이번 실습의 가장 중요한 깨달음은 다음과 같다.

> **현재 장치를 구별할 수 있는 값과, 재연결 후에도 같은 장치를 식별할 수 있는 값은 다르다.**

---

# 2. 템플릿 3에서 다시 확인한 것 — SSH와 SCP

## 2-1. 원격 단일 명령 실행

```bash
ssh pa31@localhost 'uname -a'
```

`ssh 사용자@서버 '명령'` 형태를 사용하면 원격 접속 후 명령 하나를 실행하고 결과를 받을 수 있다.

실제 로봇에서는 헤드리스 로봇 PC에 접속하지 않고도 명령을 실행하는 방식으로 활용할 수 있다.

## 2-2. SCP 파일 전송

```bash
scp ~/lv1.txt pa31@localhost:~/scp_test/
```

전송 후:

```bash
ssh pa31@localhost 'ls -l ~/scp_test/lv1.txt'
```

로 파일 존재 여부를 확인했다.

### 배운 점

```text
SSH  → 원격 명령 실행
SCP  → 파일 전송
```

실제 로봇에서는 개발 PC에서 로봇 PC로 설정 파일, 스크립트 등을 전송할 때 사용할 수 있다.

---

# 3. SSH 실습에서 헷갈렸던 부분

## 3-1. `deactivate`와 `exit`

처음 SSH 세션을 종료하려고 `deactivate`를 입력했지만 명령을 찾을 수 없었다.

```text
SSH 세션 종료 → exit
Python virtual environment 종료 → deactivate
```

## 3-2. localhost도 실제 SSH 인증을 거친다

```bash
echo $SSH_CONNECTION
```

결과:

```text
127.0.0.1 41284 127.0.0.1 22
```

따라서 localhost라도 SSH 서버를 통한 실제 SSH 연결이며, 사용자 이름과 인증 방식이 중요하다.

실습 중 `pa31`과 `p31`을 혼동하여 인증 실패를 경험하면서 **비밀번호 문제와 사용자 이름 문제를 구분해서 확인해야 한다**는 것도 배웠다.

---

# 4. udev 실습의 출발점 — loop 장치

가상 IMU와 LiDAR가 loop 장치로 만들어졌고 초기에는 다음과 같았다.

```text
LiDAR → /dev/loop17
IMU   → /dev/loop18
```

처음에는 `loop17`, `loop18`을 센서의 이름처럼 생각하기 쉬웠지만, 실제로는 현재 연결 상태에서 커널이 부여한 장치 이름이다.

따라서:

```udev
KERNEL=="loop17"
```

처럼 규칙을 작성하면 현재 상태에서는 매칭될 수 있지만 재연결 후 번호가 달라질 수 있다.

---

# 5. `udevadm info --attribute-walk`를 조사한 이유

다음 명령을 사용했다.

```bash
udevadm info --attribute-walk /dev/loopN
```

처음에는 다음과 같이 생각했다.

```text
IMU와 LiDAR 속성 비교
        ↓
서로 다른 속성 찾기
        ↓
udev 규칙에 사용
        ↓
고정 이름 생성
```

하지만 실습을 통해 **서로 다른 값이라는 조건만으로는 부족하다**는 것을 알게 되었다.

실제로 필요한 조건은:

```text
구별 가능
+
재연결 후에도 유지
=
안정적인 장치 식별 기준
```

이다.

---

# 6. 처음 선택한 `diskseq`

초기 상태에서 다음과 같이 구별되었다.

```text
LiDAR → /dev/loop17 → ATTR{diskseq}=="39"
IMU   → /dev/loop18 → ATTR{diskseq}=="41"
```

그래서 `diskseq`를 장치 식별 기준으로 선택했다.

```udev
ATTR{diskseq}=="39", SYMLINK+="robot_lidar"
ATTR{diskseq}=="41", SYMLINK+="robot_imu"
```

초기 확인:

```bash
ls -l /dev/robot_lidar /dev/robot_imu
```

결과:

```text
/dev/robot_imu   -> loop18
/dev/robot_lidar -> loop17
```

즉 **초기 연결에서는 성공했다.**

---

# 7. 내가 처음 놓친 부분

처음에는 다음 두 가지를 같은 의미로 생각했다.

```text
① 현재 IMU를 다른 장치와 구별할 수 있다.
② IMU를 다시 연결해도 같은 장치라고 식별할 수 있다.
```

하지만 실제로는 다르다.

현재:

```text
IMU → diskseq 41
LiDAR → diskseq 39
```

라고 해서 `diskseq=41`이 IMU의 영구적인 신분증이라는 뜻은 아니다.

> **현재 상태에서 구별되는 값과 장치 자체에 고정된 식별 정보는 다르다.**

---

# 8. 재연결 테스트

규칙을 다시 불러왔다.

```bash
sudo udevadm control --reload-rules
```

두 장치를 해제한 뒤 기존과 다른 순서로 다시 연결하고:

```bash
ls -l /dev/robot_*
```

를 실행했다.

결과:

```text
ls: '/dev/robot_*'에 접근할 수 없습니다: 그런 파일이나 디렉터리가 없습니다
```

초기에는 성공했던 규칙이 재연결 후 동작하지 않았다.

단순히 규칙을 다시 작성하는 대신 **왜 매칭되지 않는지**를 확인하기 위해 속성을 다시 비교했다.

---

# 9. 동일한 IMU의 재연결 전·후 비교

| 속성 | 해제 전 IMU | 재연결 후 IMU | 변화 |
|---|---:|---:|---|
| `KERNEL` | `loop18` | `loop17` | ⚠️ 변경 |
| `ATTR{diskseq}` | `41` | `44` | ⚠️ 변경 |
| `ATTR{stat}` | `68 0 1344 1 ...` | `215 0 4060 2 ...` | ⚠️ 변경 |
| `SUBSYSTEM` | `block` | `block` | 동일 |
| `DRIVER` | `""` | `""` | 동일 |
| `ATTR{size}` | `20480` | `20480` | 동일 |
| `ATTR{removable}` | `0` | `0` | 동일 |
| `ATTR{ro}` | `0` | `0` | 동일 |
| `ATTR{loop/autoclear}` | `0` | `0` | 동일 |
| `ATTR{loop/dio}` | `0` | `0` | 동일 |
| `ATTR{loop/offset}` | `0` | `0` | 동일 |
| `ATTR{loop/partscan}` | `0` | `0` | 동일 |
| `ATTR{queue/rotational}` | `0` | `0` | 동일 |
| `ATTR{queue/logical_block_size}` | `512` | `512` | 동일 |
| `ATTR{queue/physical_block_size}` | `512` | `512` | 동일 |
| `ATTR{queue/scheduler}` | `[none] mq-deadline` | `[none] mq-deadline` | 동일 |
| `ATTR{zoned}` | `none` | `none` | 동일 |

가장 중요한 변화는:

```text
loop18 → loop17
diskseq 41 → 44
```

였다.

따라서:

```udev
ATTR{diskseq}=="41"
```

은 재연결 후 동일한 IMU를 더 이상 매칭할 수 없다.

---

# 10. 재연결 후 IMU와 LiDAR 비교

재연결 후에는 다음과 같이 두 센서가 구별되었다.

| 항목 | 재연결 후 IMU `loop17` | 재연결 후 LiDAR `loop18` | 차이 |
|---|---|---|---|
| `KERNEL` | `loop17` | `loop18` | ⚠️ 다름 |
| `ATTR{diskseq}` | `44` | `41` | ⚠️ 다름 |
| `ATTR{stat}` | `215 0 4060 2 ...` | `68 0 1344 1 ...` | ⚠️ 다름 |
| `SUBSYSTEM` | `block` | `block` | 동일 |
| `DRIVER` | `""` | `""` | 동일 |
| `ATTR{size}` | `20480` | `20480` | 동일 |
| `ATTR{removable}` | `0` | `0` | 동일 |
| `ATTR{ro}` | `0` | `0` | 동일 |
| `ATTR{loop/autoclear}` | `0` | `0` | 동일 |
| `ATTR{loop/dio}` | `0` | `0` | 동일 |
| `ATTR{loop/offset}` | `0` | `0` | 동일 |
| `ATTR{loop/partscan}` | `0` | `0` | 동일 |
| `ATTR{queue/rotational}` | `0` | `0` | 동일 |
| `ATTR{queue/logical_block_size}` | `512` | `512` | 동일 |
| `ATTR{queue/physical_block_size}` | `512` | `512` | 동일 |
| `ATTR{queue/scheduler}` | `[none] mq-deadline` | `[none] mq-deadline` | 동일 |
| `ATTR{zoned}` | `none` | `none` | 동일 |

현재 연결 상태에서는 `KERNEL`, `diskseq`, `stat`으로 두 장치가 구별된다.

그러나 동일 IMU를 재연결했을 때 이 값들이 변경되었기 때문에 안정적인 식별자로 사용할 수 없다.

---

# 11. `stat`도 식별자로 쓰면 안 되는 이유

`stat` 역시 두 센서에서 차이가 났지만 동일한 IMU의 재연결 전후에도 변경되었다.

```text
68 0 1344 1 ...
        ↓
215 0 4060 2 ...
```

따라서:

> **서로 다른 값이라고 해서 장치 고유 식별 정보인 것은 아니다.**

현재 상태나 I/O 통계에 따라 변할 수 있는 값은 장치 식별자로 사용하면 안 된다.

---

# 12. 이번 실습의 가장 중요한 결론

> **현재 두 장치를 구별할 수 있는 값과 재연결 후에도 같은 장치를 식별할 수 있는 값은 다르다.**
>
> `KERNEL`, `diskseq`, `stat`은 현재 상태에서는 IMU와 LiDAR를 구별할 수 있었지만 동일 장치를 해제하고 재연결했을 때 값이 변경되었다.
>
> 따라서 단순히 `udevadm info --attribute-walk /dev/loopN`에서 서로 다른 값을 하나 선택하는 것만으로는 부족하며, **재연결 후에도 유지되는 장치 고유 식별 정보를 찾아야 한다.**

---

# 13. udev 규칙 문법에서 배운 것

작성한 규칙:

```udev
ATTR{diskseq}=="39", SYMLINK+="robot_lidar"
ATTR{diskseq}=="41", SYMLINK+="robot_imu"
```

| 문법 | 의미 |
|---|---|
| `ATTR{...}` | 장치의 sysfs 속성을 조건으로 사용 |
| `==` | 조건을 비교하고 매칭 |
| `=` | 값을 설정 |
| `+=` | 기존 값에 값을 추가 |
| `SYMLINK+=` | 장치에 추가적인 심볼릭 링크 이름을 부여 |

한 문장으로:

> **`==`는 조건을 비교·매칭하고, `=`는 값을 설정하며, `+=`는 기존 값에 새로운 값을 추가한다.**

---

# 14. 실제로 고민하고 고생한 부분에서 배운 것

## SSH

- localhost라고 해서 일반적인 로컬 명령과 같은 것은 아니다.
- SSH 세션은 `exit`로 종료한다.
- `deactivate`는 SSH 종료 명령이 아니다.
- 인증 실패 시 비밀번호만 의심하지 말고 사용자 이름도 확인한다.

## udev

- `loop17`, `loop18`은 영구적인 센서 이름이 아니다.
- 현재 장치와 재연결된 장치를 같은 것으로 취급하려면 식별자의 안정성을 검증해야 한다.
- 첫 번째 규칙 테스트가 성공했다고 해서 끝난 것이 아니다.
- **해제 → 재연결 → 연결 순서 변경**까지 테스트해야 실제로 안정적인 규칙인지 알 수 있다.
- 실패한 실험도 중요한 학습 결과다.

---

# 15. ROS2 로봇에서 왜 중요한가

실제 로봇에서는 대략 다음 흐름으로 센서 데이터가 올라온다.

```text
물리 센서
   ↓
Linux 장치
   ↓
udev / 안정적인 장치 경로
   ↓
센서 드라이버
   ↓
ROS2 Node
   ↓
ROS2 Topic
   ↓
Localization / SLAM / Navigation
```

예를 들어:

```text
LiDAR
  ↓
/dev/robot_lidar
  ↓
LiDAR driver
  ↓
/scan
  ↓
SLAM / Navigation

IMU
  ↓
/dev/robot_imu
  ↓
IMU driver
  ↓
/imu/data
  ↓
Localization / EKF
```

센서 경로가 재연결 때 뒤집히면 ROS2 드라이버가 잘못된 장치를 열거나 장치를 찾지 못할 수 있다.

따라서 **ROS2 문제처럼 보여도 실제 원인은 Linux 장치 경로일 수 있다.**

---

# 16. ROS2 센서 문제를 디버깅하는 계층적 순서

센서 데이터가 나오지 않을 때 바로 ROS2 노드부터 확인하지 않는다.

```text
① 물리 장치 연결
        ↓
② /dev 장치 생성
        ↓
③ udev 규칙 / 장치 경로
        ↓
④ 센서 드라이버
        ↓
⑤ ROS2 node
        ↓
⑥ ROS2 topic
        ↓
⑦ TF
        ↓
⑧ RViz2 / SLAM / Navigation
```

예:

```bash
ls -l /dev/robot_lidar
```

↓

```bash
ros2 node list
```

↓

```bash
ros2 topic list
```

↓

```bash
ros2 topic hz /scan
```

처럼 **Linux 장치 계층부터 ROS2 데이터 계층으로 올라가며 문제를 좁힌다.**

---

# 17. 이번 실습의 미해결 부분

이번 가상 loop 장치 환경에서는 `udevadm info --attribute-walk /dev/loopN`에서 확인되는 속성만으로 재연결 후에도 유지되는 IMU/LiDAR의 고유 식별자를 찾지 못했다.

따라서 최종 결과는:

```text
diskseq 기반 규칙
        ↓
초기 연결 성공
        ↓
재연결
        ↓
고정 이름 생성 실패
        ↓
동일 IMU의 속성 비교
        ↓
KERNEL / diskseq / stat 변경 확인
        ↓
현재 속성만으로는 안정적인 식별 불가
```

이다.

이것은 단순한 실패가 아니라 **왜 해당 식별 기준이 부적합한지를 실제 재연결 실험으로 검증한 결과**이다.

실제 USB 센서에서는 제조사, 제품 정보, 시리얼 번호 등 재연결 후에도 유지되는 식별 정보가 udev에 노출되는지 먼저 확인하는 것이 중요하다.

---

# 18. 앞으로 센서 udev 작업을 할 때 기억할 체크리스트

```text
[ ] 장치 연결 상태 확인
[ ] /dev 장치 경로 확인
[ ] udevadm info --attribute-walk로 속성 조사
[ ] IMU/LiDAR 사이에서 다른 속성 확인
[ ] 그 속성이 재연결 후에도 동일한지 확인
[ ] 안정적인 식별 속성으로 udev rule 작성
[ ] udev 규칙 reload
[ ] 장치 재연결
[ ] /dev/robot_* 확인
[ ] 심볼릭 링크가 올바른 장치를 가리키는지 확인
[ ] 연결 순서를 바꿔 다시 검증
[ ] ROS2 driver에서 안정적인 경로 사용
[ ] ros2 node / topic / topic hz로 최종 데이터 확인
```

---

# 19. 핵심 명령어 치트시트

```bash
# SSH 원격 단일 명령
ssh 사용자@서버 'uname -a'

# SSH 세션 종료
exit

# SCP 파일 전송
scp ~/파일 사용자@서버:~/대상폴더/

# udev 장치 속성 확인
udevadm info --attribute-walk /dev/loopN

# udev 규칙 확인
cat /etc/udev/rules.d/99-robot-sensor.rules

# udev 규칙 다시 읽기
sudo udevadm control --reload-rules

# 심볼릭 링크 확인
ls -l /dev/robot_*

# ROS2 노드 확인
ros2 node list

# ROS2 토픽 확인
ros2 topic list

# 센서 토픽 주기 확인
ros2 topic hz /scan
```

---

## 최종 한 줄

> **센서 운용에서 중요한 것은 "장치가 지금 어디에 연결되어 있는가"가 아니라 "장치가 다시 연결되어도 내가 원하는 센서를 확실하게 찾아낼 수 있는가"이다.**
