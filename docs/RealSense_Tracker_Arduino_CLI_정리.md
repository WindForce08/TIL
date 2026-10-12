# RealSense Tracker — Arduino CLI 이해 정리

## 1. Arduino CLI란?

**Arduino CLI(Command Line Interface)**는 Arduino 개발 환경에서 GUI로 수행하던 작업을 터미널 명령어로 수행할 수 있게 해주는 도구다.

쉽게 말하면:

> Arduino IDE에서 버튼으로 하던 보드 선택, 컴파일, 라이브러리/보드 관리 등의 작업을 CLI 명령어로 수행하게 해주는 프로그램.

예:

```bash
arduino-cli compile ...
arduino-cli board list
arduino-cli core list
arduino-cli lib install ...
```

---

## 2. 이번 프로젝트에서 Arduino CLI가 필요한 이유

현재 프로젝트는 일반적인 PC + Arduino IDE 환경이 아니라 다음 구조다.

```text
Raspberry Pi 4
Ubuntu 26.04 LTS ARM64
       │
       ├── ROS 2 Lyrical
       ├── Camera
       ├── OpenCR
       └── Dynamixel ×2
```

프로젝트 목표 중 하나는 **Raspberry Pi 자체에서 OpenCR 펌웨어를 빌드하고 OpenCR에 업로드하는 것**이다.

따라서 다음 구조가 필요하다.

```text
Raspberry Pi
    ↓
Arduino CLI
    ↓
OpenCR Core
    ↓
ARM Cross Compiler
    ↓
OpenCR firmware (.bin)
```

Arduino CLI는 이 빌드 과정을 관리하는 **빌드 진입점/관리 도구** 역할을 한다.

---

# 3. Arduino CLI가 직접 컴파일러인가?

아니다.

Arduino CLI는 실제 ARM 코드를 직접 컴파일하는 컴파일러라기보다 **빌드 과정을 지휘하는 도구**에 가깝다.

각 구성요소의 역할은 다음과 같다.

| 구성요소 | 역할 |
|---|---|
| Arduino CLI | 빌드 과정 관리 |
| OpenCR Core | OpenCR용 보드 설정 및 빌드 규칙 제공 |
| `arm-none-eabi-gcc` | ARM Cortex-M 코드 컴파일 |
| `arm-none-eabi-g++` | C++ 코드 컴파일/링크 |
| `arm-none-eabi-objcopy` | ELF → BIN 변환 |
| `opencr_ld` | 생성된 BIN을 OpenCR에 업로드 |

구조:

```text
                Arduino CLI
                     │
              "OpenCR로 빌드"
                     │
                     ▼
               OpenCR Core
                     │
             빌드 설정 제공
                     │
                     ▼
             ARM GNU Toolchain
                     │
               실제 컴파일
                     │
                     ▼
              .elf / .bin
```

---

# 4. OpenCR Core란?

OpenCR은 일반적인 Arduino Uno와 같은 보드가 아니기 때문에 OpenCR에 맞는 빌드 정보가 필요하다.

OpenCR Core에는 다음과 같은 정보가 포함된다.

- 보드 설정
- CPU 설정
- 컴파일 옵션
- Arduino API
- 라이브러리
- 링커 설정
- OpenCR 관련 빌드 설정

즉,

> **OpenCR Core = Arduino 코드를 OpenCR용 펌웨어로 만드는 방법을 정의한 패키지**

라고 이해하면 된다.

이번 프로젝트에서는 OpenCR Core 1.5.3을 사용했다.

```bash
arduino-cli core list
```

결과:

```text
OpenCR:OpenCR 1.5.3
```

---

# 5. 실제 빌드 명령

이번 Phase 1에서 사용한 핵심 명령은 다음과 같다.

```bash
arduino-cli compile \
  --fqbn OpenCR:OpenCR:OpenCR \
  ~/opencr_test
```

의미:

```text
arduino-cli
    ↓
compile
    ↓
OpenCR:OpenCR:OpenCR
    ↓
~/opencr_test
```

즉,

> `~/opencr_test` 프로젝트를 OpenCR 보드용 펌웨어로 컴파일하라.

는 의미다.

전체 과정:

```text
opencr_test.ino
       ↓
Arduino CLI
       ↓
OpenCR Core
       ↓
arm-none-eabi-gcc
       ↓
opencr_test.ino.elf
       ↓
arm-none-eabi-objcopy
       ↓
opencr_test.ino.bin
```

---

# 6. `opencr_ld`와 Arduino CLI의 차이

