# TIL — C++ 포인터부터 Virtual 다형성까지

## 0. 학습 요약

이번 학습의 핵심은 `virtual`을 단독으로 외우는 것이 아니라 **포인터의 타입과 실제 객체의 타입 차이**를 이해한 것이다.

핵심 흐름:

```text
메모리 → 주소 → 포인터 → 포인터 타입
→ 객체 포인터 → 상속 → Upcasting
→ Base* + Derived 객체
→ virtual → override
→ 정적/동적 바인딩 → 다형성
→ 센서 추상화 → ROS2 / Physical AI
```

---

# 1. C++ 객체지향과 Physical AI

## 내가 했던 질문

- Python과 C++의 다형성은 어떻게 다른가?
- C++의 `virtual`은 왜 필요한가?
- 이것이 ROS2와 Physical AI에서 어떻게 연결되는가?

## 몰랐던 개념

처음에는 다형성을 단순히 "부모 함수를 자식이 다시 정의하는 것" 정도로 생각했다.

## 새로 학습한 내용

다형성의 핵심은 **공통 인터페이스를 통해 서로 다른 객체를 동일한 방식으로 다루면서 실제 객체에 맞는 동작을 실행하는 것**이다.

Physical AI에서는:

```text
Sensor
 ├── LiDAR
 ├── Camera
 └── IMU
```

처럼 공통 인터페이스를 만들 수 있다.

---

# 2. C++ 포인터 기초

## 내가 했던 질문

> "C++ 포인터 설명부터 만화로 설명해줘. 전공자 수준에 맞게"

## 핵심 개념

```cpp
int x = 10;
int* p = &x;
```

- `x` → 실제 `int` 변수
- `&x` → x의 주소
- `p` → 주소를 저장하는 포인터 변수
- `int*` → p의 타입
- `*p` → p가 가리키는 실제 값

```text
p
│
│ 주소
↓
┌──────┐
│  10  │
└──────┘
```

---

# 3. `&`와 `*`

## 새로 학습한 내용

```cpp
&x
```

→ 주소를 얻는다.

```cpp
*p
```

→ 포인터가 가리키는 대상에 접근한다.

예:

```cpp
int x = 10;
int* p = &x;

*p = 20;
```

결과:

```cpp
x == 20
```

---

# 4. 포인터의 타입

## 내가 했던 핵심 질문

> **"포인터의 타입이 뭐야?"**

예:

```cpp
Animal* animal = &dog;
```

여기서 포인터의 타입은:

```text
Animal*
```

이다.

포인터 타입은 **그 포인터를 통해 대상을 어떤 타입으로 취급할 것인지**를 나타낸다.

---

# 5. 포인터 타입과 실제 객체 타입

이 부분이 이번 학습의 핵심이다.

```cpp
Dog dog;
Animal* animal = &dog;
```

두 가지 타입을 구분해야 한다.

```text
포인터의 정적 타입 → Animal*
실제 객체의 타입   → Dog
```

즉:

```text
animal
  │
  │ Animal*
  ↓
┌──────────┐
│   Dog    │
└──────────┘
```

`animal`은 Animal 객체가 아니라 **Animal 타입의 포인터 변수**이고, Dog 객체의 주소를 저장하고 있다.

---

# 6. `&dog`, `animal`, `&animal`

실제 코드에서 주소 출력도 확인했다.

```cpp
Dog dog;

std::cout << &dog;

Animal* animal = &dog;

std::cout << &animal;
```

세 개를 구분해야 한다.

```text
&dog
→ Dog 객체 자체의 주소

animal
→ Dog 객체의 주소를 저장한 포인터

&animal
→ animal 포인터 변수 자체의 주소
```

따라서:

```text
&dog == animal
```

은 같은 객체를 가리키는 주소가 될 수 있지만,

```text
&animal
```

은 별개의 주소다.

---

# 7. `.`와 `->`

객체 자체:

```cpp
Dog dog;
dog.speak();
```

→ `.`

객체 포인터:

```cpp
Dog* p = &dog;
p->speak();
```

→ `->`

개념적으로:

```cpp
p->speak();
```

는:

```cpp
(*p).speak();
```

와 같은 의미다.

---

# 8. `nullptr`

```cpp
int* p = nullptr;
```

