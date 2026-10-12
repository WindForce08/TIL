# RealSense Tracker — Phase 1 작업 기록

## 1. Phase 1 목표

Phase 1의 목표는 **Raspberry Pi 4에서 OpenCR 펌웨어를 직접 빌드하고, USB를 통해 OpenCR 1.0에 업로드하여 실행할 수 있는 환경을 구축하는 것**이다.

최종적으로 다음 흐름을 검증했다.

```text
Raspberry Pi 4
Ubuntu 26.04 LTS Server ARM64
        │
        ├── ROS 2 Lyrical
        ├── Arduino CLI
        ├── ARM64 GCC Cross Compiler
        └── opencr_ld
                │
                │ USB /dev/ttyACM0
                ▼
             OpenCR 1.0
                │
                ├── Flash Erase
                ├── Flash Write
                ├── CRC Verify
                └── Firmware Execute
```

---

## 2. 개발 환경

| 항목 | 환경 / 결과 |
|---|---|
| SBC | Raspberry Pi 4 |
| OS | Ubuntu 26.04 LTS Server |
| Architecture | ARM64 / aarch64 |
| ROS 2 | Lyrical |
| OpenCR | OpenCR 1.0 |
| OpenCR USB | `/dev/ttyACM0` |
| Arduino CLI | 1.5.1 |
| Python serial | pyserial 3.5 |
| ARM Cross Compiler | `gcc-arm-none-eabi` 14.2.1 |
| Binutils | `binutils-arm-none-eabi` |
| OpenCR Core | 1.5.3 |
| OpenCR Loader | `opencr_ld` 1.0.4 |

---

# 3. 진행 과정

## 3.1 ROS 2 환경 확인

Raspberry Pi에 Ubuntu 26.04 LTS Server와 ROS 2 Lyrical을 설치한 상태에서 ROS 2 기본 통신을 테스트했다.

```bash
source /opt/ros/lyrical/setup.bash
```

ROS 2 talker/listener 테스트를 수행하여 기본 ROS 2 통신이 정상 동작하는 것을 확인했다.

**결과: 완료**

---

## 3.2 Raspberry Pi ↔ OpenCR USB 연결 확인

USB 장치에서 OpenCR이 정상 인식되는 것을 확인했다.

```text
OpenCR Virtual ComPort in FS Mode
ROBOTIS
```

장치 파일:

```text
/dev/ttyACM0
```

udev 정보에서도 다음을 확인했다.

```text
ID_MODEL=OpenCR_Virtual_ComPort_in_FS_Mode
ID_VENDOR=ROBOTIS
ID_VENDOR_ID=0483
ID_MODEL_ID=5740
```

### 권한 설정

초기에는 `/dev/ttyACM0` 접근을 위해 `dialout` 그룹 권한이 필요했다.

```bash
sudo usermod -aG dialout $USER
newgrp dialout
```

이후 현재 사용자가 `dialout` 그룹에 포함된 것을 확인했다.

**결과: 완료**

---

## 3.3 Arduino CLI 설치

Arduino CLI를 공식 설치 스크립트를 이용해 설치했다.

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
```

버전 확인:

```text
arduino-cli Version: 1.5.1
```

PATH 설정:

```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**결과: 완료**

---

## 3.4 OpenCR Board Manager 확인

OpenCR 공식 Board Manager URL을 Arduino CLI에 추가했다.

```bash
arduino-cli config init

arduino-cli config add board_manager.additional_urls \
https://raw.githubusercontent.com/ROBOTIS-GIT/OpenCR/master/arduino/opencr_release/package_opencr_index.json
```

인덱스를 갱신하고 OpenCR 보드를 검색했다.

```bash
arduino-cli core update-index
arduino-cli core search OpenCR
```

OpenCR Core 1.5.3을 확인했다.

### ARM64에서 발생한 문제

일반적인 OpenCR Core 설치:

```bash
arduino-cli core install OpenCR:OpenCR
```

는 다음 오류로 실패했다.

```text
Platform 'OpenCR:OpenCR': platform is not available for your OS
```

확인 결과 ROBOTIS OpenCR 패키지에서 제공하는 기존 GCC 패키지는 Raspberry Pi ARM64 Linux용이 아니었다.

따라서 Board Manager의 자동 설치 대신 **OpenCR Core와 ARM64용 Cross Compiler를 직접 연결하는 방식**으로 구성했다.

**결과: 자동 설치 실패 원인 확인 및 수동 구성으로 해결**

---

# 4. ARM64 OpenCR 컴파일 환경 구축

## 4.1 ARM Cross Compiler 설치

Ubuntu 26.04 ARM64에서 제공하는 Cross Compiler를 확인했다.

```bash
apt-cache policy gcc-arm-none-eabi
```

설치:

```bash
sudo apt update
sudo apt install gcc-arm-none-eabi binutils-arm-none-eabi
```

버전:

```text
arm-none-eabi-gcc
14.2.1 20241119
```

Cortex-M7 대상 옵션도 정상 인식되는 것을 확인했다.

