# ROS 2 & Git & Antigravity 실습 및 트러블슈팅 정리 노트
>
>작성일: 2026-08-13
>
>최종 수정일: 2026-08-14
>
>학습목표
>
---

## 📌 1. ROS 2 워크스페이스 (`ROS2_WS`) 구조 분석

* **워크스페이스 경로**: `~/Sparta/workspace/ROS2_WS`

### 패키지 구성 및 역할

| 패키지명 | 언어 | 주요 파일 | 주요 역할 및 특징 |
| :--- | :---: | :--- | :--- |
| **`demo_py_pkg`** | Python | `talker.py` | `std_msgs/String` 타입 메시지를 상대 토픽 `chatter`로 발행하는 Publisher 노드.<br>파라미터: `publish_period`, `message_prefix` |
| **`demo_cpp_pkg`** | C++ | `listener.cpp` | 상대 토픽 `chatter`를 구독하여 로그를 출력하는 Subscriber 노드.<br>파라미터: `log_prefix` |
| **`demo_bringup`** | Launch/YAML | `demo.launch.py`<br>`params.yaml` | Python 노드와 C++ 노드를 한 번에 실행하고 환경을 동적으로 제어하는 통합 패키지. |

### 주요 구현 모범 사례 (Best Practices)
1. **상대 토픽명 사용 & 토픽 리매핑 (`remappings`)**: 소스코드에서는 상대 경로(`chatter`)를 사용하고 런치 파일에서 인자로 동적 변경.
2. **네임스페이스 격리 (`PushRosNamespace`)**: `PushRosNamespace('demo')`로 노드들을 그룹화하여 관리.
3. **YAML 파라미터 덮어쓰기**: `/**` 와일드카드를 사용해 네임스페이스 변경 시에도 파라미터가 유효하도록 처리하고 `ParameterValue`로 타입 캐스팅.
4. **조건부 실행 (`IfCondition`)**: `use_listener:=false` 옵션을 통해 특정 노드 실행 여부 제어.

---

## 📌 2. ROS 2 빌드 및 패키지 미인식 해결법

### 문제 상황
```bash
Package 'demo_bringup' not found
```

### 원인 및 해결 방법
현재 터미널 환경 변수(`AMENT_PREFIX_PATH`)에 해당 워크스페이스가 등록되어 있지 않아 발생합니다. 빌드 후 `setup.bash`를 로드해야 합니다.

```bash
# 1. 워크스페이스 이동
cd ~/Sparta/workspace/ROS2_WS

# 2. 빌드
colcon build

# 3. 환경 변수 로드 (필수!)
source install/setup.bash

# 4. 실행
ros2 launch demo_bringup demo.launch.py
```

---

## 📌 3. Git & GitHub Push Protection (비밀키 유출) 해결

### 문제 상황
`git push` 시 `GCP API Key Bound to a Service Account` 오류로 GitHub Push가 거부됨.

### 원인
ROS 2 빌드 과정(`colcon build`)에서 생성된 **`build/` 및 `log/` 폴더** 내에 터미널 환경 변수(GCP API Key)가 자동 기록되었고, 이 파일들이 `.gitignore` 설정 문제로 커밋에 포함됨.

### 해결 과정
1. **`.gitignore` 들여쓰기 공백 제거 및 규칙 수정**
   ```gitignore
   # ROS 2 Build / Install / Log outputs
   build/
   install/
   log/
   **/ROS2_WS/build/
   **/ROS2_WS/install/
   **/ROS2_WS/log/
   workspace/ROS2_WS/build/
   workspace/ROS2_WS/install/
   workspace/ROS2_WS/log/
   ```
2. **커밋 히스토리 되돌리기 및 재커밋**
   ```bash
   git reset --soft <이전_정상_커밋>
   git reset
   git add .
   git commit -m "add: ROS2 예제 패키지 및 문서 추가"
   git push origin main && git push sparta main
   ```
   *(결과: `build/`, `install/`, `log/` 제외 및 pure 소스 코드만 정상 푸시 완료)*

---

## 📌 4. VS Code 오류 표시 무시 설정

* **Python (Pylance)**: 해당 줄 뒤에 `# type: ignore` 추가
* **C / C++ (IntelliSense)**: `.vscode/settings.json`에 `"C_Cpp.errorSquiggles": "disabled"` 추가
* **TypeScript / JavaScript**: 코드 상단에 `// @ts-ignore` 추가

---

## 📌 5. Antigravity CLI 실행 명령어

* **기본 실행**: `agy`
* **도움말 확인**: `agy --help`
* **CLI 종료**: `/exit` 또는 `Ctrl` + `D` (두 번)