→ 현재 유효한 객체를 가리키지 않는 포인터.

사용 전:

```cpp
if (p != nullptr) {
    std::cout << *p;
}
```

`nullptr`을 역참조하면 정의되지 않은 동작이 발생할 수 있다.

---

# 9. 포인터와 참조

포인터:

```cpp
int* p = &x;
```

참조:

```cpp
int& r = x;
```

주요 차이:

| 구분 | Pointer | Reference |
|---|---|---|
| 주소 기반 접근 | O | O |
| 다른 대상 지정 | 가능 | 일반적으로 불가 |
| `nullptr` | 가능 | 해당 용도로 사용하지 않음 |
| 접근 | `*p` | `r` |
| 멤버 접근 | `p->foo()` | `r.foo()` |

`virtual`의 동적 다형성은 포인터뿐 아니라 참조에서도 가능하다.

---

# 10. 포인터 연산과 배열

```cpp
int arr[4] = {10, 20, 30, 40};
int* p = arr;
```

```cpp
*p
*(p + 1)
*(p + 2)
```

처럼 접근할 수 있다.

`p + 1`은 1바이트 이동이 아니라 **가리키는 타입의 크기만큼 이동**한다.

또한:

```cpp
arr[i]
```

와:

```cpp
*(arr + i)
```

는 같은 원소를 가리킬 수 있다.

단, 배열과 포인터는 완전히 같은 개념은 아니다.

---

# 11. 포인터와 함수

```cpp
void increment(int* p) {
    (*p)++;
}
```

```cpp
int x = 10;
increment(&x);
```

결과:

```text
x == 11
```

포인터를 통해 함수가 호출자의 원본 객체를 직접 수정할 수 있다.

---

# 12. 포인터의 포인터

```cpp
int x = 100;
int* p = &x;
int** pp = &p;
```

구조:

```text
pp
 ↓
 p
 ↓
 x
```

따라서:

```cpp
*pp
```

→ p

```cpp
**pp
```

→ x

---

# 13. 동적 메모리와 Raw Pointer

```cpp
int* p = new int(42);
delete p;
```

직접 관리하면:

- Memory Leak
- Dangling Pointer
- Double Delete
- 예외 발생 시 해제 누락

등의 문제가 발생할 수 있다.

그래서 현대 C++에서는 RAII와 스마트 포인터가 중요하다.

---

# 14. 스마트 포인터와 RAII

## `unique_ptr`

```cpp
std::unique_ptr<Motor> motor =
    std::make_unique<Motor>();
```

→ 단독 소유

## `shared_ptr`

```cpp
std::shared_ptr<Lidar> lidar =
    std::make_shared<Lidar>();
```

→ 공동 소유

핵심:

```text
Raw Pointer
→ 주소 접근

Smart Pointer
→ 주소 접근 + 소유권/수명 관리
```

RAII:

> Resource Acquisition Is Initialization

객체의 수명과 자원 관리를 연결해 자원을 자동으로 정리하는 C++ 핵심 설계 원칙이다.

---

# 15. 상속과 Upcasting

```cpp
class Animal {};

class Dog : public Animal {};
```

이면:

```cpp
Dog dog;
Animal* p = &dog;
```

가 가능하다.

이것을 **Upcasting**이라고 한다.

```text
Animal
  ▲
  │
 Dog
```

Dog 객체를 Animal 관점에서 다룰 수 있다.

---

# 16. `virtual`이 없는 코드 분석

사용한 코드:

```cpp
class Animal {
public:
    void speak() {
        std::cout << "동물 소리\n";
    }
};

class Dog : public Animal {
public:
    void speak() {
        std::cout << "멍멍\n";
    }
};
```

```cpp
Dog dog;

dog.speak();

Animal* animal = &dog;

animal->speak();
```

결과:

```text
멍멍
동물 소리
```

`dog.speak()`은 Dog 객체 자체에 대한 호출이므로 `Dog::speak()`.

반면 `animal->speak()`은 `Animal*`이고 `virtual`이 없으므로 정적 바인딩이 이루어져 `Animal::speak()`이 호출된다.

---

# 17. 정적 바인딩과 동적 바인딩

## 정적 바인딩

`virtual`이 없는 경우:

```cpp
Animal* animal = &dog;
animal->speak();
```