두 도구의 역할은 명확하게 다르다.

### Arduino CLI

```text
소스 코드
   ↓
컴파일
   ↓
.bin
```

### opencr_ld

```text
.bin
 ↓
USB
 ↓
OpenCR Flash
```

전체 구조:

```text
[빌드 단계]

Arduino 코드
     ↓
Arduino CLI
     ↓
OpenCR Core
     ↓
ARM GCC
     ↓
firmware.bin
     │
     ▼
[업로드 단계]

opencr_ld
     ↓
/dev/ttyACM0
     ↓
OpenCR
```

따라서 Arduino CLI와 `opencr_ld`는 서로 대체 관계가 아니다.

- Arduino CLI → **만드는 역할**
- opencr_ld → **넣는 역할**

---

# 7. 왜 Raspberry Pi ARM64에서 수동 구성이 필요했는가?

일반적인 OpenCR Board Manager 설치:

```bash
arduino-cli core install OpenCR:OpenCR
```

는 다음 오류가 발생했다.

```text
Platform 'OpenCR:OpenCR': platform is not available for your OS
```

원인은 ROBOTIS에서 제공하는 기존 OpenCR GCC 패키지가 Raspberry Pi ARM64 Linux용으로 제공되지 않았기 때문이다.

따라서 다음과 같이 구성했다.

```text
Ubuntu 26.04 ARM64
        │
        ▼
gcc-arm-none-eabi
        │
        ▼
ARM Cortex-M Cross Compiler
```

그리고 OpenCR Core가 기대하는 경로에 ARM64 시스템 Cross Compiler를 연결했다.

결과적으로:

```text
Raspberry Pi ARM64
       │
       ▼
Arduino CLI
       │
       ▼
OpenCR Core
       │
       ▼
ARM64에서 실행되는 GCC
       │
       ▼
OpenCR Cortex-M Firmware
```

구조를 만들었다.

---

# 8. 이번 Phase 1에서 실제로 확인한 것

### 환경

```text
Raspberry Pi 4
Ubuntu 26.04 LTS ARM64
ROS 2 Lyrical
```

### Arduino CLI

```text
Arduino CLI 1.5.1
```

### OpenCR Core

```text
OpenCR Core 1.5.3
```

### Cross Compiler

```text
arm-none-eabi-gcc 14.2.1
```

### 결과

Raspberry Pi에서 직접 OpenCR 펌웨어를 빌드했다.

```text
opencr_test.ino.bin
66K
```

그리고:

```text
ARM Cortex-M firmware
```

로 정상 인식되는 것을 확인했다.

이후 `opencr_ld`를 Raspberry Pi ARM64에서 빌드하고:

```bash
./opencr_ld /dev/ttyACM0 115200 "$BIN" 1
```

실제 OpenCR에 업로드했다.

결과:

```text
[OK] Download
CRC OK
jump_to_fw
jump finished
```

즉:

> **Raspberry Pi에서 OpenCR 펌웨어를 직접 빌드하고 OpenCR에 실제 플래싱하는 전체 과정이 성공했다.**

---

# 9. 핵심 개념 한 장 정리

```text
┌─────────────────────────────────────┐
│           Raspberry Pi 4            │
│         Ubuntu 26.04 ARM64          │
│                                     │
│  ┌───────────────────────────────┐  │
│  │        Arduino CLI            │  │
│  │      빌드 과정 관리           │  │
│  └──────────────┬────────────────┘  │
│                 ↓                   │
│        ┌─────────────────┐          │
│        │   OpenCR Core   │          │
│        │ OpenCR 빌드 설정 │          │
│        └────────┬────────┘          │
│                 ↓                   │
│        ┌─────────────────┐          │
│        │    ARM GCC      │          │
│        │ Cross Compiler  │          │
│        └────────┬────────┘          │
│                 ↓                   │
│             firmware.bin            │
│                 │                   │
│                 ▼                   │
│           ┌───────────┐             │
│           │ opencr_ld │             │
│           └─────┬─────┘             │
└─────────────────┼───────────────────┘
                  │ USB
                  ▼
             ┌──────────┐
             │  OpenCR  │
             └────┬─────┘
                  ↓
             Dynamixel ×2
```

## 한 문장 요약

> **Arduino CLI는 Raspberry Pi에서 OpenCR Core와 ARM Cross Compiler를 이용해 OpenCR 펌웨어를 빌드하도록 관리하는 도구이고, `opencr_ld`는 그렇게 만들어진 `.bin`을 실제 OpenCR에 업로드하는 도구다.**
