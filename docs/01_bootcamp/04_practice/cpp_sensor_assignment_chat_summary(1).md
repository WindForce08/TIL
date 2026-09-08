# C++ 센서 과제 학습 정리

## 목차
1. 다형성 루프 출력
2. 스택 객체와 힙 객체의 소멸 시점
3. 가상 소멸자 실습
4. `std::boolalpha`
5. `main()` 코드 한 줄씩 분석
6. Physical AI / ROS2에서 포인터와 소멸자의 중요성
7. 템플릿 · STL · 스마트 포인터 · RAII

---

## 1. 다형성 루프 출력

사용한 핵심 코드:

```cpp
std::vector<std::unique_ptr<Sensor>> sensors;

sensors.push_back(std::make_unique<Lidar>());
sensors.push_back(std::make_unique<Imu>());

for (auto& s : sensors) {
    auto data = s->read();

    for (double value : data) {
        std::cout << value << " ";
    }
    std::cout << std::endl;
}
```

실행 결과:

```text
Program started!
1 2 3
0.1 0.2 0.3
```

`Sensor`를 부모 클래스로 두고 `Lidar`, `Imu`가 `read()`를 각각 재정의했다.

```cpp
virtual std::vector<double> read() = 0;
```

부모 타입의 포인터로 `s->read()`를 호출해도 실제 객체에 맞는 함수가 호출된다.

```text
Lidar 객체 → Lidar::read() → 1 2 3
Imu 객체   → Imu::read()   → 0.1 0.2 0.3
```

이것이 다형성이다.

---

## 2. 스택 객체와 힙 객체의 소멸 시점

기존:

```cpp
virtual ~Sensor() = default;
```

를 다음처럼 수정하여 소멸 시점을 관찰했다.

```cpp
virtual ~Sensor() {
    std::cout << "Sensor destructor called" << std::endl;
}
```

실행 결과:

```text
Program started!
1 2 3
0.1 0.2 0.3
Sensor destructor called
Sensor destructor called
```

두 개의 객체(`Lidar`, `Imu`)가 있기 때문에 소멸자 로그가 두 번 출력된다.

`unique_ptr`이 객체의 소유권을 관리하기 때문에 `main()`이 종료되고 `sensors`가 소멸할 때 관리하던 객체들도 자동으로 소멸한다.

```text
main() 종료
 ↓
sensors 소멸
 ↓
unique_ptr 소멸
 ↓
Lidar / Imu 객체 삭제
 ↓
Sensor 소멸자 실행
```

---

## 3. 가상 소멸자 실습

자식 클래스에 실제 소멸자를 추가했다.

```cpp
~Lidar() {
    std::cout << "Lidar destructor called" << std::endl;
}
```

```cpp
~Imu() {
    std::cout << "Imu destructor called" << std::endl;
}
```

부모:

```cpp
virtual ~Sensor() {
    std::cout << "Sensor destructor called" << std::endl;
}
```

실행 결과:

```text
Program started!
Lidar constructor called
Lidar connected: true
Imu constructor called
Imu connected: true
1 2 3
0.1 0.2 0.3
Lidar destructor called
Sensor destructor called
Imu destructor called
Sensor destructor called
```

관찰 결과:

```text
Lidar
 ↓
~Lidar()
 ↓
~Sensor()
```

```text
Imu
 ↓
~Imu()
 ↓
~Sensor()
```

즉 **자식 소멸자 → 부모 소멸자** 순서로 호출된다.

부모 소멸자를 `virtual`로 두는 이유는 부모 포인터를 통해 자식 객체를 삭제할 때 실제 객체의 소멸자가 올바르게 호출되도록 하기 위해서다.

---

## 4. `std::boolalpha`

다음 코드:

```cpp
std::cout << "Lidar connected: "
          << std::boolalpha
          << connected
          << std::endl;
```

`std::boolalpha`는 `bool` 값을 `true` / `false`로 출력하게 한다.

기본:

```cpp
std::cout << connected;
```

출력:

```text
1
```

`boolalpha` 사용:

```cpp
std::cout << std::boolalpha << connected;
```

출력:

```text
true
```

`std::noboolalpha`를 사용하면 다시 `0` / `1` 방식으로 출력할 수 있다.

---

## 5. `main()` 코드 한 줄씩 분석

### `int main()`

```cpp
int main() {
```

프로그램 실행이 시작되는 함수이다.

### 시작 메시지

```cpp
std::cout << "Program started!" << std::endl;
```

터미널에 시작 메시지를 출력한다.

### vector 생성

```cpp
std::vector<std::unique_ptr<Sensor>> sensors;
```

`unique_ptr<Sensor>` 여러 개를 저장하는 vector를 만든다.

```text
sensors
┌──────────────────────┐
│ 빈 vector             │
└──────────────────────┘
```

### Lidar 생성

```cpp
sensors.push_back(std::make_unique<Lidar>());
```

`std::make_unique<Lidar>()`는 힙에 `Lidar` 객체를 만들고 이를 관리하는 `unique_ptr`을 만든다.

그 후 `push_back()`으로 vector에 추가한다.

개념적으로:

```text
sensors
 ↓
unique_ptr<Sensor>
 ↓
Heap의 Lidar 객체
```

### Imu 생성

```cpp
sensors.push_back(std::make_unique<Imu>());
```

동일하게 Heap의 `Imu` 객체를 생성하고 `unique_ptr`로 관리한다.

최종 구조:

```text
sensors
 ├── unique_ptr<Sensor> ──→ Lidar
 └── unique_ptr<Sensor> ──→ Imu
```

vector가 실제 Lidar/Imu 객체를 직접 저장하는 것이 아니라 `unique_ptr`을 저장한다.

### 범위 기반 for문

```cpp
for (auto& s : sensors) {
```

`sensors`의 요소를 하나씩 꺼낸다.

첫 번째:

```text
s → Lidar를 관리하는 unique_ptr
```

두 번째:

```text
s → Imu를 관리하는 unique_ptr
```

`auto&`는 대략:

```cpp
std::unique_ptr<Sensor>& s
```

와 같다.

### `s->read()`

```cpp
auto data = s->read();
```

`unique_ptr`은 포인터처럼 사용할 수 있다.

첫 번째:

```text
s
 ↓
Lidar 객체
 ↓
Lidar::read()
 ↓
{1.0, 2.0, 3.0}
```

두 번째:

```text
s
 ↓
Imu 객체
 ↓
Imu::read()
 ↓
{0.1, 0.2, 0.3}
```

이것이 다형성이다.

### `auto data`

`read()`의 반환형이 `std::vector<double>`이므로:

```cpp
auto data = s->read();
```

는 사실상:

```cpp
std::vector<double> data = s->read();
```

와 같다.

### 데이터 출력

```cpp
for (double value : data) {
    std::cout << value << " ";
}
```

data의 값을 하나씩 출력한다.

### 줄바꿈

```cpp
std::cout << std::endl;
```

센서 하나의 출력이 끝난 뒤 다음 줄로 이동한다.

### `return 0`

```cpp
return 0;
```

`main()`이 정상 종료되었음을 의미한다.

`main()` 종료 과정에서 `sensors`가 소멸하고 `unique_ptr`이 관리하던 객체도 자동으로 정리된다.

---

## 6. Physical AI / ROS2에서 포인터와 소멸자의 중요성

C++에서 포인터와 객체 수명을 잘못 관리하면 다음과 같은 문제가 발생할 수 있다.

```text
포인터 / 객체 수명 관리 실수
        │
        ├── 메모리 누수
        ├── Dangling Pointer
        ├── Use-After-Free
        ├── Double Free
        └── 잘못된 소멸자
```

### 메모리 누수

```cpp
void callback()
{
    double* data = new double[1000];

    // 처리

    // delete[] data를 하지 않음
}
```

콜백이 반복될 때마다 메모리가 계속 증가할 수 있다.

ROS2 노드는 장시간 실행될 수 있기 때문에 작은 누수도 시간이 지나면서 문제가 커질 수 있다.

