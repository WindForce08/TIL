# Print 디버깅과 실무 로깅(Logging) 가이드

## 1. Print 디버깅(Print Debugging)이란?

코딩을 할 때 코드 내에 `print("~~~ 완료!")`와 같은 출력 구문을 삽입하여 **함수의 작동 여부, 데이터 흐름, 실행 위치 및 에러 발생 지점**을 파악하는 디버깅 기법입니다.

---

## 2. Print 디버깅의 장점과 한계

### 장점
- **직관적이고 신속함**: 별도의 도구 설정 없이 코드를 작성하는 즉시 실행 흐름을 확인할 수 있습니다.
- **학습 및 초반 개발 시 유용**: 간단한 알고리즘이나 소규모 스크립트 작성 시 매우 편리합니다.

### 한계
- **코드 오염 (Code Pollution)**: 개발 완료 후 배포 전 일일이 `print()` 문을 찾아 삭제하거나 주석 처리해야 합니다.
- **로그 중요도 구분 불가**: 단순 진행 상황 안내 메시지와 치명적인 오류(Error) 메시지가 동일하게 처리됩니다.
- **컨텍스트 정보 부족**: 출력이 실행된 시간(Timestamp), 파일 이름, 함수 이름, 줄 번호(Line number) 등의 부가 정보가 기본 제공되지 않습니다.
- **성능 및 보안 문제**: 무분별한 콘솔 출력은 디스크 I/O를 유발하며, 실무 환경에서는 민감 정보가 콘솔에 노출될 위험이 있습니다.

---

## 3. 실무에서의 발전된 형태: 로깅(Logging) 프레임워크

실무나 규모가 큰 프로젝트에서는 단순 `print()` 대신 **로깅(Logging) 라이브러리**를 사용합니다.

### 3.1. 로깅 수준 (Log Levels)

로깅 프레임워크는 출력 메시지의 중요도를 단계별로 나누어 관리합니다.

| 로그 레벨 | 용도 | 설명 |
| :--- | :--- | :--- |
| **`DEBUG`** | 디버깅 정보 | 개발 과정에서 변수 값, 내부 상태 등 세부 정보를 확인할 때 사용 (배포 시 비활성화) |
| **`INFO`** | 일반 정보 | 시스템이 정상적으로 동작하고 있음을 알리는 주요 이벤트 (예: "서버 시작 완료", "DB 연결 성공") |
| **`WARN` / `WARNING`** | 경고 | 당장 에러는 아니지만 향후 문제가 될 수 있는 상황 (예: "메모리 사용량 85% 초과") |
| **`ERROR`** | 오류 | 함수 실행 실패 등 복구 가능한 오류 발생 |
| **`FATAL` / `CRITICAL`** | 치명적 오류 | 프로그램이 더 이상 실행될 수 없어 강제 종료되는 심각한 오류 |

---

## 4. 실무 코드 작성 예시

### 4.1. ROS 2 (Python) 노드에서의 로깅

ROS 2에서는 `print()` 대신 노드가 제공하는 `self.get_logger()`를 사용합니다.

```python
import rclpy
from rclpy.node import Node

class MyRobotNode(Node):
    def __init__(self):
        super().__init__('my_robot_node')
        
        # ROS 2 표준 로깅
        self.get_logger().info('로봇 노드가 성공적으로 초기화되었습니다.')

    def process_sensor_data(self, data):
        if data is None:
            self.get_logger().error('센서 데이터가 비어있습니다!')
            return

        self.get_logger().debug(f'수신된 센서 값: {data}')
        # 작업 처리...
        self.get_logger().info('센서 데이터 처리 완료!')

def main(args=None):
    rclpy.init(args=args)
    node = MyRobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### ROS 2 로그 출력 형태
```text
[INFO] [1718123456.789123456] [my_robot_node]: 로봇 노드가 성공적으로 초기화되었습니다.
[ERROR] [1718123457.123456789] [my_robot_node]: 센서 데이터가 비어있습니다!
```
- **시간 스탬프**, **노드명**, **로그 레벨**이 자동으로 포맷팅되어 터미널 및 로그 파일에 저장됩니다.

---

### 4.2. 파이썬 기본 `logging` 모듈

일반 파이썬 애플리케이션에서는 기본 제공되는 `logging` 모듈을 활용합니다.

```python
import logging

# 로거 기본 설정 (시간 - 로그레벨 - 메시지)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
)

def run_task():
    logging.info("작업을 시작합니다.")
    
    try:
        result = 10 / 2
        logging.debug(f"계산 결과: {result}")
        logging.info("작업 처리 완료!")
    except Exception as e:
        logging.error(f"작업 처리 중 오류 발생: {e}")

if __name__ == '__main__':
    run_task()
```

---

## 5. 결론 및 실무 팁

1. **개발 초기 아이디어 검증 시**: `print()`를 활용해 빠르게 흐름을 확인하는 것은 자연스러운 디버깅 과정입니다.
2. **프로젝트 규모 확장 시**: `print()` 대신 프로젝트 환경(ROS 2 Logger, Python Logging 등)에 맞는 로깅 방식을 채택합니다.
3. **디버거(Debugger) 활용**: 변수 상태를 정밀하게 확인하고 싶을 때는 VS Code의 `Breakpoint`(중단점) 디버깅 기능을 결합하여 사용하면 훨씬 효율적입니다.
