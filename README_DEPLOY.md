# ARION Team Link MVP

팀원들이 링크로 접속해서 함께 보는 ARION Team OS입니다.

## 구조

- Frontend/App: Streamlit
- Shared DB: Supabase
- Access: 팀 공용 비밀번호
- Storage: Supabase `arion_records` 테이블
- Fallback: Supabase 설정 전에는 로컬 CSV

## 왜 이 구조인가?

로컬 CSV는 팀원마다 데이터가 따로 저장됩니다.
공용 링크 버전은 Supabase DB를 써야 팀원들이 같은 데이터를 봅니다.

## 배포 순서

### 1. Supabase 프로젝트 만들기

Supabase에서 새 프로젝트를 만듭니다.

### 2. SQL 실행

`supabase_schema.sql` 내용을 Supabase SQL Editor에서 실행합니다.

### 3. GitHub 저장소 만들기

이 폴더의 파일을 GitHub 저장소에 올립니다.

필수 파일:

```text
app.py
requirements.txt
supabase_schema.sql
.streamlit/secrets.toml.example
docs/
```

`.streamlit/secrets.toml` 실제 파일은 GitHub에 올리지 마세요.

### 4. Streamlit Community Cloud 배포

Streamlit Community Cloud에서 GitHub 저장소를 선택하고 `app.py`를 메인 파일로 배포합니다.

### 5. Secrets 설정

Streamlit 앱의 Advanced settings / Secrets에 아래 형식으로 넣습니다.

```toml
TEAM_PASSWORD = "팀원공유비밀번호"

SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_SERVICE_KEY = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
```

### 6. 앱 접속 후 초기 데이터 넣기

앱에 접속해서 비밀번호 입력 후:

```text
설정 → 초기 샘플 데이터 넣기
```

버튼을 누릅니다.

## 팀원에게 공유할 문구

```text
ARION Team OS 공용 링크입니다.

접속 후 팀 공용 비밀번호를 입력하세요.
먼저 “처음 보는 사람용 안내”를 읽고,
그다음 “팀원 오늘 할 일”에서 본인 이름으로 필터링해서 오늘 해야 할 일을 확인하세요.

완료한 일은 완료 보고에 남기고,
막힌 일은 막힌 일 탭에 적어주세요.
```

## 보안 주의

- Supabase service role key는 GitHub에 올리면 안 됩니다.
- 팀 공용 비밀번호는 외부에 공유하지 마세요.
- 사업자등록증, 통장, 신분증 같은 민감문서는 업로드하지 마세요.
- 결제, 정산, 은행 기능은 아직 만들지 않습니다.