개념:

```text
Animal*
 ↓
Animal::speak()
```

## 동적 바인딩

부모:

```cpp
class Animal {
public:
    virtual void speak() {
        std::cout << "동물 소리\n";
    }
};
```

자식:

```cpp
class Dog : public Animal {
public:
    void speak() override {
        std::cout << "멍멍\n";
    }
};
```

이제:

```cpp
Animal* animal = &dog;
animal->speak();
```

결과:

```text
멍멍
```

흐름:

```text
Animal*
 ↓
실제 객체 확인
 ↓
Dog
 ↓
Dog::speak()
```

---

# 18. 내가 처음 이해한 `virtual`

처음 이해:

> "부모 클래스에서 만들어진 virtual은 자식 클래스에서 오버라이드해서 사용하는 것이고, 그러기 위해서는 포인터가 명확해야 한다."

## 맞았던 부분

- 부모에 `virtual`을 선언한다.
- 자식이 `override`할 수 있다.
- 자식마다 다른 구현을 만들 수 있다.
- 다형성의 기반이 된다.

## 수정한 부분

"포인터가 명확해야 한다"보다는:

> **부모 타입의 포인터 또는 참조로 자식 객체를 다룰 때 `virtual`이 실제 객체의 override된 함수를 호출하도록 한다.**

가 정확하다.

즉 포인터 자체가 목적이 아니라 **부모 타입으로 자식 객체를 다루는 상황**이 핵심이다.

---

# 19. `virtual`을 "약속"으로 이해하기

부모:

```cpp
virtual void speak();
```

는 직관적으로:

> "Animal 계열 객체는 speak라는 공통 인터페이스를 제공한다."

라는 약속으로 이해할 수 있다.

자식:

```cpp
void speak() override;
```

는:

> "나는 그 인터페이스를 내 방식으로 구현한다."

라는 의미다.

단, `virtual`과 순수 가상 함수는 구분해야 한다.

```cpp
virtual void speak() {}
```

→ 기본 구현이 있는 virtual 함수

```cpp
virtual void speak() = 0;
```

→ 순수 가상 함수

---

# 20. `override`

```cpp
void speak() override
```

는 부모 클래스의 virtual 함수를 재정의한다는 것을 명시한다.

컴파일러가 실제 override 여부를 검사하게 해주는 안전장치이므로 현대 C++에서는 적극적으로 사용하는 것이 좋다.

---

# 21. `virtual`의 내부 동작 — vtable/vptr

일반적인 C++ 구현에서는 virtual dispatch를 위해 다음과 같은 구조를 사용할 수 있다.

```text
Dog 객체
┌─────────────────┐
│ vptr ─────────────→ Dog vtable
│ 기타 멤버         │       │
└─────────────────┘       ↓
                       Dog::speak()
```

따라서:

```cpp
Animal* p = new Dog;
p->speak();
```

에서 실제 객체의 virtual 함수 구현을 찾아 호출할 수 있다.

주의:

> vtable/vptr은 C++ 표준이 구체적인 구현을 강제하는 명칭이 아니라 일반적인 구현 방식이다.

---

# 22. Python과 C++ 다형성

Python은 동적 타이핑과 Duck Typing 덕분에 다형성을 상대적으로 자연스럽게 표현할 수 있다.

```python
def make_sound(animal):
    animal.speak()
```

Python은 객체가 필요한 메서드를 제공하는지를 중심으로 동작한다.

C++의 상속 기반 런타임 다형성에서는:

```text
virtual
override
Base*
Derived
```

등이 중요하다.

---

# 23. 센서 예제와 Physical AI

```cpp
class Sensor {
public:
    virtual void read() = 0;
    virtual ~Sensor() = default;
};
```

```cpp
class Lidar : public Sensor {
public:
    void read() override {
        std::cout << "거리 데이터";
    }
};
```

```cpp
class Camera : public Sensor {
public:
    void read() override {
        std::cout << "이미지 데이터";
    }
};
```

상위 시스템에서는:

```cpp
Sensor* sensor;
sensor->read();
```

처럼 공통 인터페이스를 사용할 수 있다.

```text
Sensor*
 ├── Lidar
 ├── Camera
 └── IMU
```

이 구조가 로봇 센서 추상화에 연결된다.