```bash
arm-none-eabi-gcc \
  -mcpu=cortex-m7 \
  -mfloat-abi=softfp \
  -mfpu=fpv5-sp-d16 \
  --version
```

**결과: 완료**

---

## 4.2 OpenCR Core 수동 설치

OpenCR 저장소에서 Core를 가져와 Arduino CLI의 패키지 경로에 배치했다.

```bash
mkdir -p ~/.arduino15/packages/OpenCR/hardware/OpenCR/1.5.3

cp -a arduino/opencr_arduino/opencr/. \
  ~/.arduino15/packages/OpenCR/hardware/OpenCR/1.5.3/
```

Arduino CLI에서 OpenCR Core를 확인했다.

```bash
arduino-cli core list
```

결과:

```text
OpenCR:OpenCR 1.5.3
```

---

## 4.3 ARM64 Toolchain 연결

OpenCR Core의 `platform.txt`가 기대하는 경로에 ARM64 시스템 Cross Compiler를 연결했다.

```bash
mkdir -p ~/.arduino15/packages/OpenCR/tools/opencr_gcc/5.4.0-2016q2/bin

ln -sf "$(which arm-none-eabi-gcc)" \
  ~/.arduino15/packages/OpenCR/tools/opencr_gcc/5.4.0-2016q2/bin/arm-none-eabi-gcc

ln -sf "$(which arm-none-eabi-g++)" \
  ~/.arduino15/packages/OpenCR/tools/opencr_gcc/5.4.0-2016q2/bin/arm-none-eabi-g++

ln -sf "$(which arm-none-eabi-ar)" \
  ~/.arduino15/packages/OpenCR/tools/opencr_gcc/5.4.0-2016q2/bin/arm-none-eabi-ar

ln -sf "$(which arm-none-eabi-objcopy)" \
  ~/.arduino15/packages/OpenCR/tools/opencr_gcc/5.4.0-2016q2/bin/arm-none-eabi-objcopy
```

이 구성을 통해 Raspberry Pi ARM64에서 OpenCR용 Cortex-M 펌웨어를 직접 빌드할 수 있도록 했다.

---

# 5. OpenCR 펌웨어 컴파일 테스트

테스트 스케치를 작성했다.

```cpp
void setup()
{
}

void loop()
{
}
```

빌드:

```bash
arduino-cli compile \
  --fqbn OpenCR:OpenCR:OpenCR \
  ~/opencr_test
```

초기에는 프로그램 크기 계산 단계에서 다음 메시지가 발생했다.

```text
Couldn't determine program size
```

하지만 실제 컴파일/링크와 `.bin` 생성은 정상적으로 완료되었다.

Verbose 로그에서:

```text
arm-none-eabi-g++
```

를 이용한 컴파일 및 링크가 수행되었고,

```text
arm-none-eabi-objcopy -O binary
```

를 이용해 `.bin` 파일이 생성된 것을 확인했다.

프로그램 크기 계산 단계에서 `arm-none-eabi-size`가 필요한 상태였으나, **실제 펌웨어 생성에는 영향을 주지 않았다.**

---

# 6. 생성된 펌웨어 검증

생성된 파일:

```text
opencr_test.ino.bin   66K
opencr_test.ino.elf   1.1M
opencr_test.ino.map   1.1M
```

`.bin` 파일:

```bash
file \
/home/pa31/.cache/arduino/sketches/EBC1FFC9AE275B1EBC20E58DF71D3E6E/opencr_test.ino.bin
```

결과:

```text
ARM Cortex-M firmware,
initial SP at 0x2004ffff,
reset at 0x080477a4,
...
```

즉 Raspberry Pi에서 생성한 `.bin`이 **OpenCR의 Cortex-M 계열에서 실행 가능한 펌웨어 이미지**임을 확인했다.

**결과: 완료**

---

# 7. OpenCR Loader(`opencr_ld`) 빌드

OpenCR 저장소의 loader 소스:

```text
~/OpenCR/arduino/opencr_develop/opencr_ld/
```

Makefile을 확인했다.

```makefile
all: clean opencr_ld

SRCS  = main.c
SRCS += opencr_ld.c
SRCS += serial_posix.c
SRCS += ./msg/msg.c

opencr_ld:
        gcc -o opencr_ld $(SRCS)
```

Raspberry Pi에서 빌드:

```bash
make
```

생성된 실행 파일:

```text
opencr_ld  75K
```

파일 타입:

```text
ELF 64-bit LSB pie executable, ARM aarch64
```

따라서 `opencr_ld` 역시 **Raspberry Pi 4 ARM64에서 직접 실행 가능한 업로더**임을 확인했다.

버전 및 사용법:

```text
opencr_ld ver 1.0.4

Usage:
opencl_ld <port> <baud> <binary image name>
[<0|1 to send Go command to new flashed app>]
```

**결과: 완료**

---

# 8. OpenCR Flash 업로드

펌웨어 경로:

```text
/home/pa31/.cache/arduino/sketches/EBC1FFC9AE275B1EBC20E58DF71D3E6E/opencr_test.ino.bin
```

OpenCR 장치:

```text
/dev/ttyACM0
```

