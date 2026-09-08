# GitHub 협업 플로우 학습 정리

>
>작성일 : 2026-08-05
>
>최종 수정일 : 2026-08-11
>
>학습 목표  
>- Git과 GitHub를 이용한 기본 협업 구조 이해
>

# 1. Git과 GitHub의 역할

|구분|설명|
|---|---|
|Git|버전 관리 프로그램|
|GitHub|Git 저장소를 온라인에서 관리하는 서비스|

쉽게 말하면 다음과 같다.

- Git = 게임 저장 기능
- GitHub = 클라우드 저장소
- Commit = 저장하기
- Branch = 새로운 작업 공간 만들기
- Merge = 작업 내용 합치기

---

# 2. 협업 구조 이해하기

```text
main
 ├── feature/login
 ├── feature/chat
 └── feature/profile
```

- `main` 브랜치
    - 완성된 코드만 보관한다.
    - 직접 수정하지 않는다.

- `feature/*` 브랜치
    - 새로운 기능을 개발한다.
    - 작업이 끝나면 main 브랜치와 합친다.

---

# 3. 전체 협업 흐름

```text
① 저장소 생성
        │
② 팀원 초대
        │
③ 브랜치 생성
        │
④ 기능 개발
        │
⑤ 커밋(Commit)
        │
⑥ 푸시(Push)
        │
⑦ Pull Request 생성
        │
⑧ 코드 검토
        │
⑨ 병합(Merge)
```

---

# 4. 실제 작업 순서

## 저장소 복제

```bash
git clone 저장소_주소
```

---

## 현재 상태 확인

```bash
git status
```

---

## 브랜치 생성

```bash
git branch feature/login
```

---

## 브랜치 이동

```bash
git checkout feature/login
```

또는

```bash
git switch feature/login
```

---

## 파일 추가

```bash
git add .
```

---

## 커밋 생성

```bash
git commit -m "로그인 기능 추가"
```

---

## GitHub에 업로드

```bash
git push origin feature/login
```

---

## 최신 내용 내려받기

```bash
git pull origin main
```

---

# 5. Merge Conflict

## 발생 원인

두 사람이 같은 파일의 같은 부분을 수정했을 때 발생한다.

```text
팀원 A → main.py 수정
팀원 B → main.py 수정

↓

Merge Conflict 발생
```

---

## 해결 방법

1. 충돌 내용을 확인한다.
2. 필요한 부분만 남긴다.
3. 다시 커밋한다.
4. 병합한다.

---

# 6. .gitignore

Git이 추적하지 않을 파일을 지정한다.

예시

```gitignore
venv/
__pycache__/
*.log
.env
```

---

# 7. 협업 시 주의 사항다른 팀원이 이미 코드를 수정했을 수도 있기 때문입니다.

예를 들어,

오전 9시: A 팀원이 코드를 수정함

오전 10시: 희우님이 예전 버전으

❌ 하지 말아야 할 행동

- main 브랜치에서 직접 작업하기
- 커밋 메시지를 의미 없이 작성하기
- 다른 사람의 작업 내용을 덮어쓰기
- 충돌을 무시하고 병합하기

---

⭕ 권장 사항

- 기능별 브랜치 사용하기
- 자주 커밋하기
- 자주 Pull 하기
- Pull Request 활용하기

---

# 8. 오늘의 핵심 정리

```text
clone
   ↓
branch 생성
   ↓
코드 작성
   ↓
add
   ↓
commit
   ↓
push
   ↓
pull request
   ↓
merge
```

"main 브랜치는 보호하고, 각자 브랜치를 만들어 작업한 뒤 병합한다."


---

# 9. 협업 규칙 및 네이밍 컨벤션

## 기본 원칙

- 영어 소문자를 사용한다.
- 공백은 사용하지 않는다.
- 단어 구분에는 하이픈(`-`)을 사용한다.
- 숫자는 필요한 경우에만 사용한다.
- 한글 파일명은 가급적 사용하지 않는다.
- 모든 팀원이 동일한 규칙을 따른다.

---

## 폴더 이름 예시

⭕ 좋은 예시

```text
backend
frontend
user-service
image-upload
api-server
week-01
week-02
```

❌ 좋지 않은 예시

```text
Backend
my Folder
사용자관리
UserService
image_upload
```

---

## 파일 이름 예시

⭕ 좋은 예시

```text
readme.md
install-guide.md
api-document.md
user-profile.js
main.py
```

❌ 좋지 않은 예시

```text
README최종.md
진짜최종본.md
mainFinal.py
New File.txt
```

---

## 브랜치 이름 예시

```text
feature/login
feature/chat
feature/profile

fix/login-error
fix/image-upload

docs/readme-update
```

---

## 커밋 메시지 예시

```text
feat: 로그인 기능 추가
fix: 이미지 업로드 오류 수정
docs: README 수정
refactor: 코드 구조 개선
style: 코드 형식 수정
```

---

## 최종 규칙

```text
소문자 사용
하이픈(-) 사용
일관성 유지
명확한 이름 사용
```

좋은 코드는 읽기 쉽고,
좋은 저장소는 찾기 쉬워야 한다.