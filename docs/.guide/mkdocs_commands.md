# MkDocs & GitHub TIL 관리 가이드

---

# 1. 기본 이동 명령어

현재 위치 확인

```bash
pwd
```

파일 목록 확인

```bash
ls
```

폴더 이동

```bash
cd 폴더명
```

상위 폴더로 이동

```bash
cd ..
```

홈 디렉터리로 이동

```bash
cd ~
```

---

# 2. 파일 및 폴더 생성

폴더 생성

```bash
mkdir 폴더명
```

여러 폴더 생성

```bash
mkdir -p 폴더1/폴더2
```

파일 생성

```bash
touch 파일명.md
```

---

# 3. 문서 편집

파일 열기

```bash
nano 파일명.md
```

저장

```text
Ctrl + O
```

저장 후 종료

```text
Enter
Ctrl + X
```

잘라내기

```text
Ctrl + K
```

붙여넣기

```text
Ctrl + U
```

검색하기

```text
Ctrl + W
```

---

# 4. MkDocs 명령어

프로젝트 생성

```bash
mkdocs new .
```

개발 서버 실행

```bash
mkdocs serve
```

사이트 빌드

```bash
mkdocs build
```

버전 확인

```bash
mkdocs --version
```

---

# 5. 가상 환경 명령어

가상 환경 생성

```bash
python3 -m venv venv
```

가상 환경 실행

```bash
source venv/bin/activate
```

가상 환경 종료

```bash
deactivate
```

---

# 6. Git 명령어

상태 확인

```bash
git status
```

파일 추가

```bash
git add .
```

커밋 생성

```bash
git commit -m "메시지"
```

원격 저장소 업로드

```bash
git push
```

---

# 7. 원격 저장소 관리

현재 원격 저장소 확인

```bash
git remote -v
```

원격 저장소 주소 변경

```bash
git remote set-url origin 주소
```

SSH 연결 확인

```bash
ssh -T git@github.com
```

---

# 8. Git 저장소 구조

```text
~/Git
├── TIL
├── SpartaPA
└── Project
```

- Git 폴더는 단순한 상위 폴더다.
- TIL과 SpartaPA는 각각 독립적인 Git 저장소다.
- 각 저장소에는 별도의 .git 폴더가 존재한다.

---

# 9. 자주 사용하는 작업 순서

파일 수정

```bash
nano 파일명.md
```

상태 확인

```bash
git status
```

파일 추가

```bash
git add .
```

커밋 생성

```bash
git commit -m "메시지"
```

GitHub 업로드

```bash
git push
```

---

# 10. 자주 발생하는 오류

tree 설치

```bash
sudo apt install tree
```

venv 설치

```bash
sudo apt install python3-venv
```

패키지 설치

```bash
pip install 패키지명
```

---

# 11. 개인 규칙

- 파일명은 영어로 작성한다.
- 폴더명은 소문자를 사용한다.
- 공백 대신 언더바(_)를 사용한다.
- 하루에 하나 이상의 문서를 작성한다.





