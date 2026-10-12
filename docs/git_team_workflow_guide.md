# Git 팀 협업 가이드

> RealSense Tracker / `Lv2_EYE4_Assignment` 팀 프로젝트용\
> 기준 Repository: `SpartaPA/Lv2_EYE4_Assignment`

------------------------------------------------------------------------

## 🧭 Git 가이드 네비게이터

### 🚀 처음 시작

-   [1. Git 협업 구조](#1-git-협업-구조)
-   [2. 최초 Git 환경 설정](#2-최초-git-환경-설정)
-   [3. GitHub SSH 인증 설정](#3-github-ssh-인증-설정)
-   [4. GitHub에 SSH Key 등록](#4-github에-ssh-key-등록)
-   [5. SSH 연결 테스트](#5-ssh-연결-테스트)
-   [6. 프로젝트 디렉토리 관리](#6-프로젝트-디렉토리-관리)
-   [7. 팀 Repository Clone](#7-팀-repository-clone)
-   [8. Remote 확인](#8-remote-확인)
-   [9. 원격 브랜치 확인](#9-원격-브랜치-확인)
-   [10. 기존 개인 브랜치 가져오기](#10-기존-개인-브랜치-가져오기)

### 🌿 Branch 이해

-   [11. Branch의 기본 원리](#11-branch의-기본-원리)
-   [12. fetch / pull / merge](#12-git-fetch-pull-merge)
-   [13. main보다 뒤처진 경우](#13-내-브랜치가-main보다-뒤처진-경우)

### 💻 실제 작업

-   [14. 작업 시작 전 표준 절차](#14-작업-시작-전-표준-절차)
-   [15. 작업 중 Commit](#15-작업-중-commit)
-   [16. Commit 메시지 규칙](#16-commit-메시지-규칙)
-   [17. Push](#17-push)
-   [18. Pull Request](#18-pull-request)

### 🛠️ 문제 해결

-   [19. 다른 팀원의 변경사항 반영](#19-다른-팀원의-변경사항-반영)
-   [20. Merge Conflict](#20-merge-conflict)

### 🤖 ROS 2 프로젝트

-   [21. ROS 2 프로젝트에서 Git에 올리지 않는
    것](#21-ros-2-프로젝트에서-git에-올리지-않는-것)
-   [22. 절대 Git에 올리지 않는 것](#22-절대-git에-올리지-않는-것)
-   [23. RealSense Tracker 작업 예시](#23-realsense-tracker-작업-예시)

### 📋 참고

-   [24. 자주 사용하는 명령어](#24-자주-사용하는-명령어)
-   [25. 기본 작업 명령어 세트](#25-기본-작업-명령어-세트)
-   [26. 전체 협업 흐름](#26-전체-협업-흐름)
-   [27. 핵심 규칙 요약](#27-핵심-규칙-요약)

------------------------------------------------------------------------

# 1. Git 협업 구조

현재 팀 Repository의 브랜치 구조:

``` text
main
├── dev/minhyuk
├── dev/sanghwa
├── dev/sangjun
└── dev/seunghye
```

  브랜치           역할
  ---------------- --------------------------------
  `main`           팀의 기준이 되는 안정적인 코드
  `dev/minhyuk`    개인 작업 브랜치
  `dev/sanghwa`    개인 작업 브랜치
  `dev/sangjun`    희우님 개인 작업 브랜치
  `dev/seunghye`   개인 작업 브랜치

## 기본 원칙

**각자 개인 브랜치에서 작업하고 `main`에는 직접 작업하지 않습니다.**

``` text
개인 작업
   ↓
dev/개인브랜치
   ↓
commit
   ↓
push
   ↓
Pull Request
   ↓
main
```

------------------------------------------------------------------------

# 2. 최초 Git 환경 설정

## Git 설치 확인

``` bash
git --version
```

Git이 없다면:

``` bash
sudo apt update
sudo apt install git -y
```

------------------------------------------------------------------------

# 3. GitHub SSH 인증 설정

팀 프로젝트에서는 HTTPS보다 SSH 방식을 사용하는 것을 권장합니다.

## SSH 키 생성

``` bash
ssh-keygen -t ed25519 -C "GitHub 이메일"
```

기본 경로를 사용하려면 저장 위치 질문에서 `Enter`를 누릅니다.

생성되는 파일:

``` text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

### 중요

``` text
id_ed25519
    └── 개인키
    └── 절대 공유하지 않음

id_ed25519.pub
    └── 공개키
    └── GitHub에 등록
```

공개키 확인:

``` bash
cat ~/.ssh/id_ed25519.pub
```

출력된 한 줄 전체를 복사합니다.

------------------------------------------------------------------------

# 4. GitHub에 SSH Key 등록

GitHub에서:

``` text
Settings
→ SSH and GPG keys
→ New SSH key
```

등록 예시:

``` text
Title:
Raspberry Pi 4 - RealSense Tracker

Key type:
Authentication Key

Key:
id_ed25519.pub 내용 전체
```

------------------------------------------------------------------------

# 5. SSH 연결 테스트

``` bash
ssh -T git@github.com
```

처음 연결할 경우 다음과 같은 질문이 나올 수 있습니다.

``` text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

``` bash
yes
```

성공하면:

``` text
Hi <GitHub username>! You've successfully authenticated,
but GitHub does not provide shell access.
```

이 메시지가 나오면 SSH 인증이 정상적으로 완료된 것입니다.

------------------------------------------------------------------------

# 6. 프로젝트 디렉토리 관리

Raspberry Pi에서 여러 Git 프로젝트를 관리할 때는 `~/Git` 아래에
저장합니다.

``` text
~
└── Git/
    ├── Lv2_EYE4_Assignment/
    ├── 다른 프로젝트/
    └── ...
```

생성:

``` bash
mkdir -p ~/Git
cd ~/Git
```

------------------------------------------------------------------------

# 7. 팀 Repository Clone

GitHub에서:

``` text
Code
→ SSH
```

를 선택합니다.

현재 팀 Repository:

``` text
git@github.com:SpartaPA/Lv2_EYE4_Assignment.git
```

Clone:

``` bash
cd ~/Git
git clone git@github.com:SpartaPA/Lv2_EYE4_Assignment.git
```

이후:

``` bash
cd ~/Git/Lv2_EYE4_Assignment
```

------------------------------------------------------------------------

# 8. Remote 확인

``` bash
git remote -v
```

정상적인 경우:

``` text
origin  git@github.com:SpartaPA/Lv2_EYE4_Assignment.git (fetch)
origin  git@github.com:SpartaPA/Lv2_EYE4_Assignment.git (push)
```

여기서 `origin`은 GitHub의 원격 Repository를 의미합니다.

------------------------------------------------------------------------

# 9. 원격 브랜치 확인

``` bash
git fetch origin
git branch -a
```

예:

``` text
* main
  remotes/origin/main
  remotes/origin/dev/minhyuk
  remotes/origin/dev/sanghwa
  remotes/origin/dev/sangjun
  remotes/origin/dev/seunghye
```

------------------------------------------------------------------------

# 10. 기존 개인 브랜치 가져오기

GitHub에 이미 개인 브랜치가 존재하는 경우:

``` bash
git switch -c dev/sangjun --track origin/dev/sangjun
```

확인:

``` bash
git branch
```

결과:

``` text
* dev/sangjun
  main
```

현재 브랜치와 tracking 상태 확인:

``` bash
git status
```

예:

``` text
On branch dev/sangjun
Your branch is up to date with 'origin/dev/sangjun'.
```

------------------------------------------------------------------------

# 11. Branch의 기본 원리

Git의 기본 구조:

``` text
                  GitHub
                     │
              ┌──────┴──────┐
              │             │
            main       dev/sangjun
              │             │
              │             └── 희우님 작업
              │
              └── 팀 기준 코드
```

개인 작업은:

``` text
dev/sangjun
      │
      ├── 작업
      ├── commit
      └── push
```

작업이 완료되면:

``` text
dev/sangjun
      │
      │ Pull Request
      ▼
    main
```

으로 병합합니다.

------------------------------------------------------------------------

# 12. Git fetch / pull / merge

## `git fetch`

원격 Repository의 최신 정보를 가져옵니다.

``` bash
git fetch origin
```

특징:

``` text
원격 정보 가져오기
        ↓
원격 추적 브랜치 갱신
        ↓
현재 작업 내용에는 직접 반영하지 않음
```

따라서 원격 상태를 확인하고 싶을 때 안전하게 사용할 수 있습니다.

------------------------------------------------------------------------

## `git pull`

현재 브랜치가 추적하는 원격 브랜치의 변경사항을 가져와 현재 브랜치에
반영합니다.

``` bash
git pull
```

일반적으로 다음 두 작업을 합친 개념으로 이해하면 쉽습니다.

``` text
git fetch
+
git merge
```

예를 들어 현재 `dev/sangjun`에서:

``` bash
git pull
```

하면 기본적으로:

``` text
origin/dev/sangjun
```

의 변경사항을 가져옵니다.

**중요:** `git pull`은 자동으로 `main`의 변경사항을 가져오는 명령이
아닙니다.

------------------------------------------------------------------------

## `git merge`

다른 브랜치의 변경사항을 현재 브랜치에 합칩니다.

현재 `dev/sangjun`에서:

``` bash
git merge origin/main
```

하면:

``` text
origin/main
     │
     │ merge
     ▼
dev/sangjun
```

이 됩니다.

------------------------------------------------------------------------

# 13. 내 브랜치가 main보다 뒤처진 경우

GitHub에서:

``` text
This branch is 1 commit behind main.
```

이라고 표시될 수 있습니다.

이는 현재 개인 브랜치가 `main`의 최신 커밋을 가지고 있지 않다는
뜻입니다.

예:

``` text
main
 │
 ├── A
 │
 └── B  ← 최신
       │
       │
dev/sangjun
 └── A
```

## 권장 동기화 방법

현재 `dev/sangjun`에서:

``` bash
git fetch origin
git merge origin/main
```

결과:

``` text
main
 │
 └── B
      │
      │ merge
      ▼
dev/sangjun
```

### 한 줄로도 가능

``` bash
git pull origin main
```

하지만 팀 협업과 Git 학습을 위해 다음처럼 단계별로 실행하는 것을
권장합니다.

``` bash
git fetch origin
git merge origin/main
```

------------------------------------------------------------------------

# 14. 작업 시작 전 표준 절차

매번 작업을 시작할 때 다음 순서를 권장합니다.

## 1. Repository 이동

``` bash
cd ~/Git/Lv2_EYE4_Assignment
```

## 2. 현재 브랜치 확인

``` bash
git branch
```

반드시 본인의 작업 브랜치인지 확인합니다.

``` text
* dev/sangjun
```

## 3. 작업 상태 확인

``` bash
git status
```

## 4. 원격 정보 갱신

``` bash
git fetch origin
```

## 5. main 변경사항 반영

필요한 경우:

``` bash
git merge origin/main
```

## 6. 작업 시작

``` text
코드 작성
↓
테스트
↓
수정
```

------------------------------------------------------------------------

# 15. 작업 중 Commit

하나의 의미 있는 작업 단위를 완료하면 commit합니다.

상태 확인:

``` bash
git status
```

변경사항 확인:

``` bash
git diff
```

파일 추가:

``` bash
git add .
```

Commit:

``` bash
git commit -m "feat: add ROS2 package skeleton"
```

### Commit의 의미

Commit은 GitHub에 업로드하는 것이 아니라 **현재 로컬 Git Repository에
작업 이력을 기록하는 것**입니다.

``` text
코드 수정
   ↓
git add
   ↓
git commit
   ↓
로컬 Git에 기록
   ↓
git push
   ↓
GitHub에 업로드
```

------------------------------------------------------------------------

# 16. Commit 메시지 규칙

권장 형식:

``` text
type: 작업 내용
```

## Type

  Type         용도
  ------------ -----------------------
  `feat`       새로운 기능
  `fix`        버그 수정
  `docs`       문서 수정
  `refactor`   코드 구조 개선
  `test`       테스트 추가/수정
  `chore`      설정, 빌드, 기타 작업

## 예시

새로운 ROS 2 Node:

``` bash
git commit -m "feat: add perception node"
```

버그 수정:

``` bash
git commit -m "fix: correct target position calculation"
```

README 수정:

``` bash
git commit -m "docs: update project architecture"
```

설정 변경:

``` bash
git commit -m "chore: update ROS2 dependencies"
```

------------------------------------------------------------------------

# 17. Push

Commit이 완료되면 자신의 브랜치에 push합니다.

``` bash
git push
```

현재:

``` text
dev/sangjun
```

에서 작업하고 있다면:

``` text
로컬 dev/sangjun
      │
      │ git push
      ▼
GitHub dev/sangjun
```

으로 올라갑니다.

`git push`가 자동으로 `main`에 올라가는 것이 아닙니다.

------------------------------------------------------------------------

# 18. Pull Request

작업이 완료되면 GitHub에서 Pull Request를 생성합니다.

``` text
dev/sangjun
      │
      │ Pull Request
      ▼
    main
```

PR에는 다음 내용을 작성하는 것을 권장합니다.

``` markdown
## 작업 내용

- ROS 2 package skeleton 생성
- 기본 Node 구조 생성
- launch 파일 추가

## 테스트

- colcon build 성공
- tracker.launch.py 실행 확인

## 참고

실제 RealSense / Dynamixel 기능은 다음 단계에서 구현 예정
```

------------------------------------------------------------------------

# 19. 다른 팀원의 변경사항 반영

내 브랜치에서 작업 중인데 `main`에 새로운 작업이 추가되었다면:

``` bash
git fetch origin
git merge origin/main
```

충돌이 없다면 계속 작업합니다.

### 핵심

``` text
main
 │
 │ 최신 팀 코드
 ▼
dev/sangjun
 │
 └── 내 작업
```

내 브랜치에 `main`을 반영하는 것은 **내 작업을 main에 합치는 것과 반대
방향**입니다.

------------------------------------------------------------------------

# 20. Merge Conflict

충돌이 발생하면 Git이 충돌 파일을 표시합니다.

``` bash
git status
```

충돌 파일 내부에는 다음과 같은 표시가 생길 수 있습니다.

``` text
<<<<<<< HEAD
내 코드
=======
다른 브랜치 코드
>>>>>>> origin/main
```

필요한 코드를 선택하여 직접 수정합니다.

수정 후:

``` bash
git add <충돌파일>
```

그리고:

``` bash
git commit
```

합니다.

## 주의

충돌이 발생했다고 무작정:

``` bash
git reset --hard
```

하지 않습니다.

작업 중인 코드가 삭제될 수 있습니다.

------------------------------------------------------------------------

# 21. ROS 2 프로젝트에서 Git에 올리지 않는 것

ROS 2를 빌드하면 다음 디렉토리가 생성됩니다.

``` text
build/
install/
log/
```

이들은 Git에 올리지 않습니다.

## `.gitignore`

``` gitignore
build/
install/
log/

__pycache__/
*.py[cod]

.venv/
venv/

.vscode/

.env
```

------------------------------------------------------------------------

# 22. 절대 Git에 올리지 않는 것

다음 정보는 Repository에 올리지 않습니다.

``` text
개인 SSH Private Key
비밀번호
API Key
Token
.env 비밀정보
개인 인증정보
```

특히:

``` text
~/.ssh/id_ed25519
```

는 절대 Git에 추가하지 않습니다.

GitHub에 등록하는 것은:

``` text
id_ed25519.pub
```

입니다.

------------------------------------------------------------------------

# 23. RealSense Tracker 작업 예시

현재 프로젝트에서 ROS 2 통합 뼈대를 만든다고 가정합니다.

## 작업 시작

``` bash
cd ~/Git/Lv2_EYE4_Assignment

git status
git branch

git fetch origin
git merge origin/main
```

## 코드 작성

예상 구조:

``` text
Lv2_EYE4_Assignment/
├── README.md
├── lv2_module5/
│   └── ...
└── ros2_ws/
    └── src/
        └── realsense_tracker/
            ├── package.xml
            ├── setup.py
            ├── camera_node.py
            ├── perception_node.py
            ├── coordinator_node.py
            └── dynamixel_node.py
```

> 실제 디렉토리 위치는 팀 Repository의 현재 구조와 선생님/팀에서 정한
> 제출 구조를 우선합니다.

## 빌드

ROS 2 workspace에서:

``` bash
colcon build
```

## 테스트

``` bash
source install/setup.bash
ros2 launch realsense_tracker tracker.launch.py
```

## Git 상태 확인

``` bash
git status
```

## Commit

``` bash
git add .
git commit -m "feat: add ROS2 package skeleton"
```

## Push

``` bash
git push
```

------------------------------------------------------------------------

# 24. 자주 사용하는 명령어

  목적                    명령어
  ----------------------- --------------------------
  현재 상태               `git status`
  브랜치 확인             `git branch`
  원격 브랜치 포함 확인   `git branch -a`
  원격 주소 확인          `git remote -v`
  원격 정보 가져오기      `git fetch origin`
  현재 브랜치 pull        `git pull`
  main 변경사항 반영      `git merge origin/main`
  변경사항 확인           `git diff`
  커밋 기록 확인          `git log --oneline`
  파일 추가               `git add .`
  Commit                  `git commit -m "..."`
  원격에 push             `git push`
  브랜치 변경             `git switch <branch>`
  새 브랜치 생성          `git switch -c <branch>`

------------------------------------------------------------------------

# 25. 기본 작업 명령어 세트

앞으로 대부분의 작업은 다음 흐름으로 진행하면 됩니다.

``` bash
# 1. 프로젝트 이동
cd ~/Git/Lv2_EYE4_Assignment

# 2. 현재 브랜치 확인
git branch

# 3. 작업 상태 확인
git status

# 4. 원격 정보 업데이트
git fetch origin

# 5. main 변경사항 반영
git merge origin/main

# 6. 작업
# ...

# 7. 변경사항 확인
git status
git diff

# 8. 테스트
colcon build

# 9. Commit
git add .
git commit -m "feat: 작업 내용"

# 10. Push
git push
```

------------------------------------------------------------------------

# 26. 전체 협업 흐름

``` text
                       GitHub
                          │
                          ▼
                        main
                          │
                          │ fetch / merge
                          ▼
                   dev/sangjun
                          │
                          │
                        작업
                          │
                          ▼
                        commit
                          │
                          ▼
                         push
                          │
                          ▼
                 origin/dev/sangjun
                          │
                          │ Pull Request
                          ▼
                        main
```

## 방향을 기억하기

### main → 개인 브랜치

팀의 최신 코드를 내 작업에 반영:

``` bash
git fetch origin
git merge origin/main
```

### 개인 브랜치 → main

내 작업을 팀 코드에 반영:

``` text
Pull Request
```

------------------------------------------------------------------------

# 27. 핵심 규칙 요약

## ① `main`에서 직접 작업하지 않는다.

``` text
❌ main에서 코드 작성

⭕ dev/sangjun에서 코드 작성
```

## ② 작업 전에 현재 브랜치를 확인한다.

``` bash
git branch
```

## ③ 작업 전에 원격 상태를 확인한다.

``` bash
git fetch origin
```

필요하면:

``` bash
git merge origin/main
```

## ④ 의미 있는 단위로 commit한다.

``` bash
git add .
git commit -m "feat: 작업 내용"
```

## ⑤ 자신의 브랜치에 push한다.

``` bash
git push
```

## ⑥ `main`에 반영할 때는 Pull Request를 사용한다.

``` text
dev/sangjun
      ↓
Pull Request
      ↓
main
```

## ⑦ Private Key와 비밀번호를 절대 Repository에 올리지 않는다.

------------------------------------------------------------------------

# 한 줄 요약

> **항상 개인 브랜치에서 작업하고, 작업 전 `main`의 최신 상태를
> 확인하며, 작은 단위로 commit하고, 자신의 브랜치에 push한 뒤 Pull
> Request를 통해 `main`에 반영합니다.**
