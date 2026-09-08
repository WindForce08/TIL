# SSH 학습 정리

> 목적: 온보드 컴퓨터에 원격 접속하고, ROS 2 개발 환경에서 SSH를 활용할 수 있도록 SSH의 핵심 개념과 실전 사용법을 정리한다.

---

## 01. SSH란?

**SSH(Secure Shell)**는 네트워크를 통해 다른 컴퓨터에 안전하게 원격 접속하기 위한 프로토콜이다.

대표적으로 다음 작업에 사용한다.

- 원격 컴퓨터 터미널 접속
- 원격 명령 실행
- 파일 전송
- 포트 포워딩
- 서버/로봇/온보드 컴퓨터 관리

기본 접속 형태:

```bash
ssh 사용자명@호스트주소
```

예:

```bash
ssh pa31@localhost
```

여기서:

- `pa31` → 원격 컴퓨터의 사용자 계정
- `localhost` → 현재 컴퓨터 자신
- SSH 기본 포트 → `22`

---

## 02. SSH 접속 구조

```text
[내 PC]
   │
   │ SSH
   │ TCP 22
   ▼
[원격 컴퓨터]
   └── 사용자 계정
       └── pa31
```

실제 로봇 개발에서는 다음과 같은 구조가 흔하다.

```text
[개발 PC]
    │
    │ SSH
    ▼
[로봇/UGV 온보드 컴퓨터]
    │
    ├── ROS 2 Node
    ├── 센서 드라이버
    ├── 카메라
    └── 모터/제어 프로그램
```

즉, 개발 PC에서 로봇의 온보드 컴퓨터에 SSH로 들어가 직접 명령을 실행하고 프로그램을 관리할 수 있다.

---

## 03. 비밀번호 인증 vs 공개키 인증

SSH 인증 방식은 여러 가지가 있지만 실습에서 가장 많이 접하는 방식은 다음 두 가지다.

### 비밀번호 인증

```text
ssh pa31@robot

Password:
********
```

서버가 사용자의 계정 비밀번호를 확인한다.

### 공개키 인증

```text
ssh pa31@robot
```

비밀번호를 입력하지 않고 개인키를 이용해 인증한다.

이 방식이 흔히 말하는 **SSH 무비밀번호 접속**이다.

단, "무비밀번호"라는 표현은 **계정 비밀번호를 입력하지 않는다**는 의미다.

개인키 자체에 passphrase가 설정되어 있다면 개인키 암호를 입력할 수 있다.

---

# 04. 개인키·공개키

SSH 키 인증에서는 한 쌍의 키를 사용한다.

```text
개인키(Private Key) 🔑
    └── 내가 안전하게 보관

공개키(Public Key) 🔒
    └── 서버에 등록
```

### 핵심 원칙

> **공개키는 서버에 등록하고, 개인키는 절대 서버에 보내지 않는다.**

일반적인 파일 이름:

```text
~/.ssh/id_ed25519          # 개인키
~/.ssh/id_ed25519.pub      # 공개키
```

서버에는 보통 다음 파일에 공개키가 등록된다.

```text
~/.ssh/authorized_keys
```

예:

```text
/home/pa31/.ssh/authorized_keys
```

---

## 05. 자물쇠 비유

공개키와 개인키는 다음처럼 생각하면 이해하기 쉽다.

```text
공개키 = 누구에게나 나눠줄 수 있는 자물쇠
개인키 = 그 자물쇠와 연결된 나만의 열쇠
```

다만 SSH 로그인에서는 단순히 "상자를 잠그고 보내는 것"이 목적은 아니다.

핵심은:

> **서버가 내가 올바른 개인키를 가지고 있다는 사실을 공개키를 이용해 검증하는 것**

이다.

```text
[클라이언트]                         [서버]

개인키 🔑                            공개키 🔒
   │                                    │
   │──── 인증 요청 ────────────────────>│
   │                                    │
   │ 개인키를 이용해                    │
   │ 인증에 필요한 증명 생성            │
   │                                    │
   │──── 인증 증명 ────────────────────>│
   │                                    │
   │                       공개키로 검증 │
   │                                    │
   │<──────── 인증 성공 ────────────────│
```

개인키 자체가 서버로 전달되는 것이 아니라는 점이 중요하다.

---

# 06. SSH 키 생성

현재 PC에서 새로운 SSH 키를 생성할 수 있다.

권장 예:

```bash
ssh-keygen -t ed25519
```

일반적으로 다음 파일이 생성된다.

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

확인:

```bash
ls -la ~/.ssh/
```