---

# 24. Composition과 Inheritance

상속:

```text
Dog is an Animal
```

Composition:

```text
Robot has a Sensor
Robot has a Motor
Robot has a Controller
```

Physical AI에서는 실제 시스템 구조를 표현하기 위해 Composition이 매우 중요하다.

```text
Robot
 ├── Sensor
 ├── Motor
 ├── Controller
 └── Planner
```

상속과 Composition을 목적에 맞게 조합한다.

---

# 25. 캡슐화

C++의 접근 지정자:

```cpp
public:
private:
protected:
```

핵심:

> 내부 구현은 숨기고 외부에는 필요한 인터페이스만 공개한다.

센서나 제어 객체의 내부 상태를 직접 변경하지 못하게 하고 명확한 API를 제공하는 방식으로 활용할 수 있다.

---

# 26. Python Magic Method와 C++ 연산자 오버로딩

Python:

```python
__init__
__repr__
__add__
__len__
```

등은 객체의 특정 동작을 정의한다.

C++에서는 생성자와 연산자 오버로딩으로 비슷한 객체 중심 인터페이스를 설계할 수 있다.

예:

```cpp
Vector operator+(const Vector& other);
```

로봇의 벡터, 위치, 속도, 행렬 등을 자연스럽게 다룰 수 있다.

---

# 27. Jacobian과 Physical AI

로봇의 Jacobian `J`는 관절 공간과 작업 공간의 관계를 나타낸다.

```text
q̇ → J → ẋ
```

일반적으로:

```text
ẋ = J q̇
```

역으로:

```text
q̇ = J⁺ ẋ
```

와 같이 pseudoinverse를 사용할 수 있다.

---

# 28. Singularity와 Condition Number

Jacobian이 특이점에 가까워지면 작은 입력 변화가 큰 출력 변화를 만들 수 있다.

Condition Number가 커질수록 수치적으로 민감해진다.

Physical AI의 오차 흐름:

```text
센서 오차
 ↓
좌표 변환
 ↓
상태 추정
 ↓
Jacobian / IK
 ↓
관절 명령 오차
 ↓
로봇 끝단 위치 오차
```

따라서 로봇 시스템은 코드의 정상 실행뿐 아니라 수치적 안정성도 고려해야 한다.

---

# 29. Isotropy / Anisotropy

### Isotropy

방향에 따라 성능이 비교적 균일하다.

### Anisotropy

방향에 따라 성능 차이가 크다.

특이점에 가까워지면 특정 방향의 움직임이 매우 어려워질 수 있다.

---

# 30. 전체 개념 연결

## 메모리/객체 관점

```text
변수
 ↓
메모리
 ↓
주소
 ↓
포인터
 ↓
포인터 타입
 ↓
객체 포인터
 ↓
상속
 ↓
Upcasting
 ↓
Base*
 ↓
Derived 객체
 ↓
virtual
 ↓
override
 ↓
동적 바인딩
 ↓
다형성
```

## 메모리 관리 관점

```text
Pointer
 ↓
Raw Pointer
 ↓
new/delete
 ↓
Memory Leak / Dangling Pointer
 ↓
RAII
 ↓
unique_ptr / shared_ptr
 ↓
소유권과 수명 관리
```

## Physical AI 관점

```text
Sensor
 ↓
데이터
 ↓
좌표계 변환
 ↓
상태 추정
 ↓
Jacobian / IK
 ↓
제어
 ↓
Motor
 ↓
Robot Motion
```

---

# 31. 이번 학습에서 가장 중요했던 새 개념

1. **포인터의 타입**
   ```cpp
   Animal* p;
   ```
   여기서 `Animal*`이 포인터 타입이다.

2. **정적 타입과 동적 타입**
   ```cpp
   Animal* p = &dog;
   ```
   - 정적 타입: `Animal*`
   - 실제 객체 타입: `Dog`

3. **주소와 포인터 변수의 주소 구분**
   ```text
   &dog     → Dog 객체의 주소
   animal   → Dog 객체의 주소를 저장
   &animal  → animal 포인터 변수의 주소
   ```

4. **`->`**
   ```cpp
   p->foo();
   ```
   → 포인터가 가리키는 객체의 멤버 접근

