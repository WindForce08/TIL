> 작성일 : 2026-08-31
>
> 학습내용 : ㅇㅅㅇ


# 오늘 학습 정리 --- LV1 Module 2 / C++ · CMake · Git

> 오늘은 **문제 1**을 직접 구현하면서 C++ 파일 분리 → 수동 컴파일/링크 →
> CMake → 증분 빌드 → Git 관리까지 연결해서 학습했다.

------------------------------------------------------------------------

## 1. 오늘 진행한 전체 흐름

``` text
[문제 1]
로봇 제동거리 계산기
        ↓
stop_distance.cpp 작성
        ↓
g++ -Wall -std=c++17 빌드/실행
        ↓
Motor 클래스 분리
        ↓
motor.hpp + motor.cpp + main.cpp
        ↓
수동 2단계 빌드
        ↓
① .cpp → .o 컴파일
② .o → 실행파일 링크
        ↓
CMakeLists.txt 작성
        ↓
build/에서 cmake .. && make
        ↓
증분 빌드 확인
        ↓
.gitignore 정리
        ↓
이미 추적된 빌드 산출물 제거
```

------------------------------------------------------------------------

# 2. 문제 1 --- 제동거리 계산기

## 과제 요구사항

속도와 마찰계수를 입력받아 정지거리를 계산한다.

사용한 공식:

``` text
d = v² / (2 × μ × g)

# d : 정지거리 [m]
# v : 속도 [m/s]
# μ : 마찰계수
# g : 중력가속도 = 9.81 m/s²
```

### 최종 코드

``` cpp
#include <cstdlib>
#include <iostream>

namespace
{
    // 프로그램 전체에서 사용하는 중력가속도 상수
    constexpr double kGravity = 9.81;

    // 정지거리 계산 함수
    // d = v² / (2 * μ * g)
    double stop_distance(double speed, double mu)
    {
        return (speed * speed) / (2.0 * mu * kGravity);
    }
}

int main()
{
    // 사용자에게 입력받을 속도와 마찰계수
    double speed;
    double mu;

    std::cout << "속도(m/s)를 입력하세요: ";
    std::cin >> speed;

    std::cout << "마찰 계수를 입력하세요: ";
    std::cin >> mu;

    // 계산 결과 출력
    std::cout << "정지거리: "
              << stop_distance(speed, mu)
              << " m"
              << std::endl;

    return 0;  // 0 = 정상 종료
}
```

### 빌드 및 실행

``` bash
# 문제에서 요구한 C++17 + 경고 옵션으로 컴파일
g++ -Wall -std=c++17 stop_distance.cpp -o stop_distance

# 실행
./stop_distance
```

### 실제 테스트

``` text
속도(m/s)를 입력하세요: 54
마찰 계수를 입력하세요: 3
정지거리: 49.5413 m
```

또 다른 테스트:

``` text
속도(m/s)를 입력하세요: 654
마찰 계수를 입력하세요: 2
정지거리: 10900 m
```

### 오늘 이해한 내용

``` text
namespace
# → 이름 충돌을 막기 위한 공간
# → 내부 이름은 프로젝트 상황에 맞게 이해하기 쉬운 이름으로 작성 가능

constexpr
# → 컴파일 시점에 결정되는 상수

main()
# → 실행파일이 실행될 때 프로그램이 시작되는 함수

std::cin
# → 사용자 입력

std::cout
# → 화면 출력
```

------------------------------------------------------------------------

# 3. `.hpp`와 `.cpp` 분리

Motor 클래스를 세 파일 구조로 분리했다.

``` text
cpp_basic/
├── motor.hpp
├── motor.cpp
└── main.cpp
```

## motor.hpp

``` cpp
#pragma once

class Motor
{
public:
    // 외부에서 사용할 수 있는 기능
    void setSpeed(double mps);

private:
    // Motor 내부에서만 관리하는 데이터
    double current_speed_ = 0.0;
};
```

## motor.cpp

``` cpp
#include "motor.hpp"

// motor.hpp에서 선언한 함수의 실제 구현
void Motor::setSpeed(double mps)
{
    current_speed_ = mps;
}
```

## 구조 이해

``` text
motor.hpp
    ↓
# "Motor라는 클래스가 있고,
#  setSpeed()라는 기능을 제공한다."

motor.cpp
    ↓
# "setSpeed()를 실제로 어떻게 동작시킬지 구현한다."
```

