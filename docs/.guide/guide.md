# GitHub SSH 연결

## 1. SSH 키 생성

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

> Enter만 눌러 기본 경로(`~/.ssh/id_ed25519`)를 사용합니다.

---

## 2. SSH 에이전트 실행 및 키 등록

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## 3. 공개 키 복사

```bash
cat ~/.ssh/id_ed25519.pub
```

출력된 내용을 복사하여 **GitHub → Settings → SSH and GPG keys → New SSH key**에 등록합니다.

---

## 4. 연결 확인

```bash
ssh -T git@github.com
```

성공 시 다음과 비슷한 메시지가 출력됩니다.

```text
Hi <GitHub_ID>! You've successfully authenticated...
```

---

# 로컬 프로젝트와 GitHub 연결

## 1. Git 초기화

```bash
git init
```

---

## 2. 원격 저장소 연결

```bash
git remote add origin git@github.com:<GitHub_ID>/<Repository>.git
```

확인

```bash
git remote -v
```

---

## 3. 최초 업로드

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

---

# 이후 작업

변경사항 저장

```bash
git add .
git commit -m "Commit message"
```

원격 저장소 최신 내용 가져오기

```bash
git pull origin main
```

업로드

```bash
git push origin main
```
