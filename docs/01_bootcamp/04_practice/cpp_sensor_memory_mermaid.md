# C++ 상속 · 포인터 · 힙 메모리 · 소멸자 한눈에 보기

> 이 문서는 현재 과제의 `Sensor → Lidar / Imu` 구조를 기준으로 메모리와
> 소멸자 흐름을 아주 단순하게 정리한 자료입니다.

------------------------------------------------------------------------

## 1. 클래스 관계부터 보기

``` mermaid
classDiagram
    class Sensor {
        <<abstract>>
        bool connected
        virtual read()
        virtual ~Sensor()
    }

    class Lidar {
        read()
        ~Lidar()
    }

    class Imu {
        read()
        ~Imu()
    }

    Sensor <|-- Lidar
    Sensor <|-- Imu
```

### 핵심

-   `Sensor` = 부모 클래스
-   `Lidar`, `Imu` = 자식 클래스
-   자식 클래스는 부모 클래스의 기능을 물려받습니다.
-   `read()`는 자식 클래스에서 각각 다르게 구현합니다.

------------------------------------------------------------------------

## 2. 객체를 만들면 어떻게 연결되는가?

현재 코드:

``` cpp
std::vector<std::unique_ptr<Sensor>> sensors;

sensors.push_back(std::make_unique<Lidar>());
sensors.push_back(std::make_unique<Imu>());
```

아주 단순하게 생각하면:

``` mermaid
flowchart LR
    V["sensors 벡터"] --> P1["unique_ptr<Sensor>"]
    V --> P2["unique_ptr<Sensor>"]

    P1 --> L["Lidar 객체"]
    P2 --> I["Imu 객체"]
```

중요한 점:

> `unique_ptr<Sensor>` 자체가 `Lidar` 객체가 되는 것은 아닙니다.

`unique_ptr`는 **객체가 있는 곳을 가리키는 역할**을 합니다.

------------------------------------------------------------------------

## 3. 메모리 주소를 아주 단순하게 생각하기

실제 주소는 실행할 때마다 달라집니다.

따라서 아래 주소는 **설명을 위한 가상의 주소**입니다.

``` mermaid
flowchart TB
    subgraph Stack["Stack"]
        V["sensors 벡터"]
        P1["unique_ptr #1\n0x1000을 가리킴"]
        P2["unique_ptr #2\n0x2000을 가리킴"]
    end

    subgraph Heap["Heap"]
        L["0x1000\nLidar 객체"]
        I["0x2000\nImu 객체"]
    end

    V --> P1
    V --> P2
    P1 --> L
    P2 --> I
```

### 이것만 기억하세요

``` text
unique_ptr
    ↓
"객체가 있는 주소"를 가지고 있음
    ↓
그 주소의 객체를 관리함
```

예를 들어:

``` text
unique_ptr #1 → 0x1000 → Lidar
unique_ptr #2 → 0x2000 → Imu
```

------------------------------------------------------------------------

## 4. 그런데 왜 `Sensor*`로 Lidar를 가리킬 수 있을까?

상속 관계가 있기 때문입니다.

``` mermaid
flowchart LR
    S["Sensor*"] --> L["Lidar 객체"]

    L -->|"실제 객체"| R["Lidar::read()"]
```

즉,

``` cpp
Sensor* p = new Lidar();
```

처럼 사용할 수 있습니다.

변수 `p`의 타입은 `Sensor*`이지만,

실제로 가리키는 객체는 `Lidar`입니다.

------------------------------------------------------------------------

## 5. 그래서 다형성이 발생한다

현재 코드의:

``` cpp
for (auto& s : sensors) {
    auto data = s->read();
}
```

를 아주 단순하게 표현하면:

``` mermaid
flowchart TD
    A["s->read()"] --> B{"실제 객체는?"}

    B -->|"Lidar"| C["Lidar::read()"]
    B -->|"Imu"| D["Imu::read()"]
```

즉,

``` text
Sensor 타입으로 접근
        ↓
실제 객체 확인
        ↓
Lidar → Lidar::read()
Imu   → Imu::read()
```

이것이 **다형성**입니다.

------------------------------------------------------------------------

## 6. `virtual`은 무엇을 해주는가?

쉽게 생각하면:

``` cpp
virtual std::vector<double> read() = 0;
```

는

> "Sensor로 접근하더라도 실제 객체에 맞는 함수를 찾아가라."

라고 C++에게 알려주는 역할입니다.

``` mermaid
flowchart LR
    P["Sensor 포인터"] --> V["virtual 함수"]
    V --> L["실제 객체가 Lidar\n→ Lidar::read()"]
    V --> I["실제 객체가 Imu\n→ Imu::read()"]
```