------------------------------------------------------------------------

# 4. `public`과 `private`

``` cpp
class Motor
{
public:
    // 클래스 외부에서 접근할 수 있음
    void setSpeed(double mps);

private:
    // 클래스 내부에서만 직접 접근할 수 있음
    double current_speed_ = 0.0;
};
```

사용자는 `setSpeed()`를 통해 Motor를 제어한다.

``` cpp
Motor motor;

// public 함수이므로 외부에서 호출 가능
motor.setSpeed(5.0);

// private 데이터이므로 직접 접근하면 안 됨
// motor.current_speed_ = 5.0;  // 오류
```

핵심 구조:

``` text
외부
 ↓
setSpeed()             # public: 외부에 공개된 인터페이스
 ↓
current_speed_         # private: 클래스 내부 데이터
```

------------------------------------------------------------------------

# 5. `.hpp`를 직접 컴파일하면서 발생한 경고

처음에 다음 명령을 실행했다.

``` bash
g++ -c motor.hpp -o motor.o

# 경고:
# warning: #pragma once in main file
```

### 왜 발생했는가?

``` text
.hpp
# → 보통 선언을 담는 헤더 파일
# → .cpp에서 #include하여 사용

.cpp
# → 실제 컴파일 대상
```

따라서 다음처럼 하는 것이 올바르다.

``` bash
# 잘못된 접근
g++ -c motor.hpp -o motor.o

# 올바른 접근
g++ -c motor.cpp -o motor.o
```

------------------------------------------------------------------------

# 6. 수동 2단계 빌드

이번 실습에서 가장 중요한 부분 중 하나다.

## 1단계 --- 컴파일

``` bash
# main.cpp를 컴파일해서 main.o 생성
g++ -Wall -Wextra -O2 -std=c++17 -c main.cpp -o main.o

# motor.cpp를 컴파일해서 motor.o 생성
g++ -Wall -Wextra -O2 -std=c++17 -c motor.cpp -o motor.o
```

결과:

``` text
main.cpp  ──컴파일──→ main.o
motor.cpp ──컴파일──→ motor.o
```

여기서 `-c`의 의미:

``` text
-c
# → compile only
# → 컴파일만 수행
# → 링크는 하지 않음
```

## 2단계 --- 링크

``` bash
# 여러 .o 파일을 하나의 실행파일로 연결
g++ main.o motor.o -o robot
```

전체 흐름:

``` text
main.cpp ──compile──→ main.o ──┐
                               │
                               ├──link──→ robot
                               │
motor.cpp ─compile──→ motor.o ─┘
```

------------------------------------------------------------------------

# 7. `main()` 링크 오류를 직접 경험

다음 명령을 실행했을 때 오류가 발생했다.

``` bash
# -c가 없기 때문에 컴파일 후 링크까지 수행하려고 함
g++ -Wall -Wextra -O2 -std=c++17 motor.cpp -o motor.o
```

오류:

``` text
undefined reference to `main'
```

### 원인

``` text
-c가 없음
    ↓
컴파일 + 링크를 시도
    ↓
실행파일을 만들려고 함
    ↓
그런데 motor.cpp에는 main()이 없음
    ↓
undefined reference to main
```

올바른 명령:

``` bash
# motor.cpp는 객체 파일만 만들면 되므로 -c 사용
g++ -Wall -Wextra -O2 -std=c++17 -c motor.cpp -o motor.o
```

### 반드시 기억할 차이

``` bash
# 컴파일만
g++ -c motor.cpp -o motor.o

# 링크
g++ main.o motor.o -o robot
```

------------------------------------------------------------------------

# 8. `robot`은 무엇을 실행하는가?

링크가 끝나면:

``` bash
g++ main.o motor.o -o robot
```

하나의 실행파일 `robot`이 만들어진다.

실행:

``` bash
./robot
```

중요:

``` text
main.o를 실행하는 것 아님
motor.o를 실행하는 것 아님

main.o + motor.o
       ↓
    링크
       ↓
     robot
       ↓
     ./robot
       ↓
    main()부터 시작
```

프로그램 흐름:

``` text
./robot
   ↓
main()
   ↓
Motor motor;
   ↓
motor.setSpeed(...)
   ↓
Motor::setSpeed()
   ↓