공개키 확인:

```bash
cat ~/.ssh/id_ed25519.pub
```

개인키는 외부에 공개하면 안 된다.

```bash
cat ~/.ssh/id_ed25519
```

이 파일의 내용을 다른 사람에게 전달하거나 GitHub/GitLab 등에 올리면 안 된다.

---

# 07. 공개키를 서버에 등록하기

가장 편한 방법:

```bash
ssh-copy-id pa31@robot-ip
```

예:

```bash
ssh-copy-id pa31@192.168.1.100
```

이 명령은 클라이언트의 공개키를 서버의:

```text
~/.ssh/authorized_keys
```

에 추가한다.

이후:

```bash
ssh pa31@192.168.1.100
```

로 접속할 수 있다.

---

# 08. authorized_keys

서버에서 확인:

```bash
cat ~/.ssh/authorized_keys
```

여기에 클라이언트의 공개키가 들어 있다.

구조는 대략 다음과 같다.

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... 사용자@컴퓨터
```

여러 컴퓨터에서 접속한다면 여러 공개키를 등록할 수 있다.

```text
ssh-ed25519 AAAA... laptop
ssh-ed25519 BBBB... desktop
ssh-ed25519 CCCC... robot-dev-pc
```

각각에 대응하는 개인키를 가진 장치만 인증할 수 있다.

---

# 09. SSH 접속 로그 확인

Ubuntu에서는 SSH 인증 로그를 확인할 수 있다.

```bash
sudo grep "Accepted" /var/log/auth.log
```

최근 기록:

```bash
sudo grep "Accepted" /var/log/auth.log | tail -20
```

예:

```text
Accepted publickey for pa31 from 127.0.0.1 port 12345 ssh2
```

### 로그에서 확인할 것

```text
Accepted publickey
```

→ 공개키 인증 성공

```text
Accepted password
```

→ 비밀번호 인증 성공

현재 SSH 서비스 로그는 다음으로도 확인할 수 있다.

```bash
sudo journalctl -u ssh
```

---

# 10. SSH 설정 파일

SSH는 크게 두 종류의 설정을 구분하면 좋다.

### 클라이언트 설정

```text
~/.ssh/config
```

예:

```text
Host robot
    HostName 192.168.1.100
    User pa31
    IdentityFile ~/.ssh/id_ed25519
```

이후:

```bash
ssh robot
```

만 입력해도 된다.

### 서버 설정

```text
/etc/ssh/sshd_config
```

SSH 서버의 인증 방식, 포트 등의 설정을 관리한다.

설정 변경 후에는 보통 SSH 서비스를 재시작한다.

```bash
sudo systemctl restart ssh
```

실제 운영 환경에서는 설정을 변경하기 전에 문법과 기존 접속 가능 여부를 확인하는 것이 중요하다.

---

# 11. SSH로 파일 전송하기

SSH는 원격 터미널 접속뿐 아니라 파일 전송에도 사용할 수 있다.

## SCP

로컬 → 원격:

```bash
scp my_file.py pa31@192.168.1.100:~/workspace/
```

원격 → 로컬:

```bash
scp pa31@192.168.1.100:~/workspace/result.txt .
```

디렉터리 전체:

```bash
scp -r my_package pa31@192.168.1.100:~/ros2_ws/src/
```

---

# 12. SSH와 rsync

ROS 2 개발에서는 코드나 파일을 반복적으로 옮겨야 하는 경우가 많다.

이때 `rsync`가 편리하다.

```bash
rsync -avz ./my_package/ pa31@192.168.1.100:~/ros2_ws/src/my_package/
```

장점:

- 변경된 파일 위주로 전송
- 반복적인 동기화에 유리
- 큰 프로젝트에서 SCP보다 편리할 수 있음

---

# 13. ROS 2에서 SSH를 사용하는 이유

ROS 2에서는 개발 PC와 로봇의 온보드 컴퓨터를 분리해서 사용하는 경우가 많다.

```text
┌──────────────────────┐
│ 개발 PC               │
│                      │
│ VS Code              │
│ 코드 작성             │
│ 빌드                  │
└──────────┬───────────┘
           │
           │ SSH
           ▼