------------------------------------------------------------------------

# 7. 이제 소멸자를 보자

현재 과제에서 가장 중요한 부분입니다.

``` cpp
virtual ~Sensor() {
    std::cout << "Sensor destructor called" << std::endl;
}
```

그리고 자식 클래스:

``` cpp
~Lidar() {
    std::cout << "Lidar destructor called" << std::endl;
}
```

``` cpp
~Imu() {
    std::cout << "Imu destructor called" << std::endl;
}
```

소멸 순서는:

``` mermaid
flowchart TD
    A["Lidar 객체 소멸"] --> B["~Lidar()"]
    B --> C["~Sensor()"]

    D["Imu 객체 소멸"] --> E["~Imu()"]
    E --> F["~Sensor()"]
```

### 핵심 규칙

> **자식 소멸자 → 부모 소멸자**

------------------------------------------------------------------------

# 8. `unique_ptr`이 있으면 누가 삭제하는가?

우리가 직접:

``` cpp
delete p;
```

를 하지 않아도 됩니다.

`unique_ptr`이 객체를 관리하기 때문입니다.

``` mermaid
flowchart TD
    A["main() 종료"] --> B["sensors 소멸"]
    B --> C["unique_ptr 소멸"]
    C --> D["관리하던 객체 삭제"]
    D --> E["Lidar / Imu 소멸자 실행"]
    E --> F["Sensor 소멸자 실행"]
```

즉:

``` text
main 종료
   ↓
vector 소멸
   ↓
unique_ptr 소멸
   ↓
Lidar / Imu 삭제
   ↓
자식 소멸자
   ↓
부모 소멸자
```

------------------------------------------------------------------------

# 9. 왜 부모 소멸자에 `virtual`이 필요한가?

이것이 이번 과제의 핵심입니다.

### 정상적인 경우

``` cpp
virtual ~Sensor()
```

``` mermaid
flowchart TD
    A["unique_ptr<Sensor>"] --> B["실제 객체 확인"]
    B --> C["Lidar"]
    C --> D["~Lidar()"]
    D --> E["~Sensor()"]
```

`virtual` 덕분에 실제 객체가 `Lidar`라는 것을 알고

``` text
~Lidar()
  ↓
~Sensor()
```

순서로 소멸합니다.

------------------------------------------------------------------------

## 10. `virtual`이 없으면?

``` cpp
~Sensor()
```

만 있다면 부모 타입을 통해 삭제할 때 문제가 생길 수 있습니다.

``` mermaid
flowchart TD
    A["Sensor 포인터"] --> B["delete"]
    B --> C["~Sensor()"]
    C --> D["자식 소멸자 호출 안 될 수 있음"]
```

쉽게 기억하면:

``` text
virtual 있음
→ 실제 객체의 소멸자부터 호출
→ 안전한 다형성 삭제

virtual 없음
→ 부모 소멸자만 호출될 수 있음
→ 자식 부분이 제대로 정리되지 않을 위험
```

------------------------------------------------------------------------

# 11. 전체 흐름을 하나로 연결

``` mermaid
flowchart TD
    A["Sensor 부모 클래스"] --> B["Lidar"]
    A --> C["Imu"]

    B --> D["make_unique<Lidar>()"]
    C --> E["make_unique<Imu>()"]

    D --> F["unique_ptr<Sensor>"]
    E --> G["unique_ptr<Sensor>"]

    F --> H["Heap의 Lidar 객체"]
    G --> I["Heap의 Imu 객체"]

    H --> J["s->read()"]
    I --> K["s->read()"]

    J --> L["Lidar::read()"]
    K --> M["Imu::read()"]

    H --> N["소멸"]
    I --> O["소멸"]

    N --> P["~Lidar()"]
    P --> Q["~Sensor()"]

    O --> R["~Imu()"]
    R --> S["~Sensor()"]
```

------------------------------------------------------------------------

# 12. 희우님이 지금 기억할 것 5개

``` text
① Sensor
   = 부모 클래스

② Lidar / Imu
   = Sensor를 상속받은 자식 클래스

③ unique_ptr<Sensor>
   = 실제 Lidar / Imu 객체를 가리키고 관리하는 포인터

④ virtual
   = 부모 타입으로 접근해도 실제 자식 타입의 함수를 찾아가게 함

⑤ virtual ~Sensor()
   = 부모 포인터로 자식 객체를 삭제할 때
     자식 소멸자 → 부모 소멸자 순서로 안전하게 소멸하도록 함
```

> **주소는 실제 실행마다 달라지므로 `0x1000`, `0x2000` 같은 값은 개념
> 이해를 위한 가상 주소입니다.**