current_speed_ 변경
```

------------------------------------------------------------------------

# 9. CMake

## 처음 사용한 강의 자료 구조

강의 자료는 다음 구조였다.

``` text
src/main.cpp
src/motor.cpp
include/...
```

따라서 예제에는:

``` cmake
add_executable(robot
    src/main.cpp
    src/motor.cpp
)
```

가 있었다.

하지만 현재 프로젝트는:

``` text
cpp_basic/
├── main.cpp
├── motor.cpp
├── motor.hpp
├── stop_distance.cpp
└── CMakeLists.txt
```

이므로 경로를 현재 구조에 맞게 수정했다.

## 최종 CMakeLists.txt

``` cmake
cmake_minimum_required(VERSION 3.16)

project(robot_controller CXX)

# C++17 사용
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# main.cpp + motor.cpp → robot 실행파일
add_executable(robot
    main.cpp
    motor.cpp
)

# stop_distance.cpp → stop_distance 실행파일
add_executable(stop_distance
    stop_distance.cpp
)
```

------------------------------------------------------------------------

# 10. `cmake ..` 경로 오류

처음 `cpp_basic/`에서:

``` bash
cmake ..
```

를 실행했다.

오류:

``` text
The source directory
"/home/pa31/KantPA/lv1_module2_sangjun"
does not appear to contain CMakeLists.txt.
```

### 원인

현재 위치:

``` text
cpp_basic/
```

여기서 `..`은:

``` text
lv1_module2_sangjun/
```

을 의미한다.

하지만 `CMakeLists.txt`는:

``` text
cpp_basic/CMakeLists.txt
```

에 있었다.

따라서 `build/`를 만들고 그 안에서 실행해야 한다.

------------------------------------------------------------------------

# 11. 올바른 CMake 빌드 구조

``` text
cpp_basic/
├── CMakeLists.txt
├── main.cpp
├── motor.cpp
├── motor.hpp
├── stop_distance.cpp
└── build/
```

명령:

``` bash
# cpp_basic에서 build 디렉터리 생성
mkdir build

# build로 이동
cd build

# .. = 부모 디렉터리인 cpp_basic/
# → 여기서 CMakeLists.txt를 찾음
cmake ..

# CMake가 생성한 빌드 설정으로 실제 컴파일/링크
make
```

------------------------------------------------------------------------

# 12. CMake 빌드 성공 출력

실제 확인한 출력:

``` text
-- Configuring done
-- Generating done
-- Build files have been written to:
/home/pa31/KantPA/lv1_module2_sangjun/cpp_basic/build

[ 20%] Building CXX object CMakeFiles/robot.dir/main.cpp.o
[ 40%] Building CXX object CMakeFiles/robot.dir/motor.cpp.o
[ 60%] Linking CXX executable robot
[ 60%] Built target robot

[ 80%] Building CXX object CMakeFiles/stop_distance.dir/stop_distance.cpp.o
[100%] Linking CXX executable stop_distance
[100%] Built target stop_distance
```

출력을 읽으면:

``` text
main.cpp + motor.cpp
        ↓
      compile
        ↓
      link
        ↓
      robot

stop_distance.cpp
        ↓
      compile
        ↓
      link
        ↓
  stop_distance
```

------------------------------------------------------------------------

# 13. 증분 빌드

`motor.cpp`만 수정하고 다시 `make`했다.

``` bash
# motor.cpp 수정 후
make
```

실제 출력:

``` text
Consolidate compiler generated dependencies of target robot
[ 20%] Building CXX object CMakeFiles/robot.dir/motor.cpp.o
[ 40%] Linking CXX executable robot
[ 60%] Built target robot

Consolidate compiler generated dependencies of target stop_distance
[100%] Built target stop_distance
```

### 결과 분석

``` text
main.cpp
# → 변경 없음
# → 다시 컴파일하지 않음

motor.cpp
# → 변경됨
# → motor.cpp.o만 다시 컴파일

stop_distance.cpp
# → 변경 없음
# → 다시 컴파일하지 않음

motor.cpp.o 변경
# → robot 실행파일은 motor.o를 포함하므로 다시 링크
```

즉:

``` text
motor.cpp
   ↓
motor.cpp.o 재컴파일
   ↓
robot 재링크
```

------------------------------------------------------------------------

# 14. 증분 빌드란?

증분 빌드(Incremental Build)는 매번 전체 프로젝트를 처음부터 빌드하지
않고 **변경된 파일과 그 의존성을 기준으로 필요한 부분만 다시 빌드하는
방식**이다.

``` text
전체 빌드