┌──────────────────────┐
│ 로봇 온보드 컴퓨터     │
│                      │
│ Ubuntu               │
│ ROS 2                │
│ Camera Driver        │
│ LiDAR Driver         │
│ Motor Controller     │
└──────────────────────┘
```

SSH를 이용하면 로봇에 직접 모니터와 키보드를 연결하지 않고도 온보드 컴퓨터를 관리할 수 있다.

---

# 14. ROS 2 예시 ① 온보드 컴퓨터 접속

로봇의 IP가:

```text
192.168.1.100
```

이고 계정이:

```text
pa31
```

이라면:

```bash
ssh pa31@192.168.1.100
```

접속 후:

```bash
source /opt/ros/humble/setup.bash
```

워크스페이스가 있다면:

```bash
source ~/ros2_ws/install/setup.bash
```

ROS 2 노드 확인:

```bash
ros2 node list
```

토픽 확인:

```bash
ros2 topic list
```

---

# 15. ROS 2 예시 ② 원격으로 노드 실행

SSH로 로봇에 접속한 뒤:

```bash
ros2 run my_robot_pkg my_node
```

개발 PC에서 직접 실행한 것처럼 보이지만 실제 프로그램은 **온보드 컴퓨터에서 실행**된다.

```text
개발 PC
   │
   │ SSH
   ▼
온보드 컴퓨터
   │
   └── ros2 run my_robot_pkg my_node
```

---

# 16. ROS 2 예시 ③ 코드 수정 → 로봇으로 전송 → 빌드

개발 PC:

```bash
rsync -avz ./my_robot_pkg/ \
pa31@192.168.1.100:~/ros2_ws/src/my_robot_pkg/
```

온보드 컴퓨터:

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_pkg
source install/setup.bash
```

실행:

```bash
ros2 run my_robot_pkg my_node
```

이 방식은 간단한 ROS 2 개발 환경에서 자주 사용할 수 있는 기본적인 작업 흐름이다.

---

# 17. ROS 2 예시 ④ SSH + VS Code

VS Code의 Remote SSH 기능을 사용하면 개발 PC에서 원격 컴퓨터의 파일을 직접 편집할 수 있다.

개념적으로:

```text
[개발 PC]
VS Code
   │
   │ SSH
   ▼
[온보드 컴퓨터]
~/ros2_ws/
```

그러면 온보드 컴퓨터에 있는 ROS 2 패키지를 마치 로컬 파일처럼 편집할 수 있다.

이 방식은 다음과 같은 상황에서 특히 편리하다.

- 로봇에 직접 모니터를 연결하기 어려움
- 온보드 컴퓨터의 GPU/센서를 사용해야 함
- 실제 로봇 환경에서 코드를 실행해야 함
- 개발 PC와 로봇의 파일을 계속 복사하기 번거로움

---

# 18. ROS 2에서 SSH와 ROS 2 통신은 서로 다르다

중요한 구분이다.

```text
SSH
└── 컴퓨터에 원격으로 로그인/관리

ROS 2 DDS
└── 노드끼리 토픽/서비스/액션 등을 통해 통신
```

예를 들어:

```text
[개발 PC]
    │
    │ SSH
    ▼
[온보드 컴퓨터]
    │
    │ ROS 2 / DDS
    ├──────────► Camera Node
    ├──────────► LiDAR Node
    └──────────► Motor Node
```

SSH가 ROS 2 통신을 대신하는 것은 아니다.

SSH는 주로 **컴퓨터에 들어가서 명령을 실행하고 관리하기 위한 통로**이고, ROS 2는 **실행 중인 노드들 사이의 통신을 담당**한다.

---

# 19. ROS 2에서 자주 발생하는 구조

실제 로봇에서는 다음과 같은 구성이 가능하다.

```text
                  ┌─────────────────┐
                  │    개발 PC       │
                  │                 │
                  │ VS Code         │
                  │ RViz            │
                  │ 터미널          │
                  └───────┬─────────┘
                          │
                         SSH
                          │
                          ▼
                  ┌─────────────────┐
                  │ 온보드 컴퓨터     │
                  │                 │
                  │ ROS 2           │
                  │                 │
                  │ Camera Node     │
                  │ LiDAR Node      │
                  │ Control Node    │
                  └───────┬─────────┘
                          │
                  ┌───────┴────────┐
                  ▼                ▼
              Camera           Motor
```

개발 PC에서는 SSH를 통해 온보드 컴퓨터를 관리하고, ROS 2 DDS를 통해 필요한 ROS 2 노드들과 통신할 수 있다.

---

# 20. SSH 포트 포워딩

SSH는 단순한 원격 로그인 외에도 네트워크 연결을 전달할 수 있다.

대표적인 옵션:

```bash
ssh -L 로컬포트:목적지:목적지포트 user@server
```

예를 들어 원격 컴퓨터의 특정 서비스를 로컬 포트로 전달할 수 있다.