```text
callback
 ↓
메모리 증가
 ↓
callback
 ↓
메모리 증가
 ↓
계속 증가
```

### Dangling Pointer

```cpp
Sensor* sensor = new Lidar();

delete sensor;

sensor->read();
```

`delete` 이후 포인터가 가지고 있는 주소는 남아 있을 수 있지만 그 주소의 객체는 이미 삭제되었다.

```text
sensor
  ↓
삭제된 객체
```

이를 Dangling Pointer라고 한다.

### ROS2 Callback에서의 문제

ROS2 callback이 계속 실행되는 상황에서 객체가 너무 일찍 삭제되면:

```text
ROS2 Executor
     ↓
Callback
     ↓
sensor->read()
     ↓
이미 삭제된 객체
     ↓
Crash / 잘못된 데이터
```

가 발생할 수 있다.

센서 데이터가 잘못 처리되면:

```text
센서
 ↓
Perception
 ↓
Controller
 ↓
Motor
```

전체 로봇 동작에 영향을 줄 수 있다.

### 가상 소멸자

```cpp
Sensor* sensor = new Lidar();
delete sensor;
```

와 같은 부모 포인터 기반 삭제에서는:

```cpp
virtual ~Sensor()
```

가 중요하다.

정상적인 다형성 삭제:

```text
delete Sensor 포인터
       ↓
실제 객체 = Lidar
       ↓
~Lidar()
       ↓
~Sensor()
```

---

## 7. 템플릿 · STL · 스마트 포인터 · RAII

현재 배우는 개념들은 서로 연결된다.

```text
C++
 │
 ├── STL
 │    └── vector, map 등
 │
 ├── Template
 │    └── vector<T>, unique_ptr<T>
 │
 ├── Smart Pointer
 │    └── unique_ptr, shared_ptr
 │
 └── RAII
      └── 객체의 수명에 자원 관리를 묶음
```

### STL

```cpp
std::vector<double>
```

센서 데이터처럼 여러 값을 저장할 때 사용한다.

### 스마트 포인터

```cpp
std::unique_ptr<Sensor>
```

객체의 소유권과 수명을 관리한다.

```text
unique_ptr
    ↓
Sensor 객체
    ↓
unique_ptr 소멸
    ↓
Sensor 객체 자동 정리
```

### 템플릿

```cpp
std::vector<double>
```

는 개념적으로:

```text
vector<T>
      ↑
      T = double
```

이다.

```cpp
std::unique_ptr<Sensor>
```

는:

```text
unique_ptr<T>
          ↑
        T = Sensor
```

이다.

### RAII

자원의 생성과 소멸을 객체의 수명에 연결하는 방식이다.

현재 코드에서는:

```text
객체 생성
 ↓
unique_ptr이 소유
 ↓
객체 사용
 ↓
unique_ptr 소멸
 ↓
객체 자동 삭제
```

로 이해할 수 있다.

---

# 핵심 정리

```text
Sensor
  ↑
Lidar / Imu
```

→ 상속 관계

```text
vector
  ↓
unique_ptr<Sensor>
  ↓
실제 Heap 객체
```

→ 객체 저장 및 소유권 관리

```text
s->read()
  ↓
실제 객체 확인
  ↓
Lidar::read() 또는 Imu::read()
```

→ 다형성

```text
virtual ~Sensor()
  ↓
자식 소멸자
  ↓
부모 소멸자
```

→ 안전한 다형성 객체 정리

```text
STL + Template + Smart Pointer + RAII
```

→ 장시간 실행되는 C++/ROS2/Physical AI 시스템에서 객체와 자원을 관리하기 위한 핵심 기초

---

# 다음 학습 후보

1. Stack vs Heap의 실제 메모리 구조
2. `unique_ptr` / `shared_ptr` / `weak_ptr` 차이
3. `virtual`과 vtable/vptr의 실제 동작
4. ROS2 Node와 Callback의 객체 수명
5. ROS2 Publisher / Subscriber / Timer를 C++ 객체로 관리하는 방법