main.cpp ───────→ main.o ──┐
motor.cpp ──────→ motor.o ─┼──→ robot
stop_distance.cpp → ... ───┘


증분 빌드

motor.cpp만 변경
      ↓
motor.cpp → motor.o만 재컴파일
      ↓
robot만 다시 링크

main.cpp
# → 변경되지 않았으므로 기존 main.o 재사용

stop_distance.cpp
# → 변경되지 않았으므로 기존 결과물 재사용
```

판단에는 다음 정보가 사용된다.

``` text
# CMake/Make가 변경 여부와 의존성을 확인한다.
#
# 핵심:
# 1. 소스 파일이 변경되었는가?
# 2. 해당 소스가 의존하는 파일이 변경되었는가?
# 3. 기존 빌드 결과물이 최신 상태인가?
```

------------------------------------------------------------------------

# 15. 최종 제출 포맷

과제에서 요구하는 구조:

``` text
lv1_module2_이름.zip
├── report.md
├── cpp_basics/
│   ├── stop_distance.cpp
│   ├── motor.hpp
│   ├── motor.cpp
│   ├── main.cpp
│   ├── CMakeLists.txt
│   └── sensors/
├── ros2_ws/
│   └── src/
│       ├── turtle_py/
│       ├── turtle_cpp/
│       └── turtle_interfaces/
├── screenshots/
└── bags/
```

### 제출하지 않을 빌드 산출물

``` text
cpp_basic/build/
cpp_basic/main.o
cpp_basic/motor.o
cpp_basic/robot
cpp_basic/stop_distance

# → 소스가 아니라 빌드 과정에서 생성되는 파일
# → .gitignore로 관리
# → 최종 ZIP에서도 제외
```

------------------------------------------------------------------------

# 16. `.gitignore`

이번 실습에서 C++/CMake 빌드 산출물까지 관리하도록 정리했다.

``` gitignore
# Python 가상환경 / 캐시
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.ipynb_checkpoints/

# 일반 CMake / 빌드 디렉터리
build/
install/
log/

# C++ 컴파일 결과
*.o
*.obj
*.a
*.so

# 현재 cpp_basic에서 생성되는 실행파일
cpp_basic/robot
cpp_basic/stop_distance

# CMake가 생성하는 파일
CMakeCache.txt
CMakeFiles/
cmake_install.cmake
Makefile

# ROS2 빌드 결과
ros2_ws/build/
ros2_ws/install/
ros2_ws/log/

# OS
Thumbs.db
.DS_Store
```

------------------------------------------------------------------------

# 17. `.gitignore`에서 놓치기 쉬운 부분

`.gitignore`는 **아직 Git이 추적하지 않는 파일을 무시하는 역할**을 한다.

이미 Git에 올라간 파일은 `.gitignore`에 추가해도 자동으로 사라지지
않는다.

``` text
이미 Git이 추적 중
        ↓
.gitignore에 추가
        ↓
여전히 Git 추적 상태
        ↓
git rm --cached 필요
```

예:

``` bash
# Git 추적에서만 제거
# 로컬의 실제 파일은 삭제하지 않음
git rm --cached cpp_basic/robot
git rm --cached cpp_basic/stop_distance
```

------------------------------------------------------------------------

# 18. 실제 Git 작업에서 발생한 실수

처음 명령을 잘못 붙여 입력했다.

``` bash
# 잘못된 입력
git add .git rm --cached cpp_basic/robot
```

Git은 이것을 하나의 `git add` 명령으로 해석했기 때문에:

``` text
error: 알 수 없는 옵션 'cached'
```

가 발생했다.

올바른 방법:

``` bash
# 각각 별도의 명령으로 실행
git add .
git rm --cached cpp_basic/robot
git rm --cached cpp_basic/stop_distance
```

또는 필요한 파일만:

``` bash
git rm --cached cpp_basic/robot
git rm --cached cpp_basic/stop_distance