ROS 2 자체의 일반적인 통신은 DDS 네트워크 설정을 따르므로, ROS 2 전체 통신을 단순 SSH 포트 포워딩 하나로 해결할 수 있다고 생각하면 안 된다.

---

# 21. SSH 보안에서 기억할 것

### 개인키

```text
~/.ssh/id_ed25519
```

- 절대 공개하지 않는다.
- GitHub 등에 업로드하지 않는다.
- 다른 사람에게 전달하지 않는다.
- 가능하면 passphrase를 사용한다.

### 공개키

```text
~/.ssh/id_ed25519.pub
```

- 서버에 등록한다.
- `authorized_keys`에 저장한다.
- 공개되어도 개인키 자체가 노출되는 것은 아니다.

### 서버

```text
~/.ssh/authorized_keys
```

- 로그인 허용 키 목록
- 불필요한 키는 삭제
- 서버의 `.ssh` 권한을 적절하게 유지

---

# 22. 자주 사용하는 명령어 정리

## SSH 접속

```bash
ssh user@host
```

## 상세 접속 과정 확인

```bash
ssh -v user@host
```

더 자세히:

```bash
ssh -vvv user@host
```

키 인증 문제를 디버깅할 때 매우 유용하다.

## 공개키 등록

```bash
ssh-copy-id user@host
```

## 키 확인

```bash
ls -la ~/.ssh/
```

## 서버의 등록 키 확인

```bash
cat ~/.ssh/authorized_keys
```

## SSH 로그 확인

```bash
sudo grep "Accepted" /var/log/auth.log
```

## 서비스 상태

```bash
sudo systemctl status ssh
```

## 파일 복사

```bash
scp file user@host:~/path/
```

## 파일 동기화

```bash
rsync -avz ./folder/ user@host:~/folder/
```

---

# 23. SSH 문제를 만났을 때 확인 순서

```text
1. 네트워크 연결 확인
        ↓
2. SSH 서버가 실행 중인지 확인
        ↓
3. 사용자명/IP 확인
        ↓
4. 포트 확인
        ↓
5. 공개키 등록 여부 확인
        ↓
6. 개인키 사용 여부 확인
        ↓
7. SSH 로그 확인
```

대표적인 디버깅 명령:

```bash
ssh -vvv pa31@192.168.1.100
```

서버에서는:

```bash
sudo journalctl -u ssh
```

또는:

```bash
sudo grep sshd /var/log/auth.log
```

---

# 24. SSH와 ROS 2를 함께 사용할 때의 전체 흐름

ROS 2 로봇 개발에서 다음 흐름을 익혀두면 좋다.

```text
① 개발 PC에서 코드 작성
        ↓
② SSH로 온보드 컴퓨터 접속
        ↓
③ 코드 전달 또는 Remote SSH로 직접 편집
        ↓
④ 온보드 컴퓨터에서 colcon build
        ↓
⑤ ROS 2 노드 실행
        ↓
⑥ ros2 topic / node / service 등으로 상태 확인
        ↓
⑦ 필요하면 다시 코드 수정
```

예:

```bash
ssh pa31@192.168.1.100

cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash

ros2 node list
ros2 topic list

ros2 run my_robot_pkg my_node
```

---

# 25. 핵심 개념 한 장 정리

```text
SSH
│
├── 원격 컴퓨터 접속
│      └── ssh user@host
│
├── 인증
│      ├── Password
│      └── Public Key
│             ├── 개인키 → 클라이언트 보관
│             └── 공개키 → 서버 등록
│
├── 파일 전송
│      ├── scp
│      └── rsync
│
├── 원격 개발
│      └── VS Code Remote SSH
│
└── ROS 2
       ├── 온보드 컴퓨터 관리 → SSH
       ├── 코드/패키지 전달 → SCP / rsync
       ├── 프로그램 실행 → SSH 터미널
       └── 노드 간 통신 → ROS 2 DDS
```

## 핵심 문장

> **SSH는 다른 컴퓨터를 원격으로 관리하기 위한 통신 방법이고, ROS 2는 실행 중인 로봇 소프트웨어들이 서로 통신하기 위한 프레임워크다.**

> **SSH 공개키 인증에서는 공개키를 서버에 등록하고, 개인키는 클라이언트가 안전하게 보관한다.**

> **ROS 2 개발에서는 SSH를 이용해 온보드 컴퓨터에 접속하고, 그 위에서 ROS 2 노드를 빌드·실행·관리하는 방식으로 활용할 수 있다.**