5. **Upcasting**
   ```cpp
   Animal* p = &dog;
   ```

6. **정적 바인딩과 동적 바인딩**
   - `virtual` 없음 → 정적 바인딩
   - `virtual` 있음 → 동적 바인딩 가능

7. **`virtual`**
   부모 타입의 포인터/참조로 자식 객체를 다룰 때 실제 객체의 override를 선택하게 하는 핵심 기능.

8. **`override`**
   부모 virtual 함수의 재정의를 명시하고 컴파일러 검사를 받는다.

9. **RAII와 스마트 포인터**
   포인터와 소유권은 다른 개념이며, 현대 C++에서는 소유권을 스마트 포인터로 표현한다.

10. **다형성**
    단순한 오버라이딩이 아니라 공통 인터페이스를 통해 서로 다른 객체를 동일하게 다루는 설계 원리다.

---

# 32. 아직 주의해서 공부해야 할 부분

## `virtual`과 포인터

잘못된 표현:

> "`virtual`을 사용하려면 포인터가 반드시 필요하다."

정확한 표현:

> **부모 타입의 포인터나 참조로 자식 객체를 다룰 때 `virtual`을 이용하면 동적 바인딩이 가능하다.**

## 포인터 타입과 실제 객체 타입

```cpp
Animal* p = &dog;
```

를 보면:

```text
p의 타입 → Animal*
실제 객체 → Dog
```

를 분리해서 생각해야 한다.

## `virtual`의 본질

`virtual`은 단순히 "자식 함수 호출 버튼"이 아니다.

> **부모 타입으로 접근하더라도 실제 객체의 override된 구현을 선택할 수 있게 하는 메커니즘**

이다.

---

# 33. 최종 TIL 회고

이번 학습에서 가장 큰 변화는 `virtual`을 단독 문법으로 이해하는 것이 아니라 **포인터와 객체 타입의 관계 속에서 이해하기 시작했다는 것**이다.

처음:

```text
virtual = 부모의 약속
```

현재:

```text
부모 클래스
 ↓
virtual 함수
 ↓
공통 인터페이스
 ↓
자식 클래스 override
 ↓
상속
 ↓
부모 타입 포인터/참조
 ↓
자식 객체
 ↓
동적 바인딩
 ↓
실제 객체의 함수 실행
 ↓
다형성
```

이 구조가 Physical AI에서는:

```text
Sensor
 ├── LiDAR
 ├── Camera
 └── IMU
```

같은 센서 추상화로 연결된다.

메모리 관리에서는:

```text
Pointer
 ↓
Ownership
 ↓
RAII
 ↓
Smart Pointer
```

로 연결된다.

결국 이번 학습의 핵심은:

> **C++에서 포인터는 객체를 간접적으로 다루는 기반이고, 상속과 함께 부모 타입 포인터가 자식 객체를 가리킬 수 있으며, `virtual`은 이 상황에서 실제 객체의 구현을 선택하게 하여 런타임 다형성을 가능하게 한다.**

---

# 34. 다음 학습 순서

```text
[현재 학습]
포인터
 ↓
포인터 타입
 ↓
객체 포인터
 ↓
상속 / Upcasting
 ↓
virtual / override
 ↓
정적 / 동적 바인딩
 ↓
스마트 포인터 / RAII

[다음 학습]
참조 심화
 ↓
const correctness
 ↓
복사 생성자
 ↓
이동 생성자
 ↓
Rule of 3 / 5 / 0
 ↓
virtual destructor
 ↓
순수 가상 클래스 / interface 설계
 ↓
Composition vs Inheritance
 ↓
Template
 ↓
STL
 ↓
ROS2 C++ Node
 ↓
Sensor Publisher / Subscriber
 ↓
Physical AI 시스템 설계
```

---

## 핵심 키워드

```text
C++
Pointer
Address
Dereference
nullptr
Reference
Object
Class
Inheritance
Upcasting
Static Type
Dynamic Type
Static Binding
Dynamic Binding
virtual
override
vtable
vptr
Polymorphism
RAII
unique_ptr
shared_ptr
Ownership
Memory Leak
Dangling Pointer
Encapsulation
Composition
Sensor Abstraction
ROS2
Jacobian
Singularity
Condition Number
Isotropy
Anisotropy
Physical AI
```