git add .gitignore
git commit -m "chore: remove build artifacts from tracking"
git push
```

------------------------------------------------------------------------

# 19. Git 작업 위치

현재 Git 저장소의 루트는:

``` text
~/KantPA
```

이다.

``` text
~/KantPA/
├── .git/
├── .gitignore
├── report.md
├── lv1_module1_sangjun/
├── lv1_module2_sangjun/
├── lv1_module3_sangjun/
└── lv1_module4_sangjun/
```

따라서 Git 전체 상태를 확인하고 커밋하는 작업은 저장소 루트에서 하는
것이 좋다.

``` bash
# Git 저장소 루트로 이동
cd ~/KantPA

# 전체 저장소 상태 확인
git status

# 변경사항 추가
git add .

# 커밋
git commit -m "chore: update module 2"

# 원격 저장소에 업로드
git push
```

코드 작성과 빌드는 하위 디렉터리에서 해도 된다.

``` bash
# C++ 문제 작업
cd ~/KantPA/lv1_module2_sangjun/cpp_basic
```

핵심:

``` text
코드/빌드 작업
→ 필요한 프로젝트 폴더에서

Git 관리
→ ~/KantPA에서
```

------------------------------------------------------------------------

# 20. 오늘 잘했던 부분

## 20.1 오류를 직접 경험함

단순히 명령어를 복사하지 않고 실제 오류를 발생시켰다.

``` bash
# 헤더 파일을 직접 컴파일
g++ -c motor.hpp -o motor.o

# → #pragma once in main file 경고 확인
```

그리고:

``` bash
# -c 없이 motor.cpp를 빌드
g++ -Wall -Wextra -O2 -std=c++17 motor.cpp -o motor.o

# → undefined reference to `main'
```

이 과정을 통해 **컴파일과 링크가 다르다는 것을 실제 오류로 확인했다.**

## 20.2 CMake 경로 문제를 해결함

``` bash
# 잘못된 위치
cd cpp_basic
cmake ..

# → 부모 디렉터리에서 CMakeLists.txt를 찾으려 함
```

이후:

``` bash
mkdir build
cd build
cmake ..
make
```

으로 정상 빌드했다.

## 20.3 증분 빌드를 직접 확인함

`motor.cpp`만 수정한 뒤:

``` bash
make
```

를 실행해서 실제로:

``` text
Building CXX object ... motor.cpp.o
Linking CXX executable robot
```

만 다시 수행되는 것을 확인했다.

## 20.4 Git 추적과 로컬 파일의 차이를 이해함

``` bash
git rm --cached cpp_basic/robot
```

은:

``` text
Git에서는 제거
로컬 파일은 유지
```

라는 것을 경험했다.

------------------------------------------------------------------------

# 21. 놓쳤거나 복습이 필요한 부분

## 21.1 `-o`와 `-c`는 역할이 다르다

``` bash
g++ -c motor.cpp -o motor.o
```

각 옵션의 의미:

``` text
-c
# → 컴파일만 수행

-o motor.o
# → 결과 파일의 이름을 motor.o로 지정
```

`-o motor.o`라고 해서 컴파일만 하는 것은 아니다.

``` bash
# -c가 없으면 링크까지 시도한다.
g++ motor.cpp -o motor.o
```

------------------------------------------------------------------------

## 21.2 `cmake ..`의 `..`

``` bash
cd cpp_basic/build
cmake ..
```

여기서:

``` text
.   = 현재 디렉터리
..  = 부모 디렉터리
```

따라서:

``` text
cpp_basic/build
        │
        │ ..
        ↓
cpp_basic/
└── CMakeLists.txt
```

------------------------------------------------------------------------

## 21.3 `.gitignore`와 기존 추적 파일

``` text
.gitignore
   ↓
앞으로 추적하지 않을 파일을 지정
```

하지만:

``` text
이미 Git이 추적 중인 파일
   ↓
.gitignore만 추가
   ↓
자동 제거되지 않음
```

따라서:

``` bash
git rm --cached 파일명
```

이 필요하다.

------------------------------------------------------------------------

# 22. 오늘 새로 배운 핵심 개념

``` text
.hpp
# → 클래스/함수 선언을 담는 헤더

.cpp
# → 실제 함수 구현

public
# → 클래스 외부에 공개되는 인터페이스

private
# → 클래스 내부에서 관리하는 데이터

-c
# → 컴파일만 수행

.o
# → 컴파일 결과인 오브젝트 파일

링크
# → 여러 오브젝트 파일을 하나의 실행파일로 연결

main()
# → 실행파일이 시작되는 진입점

CMake
# → 빌드 과정을 설정하고 관리하는 도구