`opencr_ld` 소스에서 다운로드 단계의 실제 통신 속도가 `115200`임을 확인했다.

업로드 명령:

```bash
./opencr_ld \
  /dev/ttyACM0 \
  115200 \
  "$BIN" \
  1
```

실제 결과:

```text
opencr_ld ver 1.0.4
opencr_ld_main

file name : .../opencr_test.ino.bin
file size : 65 KB

Open port OK
Clear Buffer Start
Clear Buffer End

Board Name : OpenCR R1.0
Board Ver  : 0x17020800
Board Rev  : 0x00000000

flash_erase : 0 : 0.952000 sec
flash_write : 0 : 0.980000 sec

CRC OK 685D1A 685D1A 0.002000 sec

[OK] Download
jump_to_fw
jump finished
```

## 업로드 결과 해석

### OpenCR 인식

```text
Board Name : OpenCR R1.0
```

→ Raspberry Pi에서 OpenCR 보드 정보를 정상적으로 읽음.

### Flash Erase

```text
flash_erase : 0
```

→ Flash 삭제 성공.

### Flash Write

```text
flash_write : 0
```

→ 펌웨어 기록 성공.

### CRC 검증

```text
CRC OK 685D1A 685D1A
```

→ 전송된 펌웨어와 OpenCR에서 확인한 CRC가 일치함.

### Firmware 실행

```text
[OK] Download
jump_to_fw
jump finished
```

→ 다운로드 성공 후 새 펌웨어로 실행 전환까지 완료.

**결과: 실제 OpenCR Flash 업로드 및 CRC 검증 성공**

---

# 9. Phase 1 최종 상태

| 항목 | 상태 |
|---|---:|
| Ubuntu 26.04 LTS Server ARM64 | ✅ |
| ROS 2 Lyrical | ✅ |
| ROS 2 기본 통신 테스트 | ✅ |
| OpenCR USB 연결 | ✅ |
| `/dev/ttyACM0` 확인 | ✅ |
| `dialout` 권한 | ✅ |
| pyserial 3.5 | ✅ |
| Arduino CLI 1.5.1 | ✅ |
| OpenCR Core 1.5.3 | ✅ |
| ARM64 `gcc-arm-none-eabi` | ✅ |
| OpenCR 펌웨어 컴파일 | ✅ |
| `.bin` 생성 | ✅ |
| Cortex-M Firmware 검증 | ✅ |
| `opencr_ld` ARM64 빌드 | ✅ |
| OpenCR Flash Erase | ✅ |
| OpenCR Flash Write | ✅ |
| CRC 검증 | ✅ |
| Firmware `jump_to_fw` | ✅ |

## Phase 1 판정

**환경 구축 및 OpenCR 펌웨어 업로드까지 성공.**

현재 Raspberry Pi에서 다음 작업이 모두 가능하다.

```text
OpenCR 소스/스케치
        ↓
Arduino CLI
        ↓
ARM64 Cross Compiler
        ↓
OpenCR .bin
        ↓
opencr_ld
        ↓
USB /dev/ttyACM0
        ↓
OpenCR 1.0 Flash
        ↓
CRC 검증
        ↓
Firmware 실행
```

---

# 10. Phase 1에서 남은 선택적 확인

현재 펌웨어는 다음과 같은 빈 테스트 프로그램이다.

```cpp
void setup()
{
}

void loop()
{
}
```

따라서 **Flash 업로드 자체는 검증했지만, 애플리케이션 레벨의 Serial 출력/동작은 아직 검증하지 않았다.**

필요하다면 다음 단계에서 Serial 출력 또는 LED 동작을 포함한 테스트 펌웨어로 추가 확인할 수 있다.

---

# 11. 다음 단계 — Phase 2

Phase 1 이후에는 **OpenCR ↔ Dynamixel ×2 제어**로 진행한다.

예정 작업:

1. Dynamixel 연결 상태 확인
2. Dynamixel ID 확인
3. Baudrate 확인
4. Dynamixel Ping
5. 현재 Position 읽기
6. 단일 모터 Position 명령
7. Dynamixel 2개 동시 제어
8. OpenCR에서 모터 제어 펌웨어 구성
9. Raspberry Pi ↔ OpenCR ↔ Dynamixel 전체 경로 확인

최종 목표:

```text
Raspberry Pi
     │
     │ USB / Serial
     ▼
  OpenCR 1.0
     │
     ├──── Dynamixel #1
     │
     └──── Dynamixel #2
```

Phase 2가 정상적으로 완료되면 이후 ROS 2 Integration 단계에서 `integration_node → opencr_node → Dynamixel` 구조를 연결한다.

---

## 결론

**Phase 1은 핵심 목표를 달성했다.**

> Raspberry Pi 4 + Ubuntu 26.04 ARM64 환경에서 OpenCR용 펌웨어를 직접 컴파일하고, `opencr_ld`를 이용해 `/dev/ttyACM0`으로 OpenCR 1.0에 업로드한 뒤 CRC 검증과 `jump_to_fw`까지 성공했다.

다음 작업은 **Phase 2 — Dynamixel ×2 제어 검증**이다.
