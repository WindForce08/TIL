# C++ g++ 컴파일 및 실행 명령어 정리

## 1. 기본 컴파일

```bash
g++ main.cpp -o main
```

- `g++`: C++ 컴파일러
- `main.cpp`: 컴파일할 C++ 소스 파일
- `-o main`: 생성되는 실행 파일의 이름을 `main`으로 지정

## 2. 컴파일 후 실행

### Linux / macOS

```bash
./main
```

### Windows

```bash
main.exe
```

## 3. C++17과 경고 옵션을 사용하는 컴파일

```bash
g++ -Wall -std=c++17 main.cpp -o main
```

### 옵션 설명

| 옵션 | 설명 |
|---|---|
| `g++` | C++ 컴파일러 |
| `-Wall` | 주요 컴파일 경고를 활성화 |
| `-std=c++17` | C++17 표준으로 컴파일 |
| `main.cpp` | 컴파일할 소스 파일 |
| `-o main` | 실행 파일 이름을 `main`으로 지정 |

## 4. `-Wall`

```bash
g++ -Wall main.cpp -o main
```

`-Wall`은 컴파일러가 코드의 잠재적인 문제를 경고하도록 하는 옵션입니다.

예를 들어 사용하지 않는 변수나 일부 문법상의 문제 등을 경고해 줄 수 있습니다.

코드에 문제가 없다는 것을 보장하는 것은 아니지만, 개발할 때 경고를 확인하는 데 유용합니다.

## 5. `-std=c++17`

```bash
g++ -std=c++17 main.cpp -o main
```

`-std=c++17`은 **C++17 표준을 사용해서 컴파일하라**는 의미입니다.

C++에는 C++11, C++14, C++17, C++20, C++23 등의 표준이 있으며, 이 옵션을 사용하면 원하는 표준을 명시할 수 있습니다.

## 6. 자주 사용하는 컴파일 명령어

### 기본

```bash
g++ main.cpp -o main
```

### 경고 활성화

```bash
g++ -Wall main.cpp -o main
```

### C++17 사용

```bash
g++ -std=c++17 main.cpp -o main
```

### 경고 + C++17

```bash
g++ -Wall -std=c++17 main.cpp -o main
```

## 7. 컴파일과 실행을 한 줄로

Linux / macOS:

```bash
g++ -Wall -std=c++17 main.cpp -o main && ./main
```

`&&`는 앞의 명령이 성공했을 때만 다음 명령을 실행합니다.

따라서:

1. `main.cpp` 컴파일
2. 컴파일 성공
3. `./main` 실행

순서로 진행됩니다.

## 8. 전체 기본 흐름

```bash
# 1. 컴파일
g++ -Wall -std=c++17 main.cpp -o main

# 2. 실행
./main
```

Windows에서는 실행 파일이 보통 다음과 같이 생성됩니다.

```bash
main.exe
```

따라서:

```bash
g++ -Wall -std=c++17 main.cpp -o main.exe
main.exe
```

## 9. 명령어 구조 이해하기

다음 명령어를 기준으로 보면:

```bash
g++ -Wall -std=c++17 main.cpp -o main
```

구조는 다음과 같습니다.

```text
g++
│
├── -Wall
│   └── 컴파일 경고 활성화
│
├── -std=c++17
│   └── C++17 표준 사용
│
├── main.cpp
│   └── 입력 소스 파일
│
└── -o main
    └── 출력 실행 파일 이름
```

## 10. 가장 추천하는 기본 형태

C++17을 공부하거나 일반적인 C++ 프로그램을 컴파일할 때는 다음 형태를 기본으로 사용하면 됩니다.

```bash
g++ -Wall -std=c++17 main.cpp -o main
./main
```