cmake ..
# → 현재 build 디렉터리의 부모 디렉터리에서 CMakeLists.txt를 찾아
#    빌드 시스템을 생성

make
# → CMake가 생성한 빌드 시스템에 따라 실제 빌드

증분 빌드
# → 변경된 부분만 다시 컴파일/링크

.gitignore
# → Git에서 추적하지 않을 파일을 지정

git rm --cached
# → 로컬 파일은 유지하면서 Git 추적만 제거
```

------------------------------------------------------------------------

# 23. 오늘의 핵심 연결 관계

``` text
C++ 소스
  ↓
컴파일
  ↓
.o
  ↓
링크
  ↓
실행파일
  ↓
CMake로 이 과정을 자동화
  ↓
make로 빌드
  ↓
증분 빌드로 변경된 부분만 재빌드
  ↓
.gitignore로 생성 파일 관리
  ↓
Git 저장소에는 소스와 필요한 설정만 관리
```

------------------------------------------------------------------------

# 24. 문제 1 제출 체크리스트

``` text
[완료] stop_distance.cpp
[완료] motor.hpp
[완료] motor.cpp
[완료] main.cpp
[완료] CMakeLists.txt

[완료] 수동 2단계 빌드
[완료] 컴파일 오류/링크 오류 확인
[완료] CMake 빌드
[완료] 증분 빌드 출력 확인
[완료] 증분 빌드 원리 정리

[완료] .gitignore 수정
[완료] main.o 추적 제거
[완료] motor.o 추적 제거
[완료] robot 추적 제거
[완료] stop_distance 추적 제거

[진행 필요] report.md의 문제 1 절 최종 작성
[진행 필요] 최종 제출 ZIP 구조 검증
```

------------------------------------------------------------------------

# 25. 오늘 질문 요약

``` markdown
# 오늘 내가 질문한 내용

1. namespace 부분은 내가 이해하기 쉬운 이름으로 수정해도 되는가?
2. VS Code에서 C++ 코드의 줄바꿈/들여쓰기는 어떻게 하는가?
3. `.hpp`와 `.cpp`의 차이는 무엇인가?
4. `public`과 `private`의 역할과 차이는 무엇인가?
5. `motor.hpp`, `motor.cpp`를 만들었을 때 `main.cpp`는 어떻게 작성하는가?
6. `g++ -c motor.hpp`에서 `#pragma once in main file` 경고가 발생한 이유는 무엇인가?
7. 세 파일을 컴파일과 링크 두 단계로 나누어 빌드하는 이유는 무엇인가?
8. 링크는 왜 필요한가?
9. 증분 빌드는 무엇인가?
10. `robot`을 실행하면 `main.o`와 `motor.o`가 각각 실행되는 것인가?
11. 강의 자료의 CMakeLists.txt를 현재 프로젝트 구조에 맞게 어떻게 수정하는가?
12. `cmake ..`에서 CMakeLists.txt를 찾지 못한 이유는 무엇인가?
13. `build/`에서 `cmake ..`를 실행하는 이유는 무엇인가?
14. `cmake .. && make` 출력은 어떻게 읽는가?
15. `motor.cpp`만 수정했을 때 왜 motor.cpp만 재컴파일되는가?
16. 최종 제출 포맷에 맞는 `.gitignore`는 어떻게 작성하는가?
17. `.gitignore`에 추가했는데도 GitHub에 기존 빌드 파일이 남아 있는 이유는 무엇인가?
18. `git rm --cached`는 무엇을 하는가?
19. Git 작업을 `~/KantPA`에서 하는 이유는 무엇인가?
```

------------------------------------------------------------------------

# 26. 다음 학습으로 연결

``` text
오늘
문제 1
C++ 기본 + 빌드 시스템 + Git
        ↓
다음
문제 2
sensors/
        ↓
이후
ROS2
        ↓
Python / C++
        ↓
Node / Topic / Service / Action
        ↓
Launch / Parameter / TF / RViz / rosbag
```

> 오늘 가장 중요한 것은 **"코드를 작성했다"에서 끝나지 않고, C++ 코드가
> 어떻게 `.o`가 되고, 링크되어 실행파일이 되며, CMake가 이 과정을 어떻게
> 관리하고, Git에서는 무엇을 제출 대상으로 남겨야 하는지까지 하나의
> 흐름으로 이해한 것**이다.