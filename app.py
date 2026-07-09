
from __future__ import annotations

import os
import re
import json
import uuid
import hmac
import hashlib
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import streamlit as st

try:
    from supabase import create_client
except Exception:
    create_client = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

st.set_page_config(page_title="ARION Team OS", page_icon="👥", layout="wide")

# -----------------------------
# UI
# -----------------------------
st.markdown(
    """
<style>
:root {
  --bg: #f6f7fb;
  --card: #ffffff;
  --border: #e5e7eb;
  --text: #111827;
  --muted: #6b7280;
  --primary: #4f46e5;
  --primary-dark: #3730a3;
  --primary-soft: #eef2ff;
  --green: #059669;
  --red: #dc2626;
  --yellow: #d97706;
}
.stApp { background: var(--bg) !important; color: var(--text) !important; }
.block-container { max-width: 1480px !important; padding-top: 1.35rem !important; padding-bottom: 4rem !important; }
header[data-testid="stHeader"] { background: transparent !important; }
h1, h2, h3, h4, h5, h6 { color: var(--text) !important; letter-spacing: -0.03em; }
p, span, div, label { color: var(--text); }

.arion-header {
  background: linear-gradient(135deg, #ffffff 0%, #eef2ff 100%);
  border: 1px solid #dbeafe;
  border-radius: 28px;
  padding: 30px 34px;
  margin-bottom: 24px;
  box-shadow: 0 16px 45px rgba(79,70,229,.08);
}
.arion-title { font-size: 2.15rem; line-height: 1.15; font-weight: 950; color: #111827; letter-spacing: -0.055em; margin-bottom: 10px; }
.arion-subtitle { color: #4b5563; font-size: 1.02rem; line-height: 1.65; margin: 0; }

.arion-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 22px;
  padding: 22px 24px;
  margin: 14px 0;
  box-shadow: 0 10px 28px rgba(15,23,42,.045);
}
.arion-card h3 { margin-top: 0; color: #111827 !important; }

.login-guide {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 22px;
  padding: 20px 22px;
  margin: 12px 0 18px 0;
  box-shadow: 0 10px 28px rgba(15,23,42,.045);
}
.login-guide-title { font-size: 1.15rem; font-weight: 950; color: #111827; margin-bottom: 6px; }
.login-guide-desc { color: #6b7280; line-height: 1.6; }

[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label {
  color: #111827 !important;
  font-weight: 850 !important;
  font-size: .95rem !important;
}
input, textarea {
  background: #ffffff !important;
  color: #111827 !important;
  border-radius: 14px !important;
  border: 1px solid #d1d5db !important;
}
input:focus, textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(79,70,229,.12) !important;
}
.stButton > button,
button[kind="primary"],
button[data-testid="baseButton-primary"] {
  min-height: 42px !important;
  border-radius: 14px !important;
  border: 1px solid var(--primary) !important;
  background: var(--primary) !important;
  color: #ffffff !important;
  font-weight: 900 !important;
  padding: .55rem 1.15rem !important;
  box-shadow: 0 8px 18px rgba(79,70,229,.20);
}
.stButton > button:hover,
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
  background: var(--primary-dark) !important;
  border-color: var(--primary-dark) !important;
  color: #ffffff !important;
}
.stButton > button *, button[kind="primary"] *, button[data-testid="baseButton-primary"] * { color: #ffffff !important; }
[data-testid="stFormSubmitButton"] button {
  min-height: 42px !important;
  border-radius: 14px !important;
  border: 1px solid var(--primary) !important;
  background: var(--primary) !important;
  color: #ffffff !important;
  font-weight: 900 !important;
}
[data-testid="stFormSubmitButton"] button * { color: #ffffff !important; }

[data-testid="stMetric"] {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 20px !important;
  padding: 18px !important;
  box-shadow: 0 10px 28px rgba(15,23,42,.045);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-weight: 800 !important; }
[data-testid="stMetricValue"] { color: #111827 !important; font-size: 1.65rem !important; font-weight: 950 !important; }

.stTabs [data-baseweb="tab-list"] {
  gap: 8px;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 8px;
  box-shadow: 0 10px 28px rgba(15,23,42,.04);
  overflow-x: auto;
}
.stTabs [data-baseweb="tab"] {
  background: #f9fafb;
  border-radius: 13px;
  padding: 10px 14px;
  color: #374151;
  font-weight: 850;
}
.stTabs [aria-selected="true"] { background: var(--primary-soft) !important; color: var(--primary) !important; }

[data-testid="stDataFrame"], [data-testid="stDataEditor"] {
  border-radius: 20px !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
  background: #ffffff !important;
  box-shadow: 0 10px 28px rgba(15,23,42,.04);
}
div[data-testid="stAlert"] { border-radius: 18px !important; border: 1px solid var(--border) !important; }

.badge { display:inline-block; border-radius:999px; padding:4px 10px; font-weight:900; font-size:.78rem; }
.high { background:#fef2f2; color:#b91c1c; border:1px solid #fecaca; }
.medium { background:#fffbeb; color:#92400e; border:1px solid #fde68a; }
.low { background:#ecfdf5; color:#047857; border:1px solid #a7f3d0; }

section[data-testid="stSidebar"] { background: #ffffff !important; }
</style>
""",
    unsafe_allow_html=True,
)

def header(title: str, subtitle: str):
    st.markdown(
        f"""
<div class="arion-header">
  <div class="arion-title">{title}</div>
  <p class="arion-subtitle">{subtitle}</p>
</div>
""",
        unsafe_allow_html=True,
    )

def card(title: str, body: str):
    st.markdown(
        f"""
<div class="arion-card">
<h3>{title}</h3>
<div>{body}</div>
</div>
""",
        unsafe_allow_html=True,
    )

# -----------------------------
# Secrets
# -----------------------------
def get_secret(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, os.environ.get(name, default))
    except Exception:
        return os.environ.get(name, default)

TEAM_PASSWORD = get_secret("TEAM_PASSWORD", "change-me")
INVITE_CODE = get_secret("INVITE_CODE", TEAM_PASSWORD)
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_SERVICE_KEY = get_secret("SUPABASE_SERVICE_KEY")
NVIDIA_API_KEY = get_secret("NVIDIA_API_KEY")
NVIDIA_MODEL = get_secret("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")

# -----------------------------
# Schemas
# -----------------------------
SCHEMAS: Dict[str, List[str]] = {
    "team_users": ["user_id","email","name","role","area","projects","password_hash","status","is_admin","created_at","last_login","mindset_goal","strength","weakness","memo"],
    "team_members": ["name","role","area","projects","contact","status","today_priority","memo"],
    "team_daily_actions": ["date","owner","owner_email","area","project","task","goal","revenue_link","priority","status","estimated_minutes","actual_result","blocker","help_request","next_action","founder_review","ai_feedback","memo"],
    "mindset_checkins": ["date","owner","owner_email","energy","focus","today_commitment","worry","support_needed","ai_feedback","created_at"],
    "ai_feedback_logs": ["date","owner","owner_email","feedback_type","input_summary","ai_feedback","created_at"],
    "app_portfolio": ["project_name","type","status","core_role","revenue_model","connected_sns","current_metric","next_action","priority","memo"],
    "revenue_streams": ["revenue_source","linked_project","revenue_type","status","expected_revenue","actual_revenue","cost","net_profit","required_preparation","risk","next_action","priority","memo"],
    "social_marketing": ["campaign_name","source_content","linked_project","linked_offer","channel","format","hook","status","upload_date","views","saves","comments","clicks","inquiries","sales","next_action","memo"],
    "commerce_tests": ["product_name","sales_method","category","source","cost_price","expected_price","shipping_fee","expected_margin","certification_risk","cs_risk","return_risk","content_potential","test_status","linked_content","result","next_action","memo"],
    "blockers": ["date","owner","owner_email","project","blocker","needed_help","urgency","status","founder_decision_required","ai_feedback","resolution_memo"],
    "completion_reports": ["date","owner","owner_email","project","completed_task","result","proof_link","next_task","ai_feedback","memo"],
    "weekly_team_goals": ["week","team_goal","focus_project","focus_revenue_stream","content_target","product_target","revenue_target","status","memo"],
}

def empty_df(key: str) -> pd.DataFrame:
    return pd.DataFrame(columns=SCHEMAS[key])

@st.cache_resource
def get_supabase():
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY or create_client is None:
        return None
    clean_url = SUPABASE_URL.rstrip("/")
    if clean_url.endswith("/rest/v1"):
        clean_url = clean_url.replace("/rest/v1", "")
    return create_client(clean_url, SUPABASE_SERVICE_KEY)

LOCAL_DIR = Path(__file__).resolve().parent / "data"
LOCAL_DIR.mkdir(exist_ok=True)

def local_path(key: str) -> Path:
    return LOCAL_DIR / f"{key}.csv"

def normalize_df(key: str, df: pd.DataFrame) -> pd.DataFrame:
    for col in SCHEMAS[key]:
        if col not in df.columns:
            df[col] = ""
    keep = ["_record_id"] + SCHEMAS[key] if "_record_id" in df.columns else SCHEMAS[key]
    return df[keep]

def load_table(key: str, show_error: bool = False) -> pd.DataFrame:
    client = get_supabase()
    if client:
        try:
            res = client.table("arion_records").select("id,data").eq("table_key", key).order("id").execute()
            rows = []
            for item in res.data:
                d = item.get("data") or {}
                d["_record_id"] = item.get("id")
                rows.append(d)
            return normalize_df(key, pd.DataFrame(rows)) if rows else empty_df(key)
        except Exception as e:
            if show_error:
                st.error(f"Supabase에서 {key} 불러오기 실패: {e}")
    p = local_path(key)
    if p.exists():
        try:
            return normalize_df(key, pd.read_csv(p, encoding="utf-8-sig"))
        except Exception:
            return empty_df(key)
    return empty_df(key)

def save_table(key: str, df: pd.DataFrame, show_success: bool = True):
    df = normalize_df(key, df.copy())
    client = get_supabase()
    data_records = []
    for _, row in df.iterrows():
        clean = {col: ("" if pd.isna(row.get(col)) else row.get(col)) for col in SCHEMAS[key]}
        data_records.append({"table_key": key, "data": clean})

    if client:
        try:
            client.table("arion_records").delete().eq("table_key", key).execute()
            if data_records:
                client.table("arion_records").insert(data_records).execute()
            if show_success:
                st.success("공용 DB에 저장했습니다.")
            return True
        except Exception as e:
            st.error(f"Supabase 저장 실패: {e}")
            return False

    df.to_csv(local_path(key), index=False, encoding="utf-8-sig")
    if show_success:
        st.success("로컬 CSV에 저장했습니다. Supabase 설정 전에는 팀원들과 자동 공유되지 않습니다.")
    return True

# -----------------------------
# Auth helpers
# -----------------------------
def clean_email(email: str) -> str:
    return (email or "").strip().lower()

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def make_password_record(password: str) -> str:
    salt = uuid.uuid4().hex
    return f"{salt}${hash_password(password, salt)}"

def verify_password(password: str, record: str) -> bool:
    try:
        salt, hashed = record.split("$", 1)
        return hmac.compare_digest(hash_password(password, salt), hashed)
    except Exception:
        return False

def get_users() -> pd.DataFrame:
    return load_table("team_users")

def save_users(df: pd.DataFrame):
    return save_table("team_users", df)

def get_current_user() -> Optional[dict]:
    return st.session_state.get("user")

def is_admin() -> bool:
    user = get_current_user() or {}
    return str(user.get("is_admin", "")).lower() in ["true","1","yes","y"] or user.get("role") == "대표"

# -----------------------------
# AI helper
# -----------------------------
def ai_available() -> bool:
    return bool(NVIDIA_API_KEY and OpenAI is not None)

def call_nvidia_ai(prompt: str) -> str:
    if not ai_available():
        return "NVIDIA AI가 아직 연결되지 않았습니다. Streamlit Secrets에 NVIDIA_API_KEY를 넣으면 자동 피드백이 활성화됩니다."
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_API_KEY,
        )
        resp = client.chat.completions.create(
            model=NVIDIA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 ARION Team OS의 팀 코치다. "
                        "팀원의 업무를 비난하지 말고, 짧고 구체적으로 동기부여와 다음 행동을 제안한다. "
                        "한국어로 답한다. 금전/법률/의료 판단은 확정적으로 말하지 않는다. "
                        "답변 형식은 1) 오늘의 핵심 2) 바로 할 일 3개 3) 주의할 점 으로 한다."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            max_tokens=700,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"NVIDIA AI 호출 실패: {e}"

def log_ai_feedback(owner: str, owner_email: str, feedback_type: str, input_summary: str, ai_feedback: str):
    logs = load_table("ai_feedback_logs")
    row = pd.DataFrame([{
        "date": str(date.today()),
        "owner": owner,
        "owner_email": owner_email,
        "feedback_type": feedback_type,
        "input_summary": input_summary[:1000],
        "ai_feedback": ai_feedback,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }])
    save_table("ai_feedback_logs", pd.concat([logs.drop(columns=["_record_id"], errors="ignore"), row], ignore_index=True), show_success=False)

# -----------------------------
# Seed data
# -----------------------------
def seed_data():
    today = str(date.today())
    week = f"{date.today().isocalendar().year}-W{date.today().isocalendar().week}"
    samples = {
        "team_members": pd.DataFrame([
            {"name":"대표","role":"대표","area":"전체전략/최종결정","projects":"ARION 전체","contact":"내부","status":"active","today_priority":"수익흐름 결정","memo":"최종 승인자"},
            {"name":"개발담당","role":"개발","area":"앱/자동화","projects":"Growth OS, Seller OS, AI Engine","contact":"내부","status":"standby","today_priority":"공용 링크 버전 안정화","memo":""},
            {"name":"콘텐츠담당","role":"콘텐츠","area":"SNS/숏폼","projects":"AETHER, VEIL, AURA","contact":"내부","status":"standby","today_priority":"숏폼 대본/업로드","memo":""},
            {"name":"상품담당","role":"상품소싱","area":"위탁판매/구매대행","projects":"Seller OS","contact":"내부","status":"standby","today_priority":"저위험 상품 후보 조사","memo":""},
        ]),
        "team_daily_actions": pd.DataFrame([
            {"date":today,"owner":"대표","owner_email":"","area":"전략","project":"ARION Team OS","task":"회원가입/개인업무 버전 테스트","goal":"팀원별 화면 작동 확인","revenue_link":"전체 운영 효율","priority":"high","status":"todo","estimated_minutes":30,"actual_result":"","blocker":"","help_request":"","next_action":"팀원 초대","founder_review":"yes","ai_feedback":"","memo":""},
            {"date":today,"owner":"콘텐츠담당","owner_email":"","area":"SNS","project":"AETHER/VEIL","task":"오늘 업로드할 숏폼 주제 1개 선정","goal":"SNS 유입 시작","revenue_link":"상품 분석 리포트 홍보","priority":"medium","status":"todo","estimated_minutes":20,"actual_result":"","blocker":"","help_request":"","next_action":"후킹 문구 작성","founder_review":"no","ai_feedback":"","memo":""},
        ]),
        "app_portfolio": pd.DataFrame([
            {"project_name":"ARION 본체","type":"AI Brand / Core","status":"LIVE","core_role":"전체 브랜드와 프로젝트 지휘소","revenue_model":"SaaS/컨설팅/자동화","connected_sns":"YouTube, Blog, Instagram","current_metric":"브랜드 중심축","next_action":"Growth OS와 Seller OS 연결 구조 정리","priority":"high","memo":"도구가 아니라 본체"},
            {"project_name":"런닝스타","type":"Reward App","status":"진행중","core_role":"만보기 리워드 앱","revenue_model":"광고/제휴/리워드 커머스","connected_sns":"Reels, Shorts, TikTok","current_metric":"Android 라이브 / iOS 심사중","next_action":"AdMob 승인 문의 및 앱 소개 숏폼 제작","priority":"high","memo":""},
            {"project_name":"AURA","type":"Fortune App","status":"진행중","core_role":"만세력 사주 앱","revenue_model":"유료 리포트/상담/콘텐츠","connected_sns":"Shorts, TikTok, Instagram","current_metric":"iOS TestFlight 업로드 완료","next_action":"운세 숏폼 5개 기획","priority":"high","memo":""},
            {"project_name":"AETHER","type":"AI Content Studio","status":"LIVE","core_role":"AI 이미지/영상/캐릭터 제작 엔진","revenue_model":"제작대행/템플릿/콘텐츠 자동화","connected_sns":"All channels","current_metric":"콘텐츠 제작 엔진","next_action":"햄롤/상품 홍보 이미지 템플릿 제작","priority":"high","memo":""},
            {"project_name":"VEIL","type":"Virtual Influencer","status":"테스트","core_role":"가상 인플루언서 SNS 자동운영","revenue_model":"광고/제휴/상품 홍보","connected_sns":"Instagram, TikTok, Xiaohongshu","current_metric":"테스트 단계","next_action":"가상 인플루언서 콘텐츠 7개 테스트","priority":"medium","memo":""},
        ]),
        "revenue_streams": pd.DataFrame([
            {"revenue_source":"AI 상품 분석 리포트","linked_project":"ARION Seller OS","revenue_type":"service","status":"preparing","expected_revenue":99000,"actual_revenue":0,"cost":0,"net_profit":0,"required_preparation":"샘플 리포트 3개, 신청 문구, 고지문","risk":"성과보장 오해 방지 필요","next_action":"샘플 리포트 1개 완성","priority":"high","memo":"계좌 안정 전에는 결제 기능 개발 금지"},
            {"revenue_source":"구매대행/위탁판매","linked_project":"ARION Seller OS","revenue_type":"commerce","status":"preparing","expected_revenue":150000,"actual_revenue":0,"cost":0,"net_profit":0,"required_preparation":"상품 후보 10개, 테스트 콘텐츠, 판매채널","risk":"CS/반품/인증 리스크","next_action":"저위험 상품 3개 테스트","priority":"high","memo":"재고 선구매 금지"},
        ]),
        "social_marketing": pd.DataFrame([
            {"campaign_name":"이 상품 팔아도 될까","source_content":"창틀 청소 브러쉬 분석","linked_project":"ARION Seller OS","linked_offer":"AI 상품 분석 리포트","channel":"Instagram Reels","format":"Reels","hook":"마진 좋아 보이는데 실제로는 손해일 수 있습니다","status":"planned","upload_date":"","views":0,"saves":0,"comments":0,"clicks":0,"inquiries":0,"sales":0,"next_action":"Canva 템플릿 제작","memo":""},
        ]),
        "commerce_tests": pd.DataFrame([
            {"product_name":"창문·문틀 틈새 청소 브러쉬","sales_method":"위탁판매","category":"청소/생활용품","source":"도매/오픈마켓 후보","cost_price":1200,"expected_price":7900,"shipping_fee":3000,"expected_margin":3700,"certification_risk":"low","cs_risk":"low","return_risk":"low","content_potential":"high","test_status":"후보","linked_content":"이 상품 팔아도 될까 1편","result":"","next_action":"경쟁상품 3개 확인","memo":"전후 비교 콘텐츠 적합"},
        ]),
        "blockers": pd.DataFrame([
            {"date":today,"owner":"대표","owner_email":"","project":"사업운영","blocker":"사업용 계좌/카드 안정화 전 결제 기능 보류","needed_help":"결제/정산 기능 제외 유지","urgency":"high","status":"open","founder_decision_required":"yes","ai_feedback":"","resolution_memo":"내부 운영 MVP만 개발"},
        ]),
        "completion_reports": pd.DataFrame([
            {"date":today,"owner":"대표","owner_email":"","project":"ARION Team OS","completed_task":"회원가입/개인업무 버전 제작","result":"초대코드 기반 회원가입 구조로 전환","proof_link":"","next_task":"팀원 초대","ai_feedback":"","memo":""},
        ]),
        "weekly_team_goals": pd.DataFrame([
            {"week":week,"team_goal":"ARION Team OS 회원가입 버전 배포 및 팀원 온보딩","focus_project":"Growth OS / Seller OS","focus_revenue_stream":"AI 상품 분석 리포트, 위탁판매","content_target":5,"product_target":10,"revenue_target":99000,"status":"active","memo":"이번 주는 공용 운영 구조 구축 우선"},
        ]),
    }
    for key, df in samples.items():
        current = load_table(key)
        if current.empty:
            save_table(key, df, show_success=False)

# -----------------------------
# Login / Signup
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    header("👥 ARION Team OS", "회원가입 후 각자 자신의 오늘 할 일, 마인드셋, 완료 보고, 막힌 일을 관리하는 팀 운영 OS")

    col_a, col_b = st.columns([1,1])

    with col_a:
        card(
            "로그인",
            "이미 가입한 팀원은 이메일과 비밀번호로 로그인하세요. 로그인하면 본인 업무 화면이 자동으로 열립니다."
        )
        with st.form("login_form"):
            login_email = st.text_input("이메일", key="login_email")
            login_pw = st.text_input("비밀번호", type="password", key="login_pw")
            login_submit = st.form_submit_button("로그인")
        if login_submit:
            users = get_users()
            email = clean_email(login_email)
            matched = users[users["email"].astype(str).str.lower() == email] if not users.empty else pd.DataFrame()
            if matched.empty:
                st.error("가입된 이메일이 없습니다.")
            else:
                user = matched.iloc[0].to_dict()
                if verify_password(login_pw, user.get("password_hash","")):
                    user["last_login"] = datetime.now().isoformat(timespec="seconds")
                    users.loc[users["email"].astype(str).str.lower() == email, "last_login"] = user["last_login"]
                    save_users(users)
                    st.session_state.user = user
                    st.success("로그인 성공")
                    st.rerun()
                else:
                    st.error("비밀번호가 맞지 않습니다.")

    with col_b:
        card(
            "팀원 회원가입",
            "초대코드를 받은 팀원만 가입할 수 있습니다. 가입 후 역할에 따라 개인 업무 화면이 만들어집니다."
        )
        with st.form("signup_form"):
            invite = st.text_input("초대코드", type="password")
            name = st.text_input("이름")
            email = st.text_input("이메일")
            role = st.selectbox("역할", ["대표","개발담당","콘텐츠담당","상품담당","운영담당","마케팅담당","기타"])
            area = st.text_input("담당 영역", placeholder="예: SNS 숏폼, 상품 조사, 앱 개발")
            projects = st.text_input("관심/담당 프로젝트", placeholder="예: AETHER, VEIL, Seller OS")
            mindset_goal = st.text_area("내가 ARION에서 이루고 싶은 목표", placeholder="예: 매일 콘텐츠 1개 업로드 습관 만들기")
            pw1 = st.text_input("비밀번호", type="password")
            pw2 = st.text_input("비밀번호 확인", type="password")
            signup_submit = st.form_submit_button("회원가입")
        if signup_submit:
            if invite != INVITE_CODE:
                st.error("초대코드가 맞지 않습니다.")
            elif not name or not email or not pw1:
                st.error("이름, 이메일, 비밀번호는 필수입니다.")
            elif pw1 != pw2:
                st.error("비밀번호 확인이 맞지 않습니다.")
            elif len(pw1) < 4:
                st.error("비밀번호는 최소 4자 이상으로 입력하세요.")
            else:
                users = get_users()
                cleaned = clean_email(email)
                if not users.empty and cleaned in users["email"].astype(str).str.lower().tolist():
                    st.error("이미 가입된 이메일입니다.")
                else:
                    is_first_user = users.empty
                    new_user = pd.DataFrame([{
                        "user_id": uuid.uuid4().hex,
                        "email": cleaned,
                        "name": name.strip(),
                        "role": role,
                        "area": area,
                        "projects": projects,
                        "password_hash": make_password_record(pw1),
                        "status": "active",
                        "is_admin": "yes" if role == "대표" or is_first_user else "no",
                        "created_at": datetime.now().isoformat(timespec="seconds"),
                        "last_login": "",
                        "mindset_goal": mindset_goal,
                        "strength": "",
                        "weakness": "",
                        "memo": "",
                    }])
                    save_users(pd.concat([users.drop(columns=["_record_id"], errors="ignore"), new_user], ignore_index=True))
                    st.success("회원가입 완료. 이제 로그인하세요.")

    st.info("대표도 먼저 회원가입하세요. 첫 가입자 또는 역할이 대표인 사용자는 관리자 화면을 볼 수 있습니다.")
    st.stop()

user = st.session_state.user
header("👥 ARION Team OS", f"{user.get('name','팀원')}님의 개인 업무 화면입니다. 오늘 할 일, 마인드셋, 완료 보고, AI 피드백을 한 곳에서 관리합니다.")

with st.sidebar:
    st.markdown("### ARION Team OS")
    st.write(f"**이름:** {user.get('name','')}")
    st.write(f"**역할:** {user.get('role','')}")
    st.write(f"**담당:** {user.get('area','')}")
    st.caption("팀 공용 운영 화면")
    if ai_available():
        st.success("NVIDIA AI 연결됨")
    else:
        st.warning("NVIDIA AI 미연결")
    if st.button("로그아웃"):
        st.session_state.user = None
        st.rerun()

# Load data
team = load_table("team_members")
actions = load_table("team_daily_actions")
apps = load_table("app_portfolio")
revenue = load_table("revenue_streams")
social = load_table("social_marketing")
commerce = load_table("commerce_tests")
blockers = load_table("blockers")
reports = load_table("completion_reports")
weekly = load_table("weekly_team_goals")
mindsets = load_table("mindset_checkins")
users = load_table("team_users")

tabs = st.tabs([
    "내 홈",
    "오늘 마인드셋",
    "내 오늘 할 일",
    "완료 보고",
    "막힌 일",
    "ARION 전체 지도",
    "수익흐름",
    "SNS 마케팅",
    "구매대행/위탁판매",
    "대표 대시보드",
    "설정",
])

with tabs[0]:
    today = str(date.today())
    my_name = user.get("name","")
    my_email = user.get("email","")
    my_actions = actions[
        (actions["owner"].astype(str) == my_name) |
        (actions["owner_email"].astype(str).str.lower() == my_email)
    ] if not actions.empty else pd.DataFrame()
    my_today = my_actions[my_actions["date"].astype(str) == today] if not my_actions.empty else pd.DataFrame()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("내 오늘 할 일", len(my_today))
    c2.metric("완료", my_today["status"].astype(str).eq("done").sum() if not my_today.empty else 0)
    c3.metric("진행중", my_today["status"].astype(str).eq("doing").sum() if not my_today.empty else 0)
    c4.metric("막힘", my_today["status"].astype(str).eq("blocked").sum() if not my_today.empty else 0)

    card(
        "오늘의 기준",
        f"""
        <p><b>{user.get('name')}</b>님의 역할은 <b>{user.get('role')}</b>입니다.</p>
        <p>오늘은 수익과 연결되는 작은 결과 1개를 만드는 것이 목표입니다.</p>
        <p>완벽하게 끝내는 것보다, 막힌 일을 기록하고 다음 행동을 남기는 것이 중요합니다.</p>
        """
    )

    if not my_today.empty:
        st.subheader("내 오늘 할 일")
        st.dataframe(my_today[["project","task","goal","priority","status","next_action"]], use_container_width=True)
    else:
        st.info("아직 오늘 배정된 할 일이 없습니다. '내 오늘 할 일' 탭에서 직접 추가하거나 대표에게 요청하세요.")

with tabs[1]:
    st.subheader("오늘 마인드셋 체크인")
    st.caption("팀원이 일을 시작하기 전에 목표와 상태를 정리하도록 유도하는 화면입니다.")

    with st.form("mindset_form"):
        energy = st.slider("오늘 에너지", 1, 10, 5)
        focus = st.slider("오늘 집중도", 1, 10, 5)
        today_commitment = st.text_area("오늘 반드시 만들 결과 1개", placeholder="예: 숏폼 대본 1개 완성, 상품 후보 3개 조사")
        worry = st.text_area("오늘 걱정되는 점", placeholder="예: 시간이 부족함, 방향이 애매함")
        support_needed = st.text_area("도움이 필요한 부분", placeholder="예: 대표 결정 필요, 자료 필요")
        use_ai = st.checkbox("NVIDIA AI 피드백 받기", value=ai_available())
        submitted = st.form_submit_button("마인드셋 저장")
    if submitted:
        feedback = ""
        if use_ai:
            prompt = f"""
팀원 이름: {user.get('name')}
역할: {user.get('role')}
담당 영역: {user.get('area')}
오늘 에너지: {energy}/10
오늘 집중도: {focus}/10
오늘 반드시 만들 결과: {today_commitment}
걱정되는 점: {worry}
도움 필요한 부분: {support_needed}
이 팀원이 오늘 더 잘 실행하게 만들 짧은 피드백을 줘.
"""
            feedback = call_nvidia_ai(prompt)
            log_ai_feedback(user.get("name",""), user.get("email",""), "mindset", prompt, feedback)
        row = pd.DataFrame([{
            "date": str(date.today()),
            "owner": user.get("name",""),
            "owner_email": user.get("email",""),
            "energy": energy,
            "focus": focus,
            "today_commitment": today_commitment,
            "worry": worry,
            "support_needed": support_needed,
            "ai_feedback": feedback,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }])
        save_table("mindset_checkins", pd.concat([mindsets.drop(columns=["_record_id"], errors="ignore"), row], ignore_index=True))
        if feedback:
            st.markdown("### AI 피드백")
            st.write(feedback)

    st.subheader("내 마인드셋 기록")
    mine = mindsets[mindsets["owner_email"].astype(str).str.lower() == user.get("email","")] if not mindsets.empty else pd.DataFrame()
    st.dataframe(mine, use_container_width=True)

with tabs[2]:
    st.subheader("내 오늘 할 일")
    my_name = user.get("name","")
    my_email = user.get("email","")
    view = actions[
        (actions["owner"].astype(str) == my_name) |
        (actions["owner_email"].astype(str).str.lower() == my_email)
    ] if not actions.empty else pd.DataFrame(columns=SCHEMAS["team_daily_actions"])

    edited = st.data_editor(view, use_container_width=True, num_rows="dynamic")
    if st.button("내 할 일 저장"):
        # replace only my rows
        base = actions[
            ~(
                (actions["owner"].astype(str) == my_name) |
                (actions["owner_email"].astype(str).str.lower() == my_email)
            )
        ] if not actions.empty else pd.DataFrame(columns=SCHEMAS["team_daily_actions"])
        save_table("team_daily_actions", pd.concat([base.drop(columns=["_record_id"], errors="ignore"), edited.drop(columns=["_record_id"], errors="ignore")], ignore_index=True))

    st.markdown("### 내 할 일 추가")
    with st.form("add_my_action"):
        col1, col2 = st.columns(2)
        with col1:
            new_project = st.text_input("프로젝트")
            new_task = st.text_input("할 일")
            new_goal = st.text_input("목표 결과")
        with col2:
            new_revenue = st.text_input("수익 연결")
            new_priority = st.selectbox("우선순위", ["high","medium","low"])
            est = st.number_input("예상 소요시간/분", min_value=5, max_value=480, value=30)
        add_submit = st.form_submit_button("내 할 일 추가")
    if add_submit and new_task:
        new_row = pd.DataFrame([{
            "date": str(date.today()),
            "owner": user.get("name",""),
            "owner_email": user.get("email",""),
            "area": user.get("area",""),
            "project": new_project,
            "task": new_task,
            "goal": new_goal,
            "revenue_link": new_revenue,
            "priority": new_priority,
            "status": "todo",
            "estimated_minutes": est,
            "actual_result": "",
            "blocker": "",
            "help_request": "",
            "next_action": "",
            "founder_review": "no",
            "ai_feedback": "",
            "memo": "",
        }])
        save_table("team_daily_actions", pd.concat([actions.drop(columns=["_record_id"], errors="ignore"), new_row], ignore_index=True))
        st.rerun()

with tabs[3]:
    st.subheader("완료 보고")
    with st.form("completion_form"):
        project = st.text_input("프로젝트")
        completed_task = st.text_input("완료한 일")
        result = st.text_area("결과", placeholder="무엇이 완료되었고, 어떤 결과가 나왔는지 적어주세요.")
        proof_link = st.text_input("증빙 링크/메모")
        next_task = st.text_input("다음 할 일")
        use_ai = st.checkbox("완료 보고에 대한 AI 피드백 받기", value=ai_available())
        submitted = st.form_submit_button("완료 보고 저장")
    if submitted and completed_task:
        feedback = ""
        if use_ai:
            prompt = f"""
팀원: {user.get('name')} / 역할: {user.get('role')}
프로젝트: {project}
완료한 일: {completed_task}
결과: {result}
다음 할 일: {next_task}
이 완료 보고를 보고 칭찬 1개, 개선점 1개, 다음 행동 3개를 제안해줘.
"""
            feedback = call_nvidia_ai(prompt)
            log_ai_feedback(user.get("name",""), user.get("email",""), "completion", prompt, feedback)
        row = pd.DataFrame([{
            "date": str(date.today()),
            "owner": user.get("name",""),
            "owner_email": user.get("email",""),
            "project": project,
            "completed_task": completed_task,
            "result": result,
            "proof_link": proof_link,
            "next_task": next_task,
            "ai_feedback": feedback,
            "memo": "",
        }])
        save_table("completion_reports", pd.concat([reports.drop(columns=["_record_id"], errors="ignore"), row], ignore_index=True))
        if feedback:
            st.markdown("### AI 피드백")
            st.write(feedback)

    mine = reports[reports["owner_email"].astype(str).str.lower() == user.get("email","")] if not reports.empty else pd.DataFrame()
    st.dataframe(mine, use_container_width=True)

with tabs[4]:
    st.subheader("막힌 일 / 도움 요청")
    with st.form("blocker_form"):
        project = st.text_input("막힌 프로젝트")
        blocker = st.text_area("막힌 내용")
        needed_help = st.text_area("필요한 도움")
        urgency = st.selectbox("긴급도", ["high","medium","low"])
        founder_required = st.selectbox("대표 결정 필요", ["yes","no"])
        use_ai = st.checkbox("막힌 일 해결 방향 AI 피드백 받기", value=ai_available())
        submitted = st.form_submit_button("막힌 일 저장")
    if submitted and blocker:
        feedback = ""
        if use_ai:
            prompt = f"""
팀원: {user.get('name')} / 역할: {user.get('role')}
프로젝트: {project}
막힌 내용: {blocker}
필요한 도움: {needed_help}
긴급도: {urgency}
대표 결정 필요: {founder_required}
이 막힌 일을 해결하기 위한 현실적인 다음 행동을 제안해줘.
"""
            feedback = call_nvidia_ai(prompt)
            log_ai_feedback(user.get("name",""), user.get("email",""), "blocker", prompt, feedback)
        row = pd.DataFrame([{
            "date": str(date.today()),
            "owner": user.get("name",""),
            "owner_email": user.get("email",""),
            "project": project,
            "blocker": blocker,
            "needed_help": needed_help,
            "urgency": urgency,
            "status": "open",
            "founder_decision_required": founder_required,
            "ai_feedback": feedback,
            "resolution_memo": "",
        }])
        save_table("blockers", pd.concat([blockers.drop(columns=["_record_id"], errors="ignore"), row], ignore_index=True))
        if feedback:
            st.markdown("### AI 피드백")
            st.write(feedback)

    mine = blockers[blockers["owner_email"].astype(str).str.lower() == user.get("email","")] if not blockers.empty else pd.DataFrame()
    st.dataframe(mine, use_container_width=True)

with tabs[5]:
    st.subheader("ARION 전체 지도")
    if apps.empty:
        st.info("아직 앱 포트폴리오 데이터가 없습니다. 설정 탭에서 초기 샘플 데이터를 넣으세요.")
    else:
        st.dataframe(apps[["project_name","core_role","revenue_model","next_action","priority"]], use_container_width=True)

with tabs[6]:
    st.subheader("수익흐름")
    st.dataframe(revenue, use_container_width=True)

with tabs[7]:
    st.subheader("SNS 마케팅")
    st.dataframe(social, use_container_width=True)

with tabs[8]:
    st.subheader("구매대행/위탁판매")
    st.warning("고위험 상품, 재고 선구매, 무단 크롤링은 피하세요.")
    st.dataframe(commerce, use_container_width=True)

with tabs[9]:
    if not is_admin():
        st.warning("대표/관리자만 볼 수 있는 화면입니다.")
    else:
        st.subheader("대표 대시보드")
        today = str(date.today())
        today_df = actions[actions["date"].astype(str) == today] if not actions.empty else pd.DataFrame()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("가입 팀원", len(users))
        c2.metric("오늘 할 일", len(today_df))
        c3.metric("완료", today_df["status"].astype(str).eq("done").sum() if not today_df.empty else 0)
        c4.metric("막힘", today_df["status"].astype(str).eq("blocked").sum() if not today_df.empty else 0)

        st.subheader("전체 팀원")
        st.dataframe(users.drop(columns=["password_hash"], errors="ignore"), use_container_width=True)

        st.subheader("전체 오늘 할 일")
        edited_actions = st.data_editor(actions, use_container_width=True, num_rows="dynamic")
        if st.button("대표: 전체 할 일 저장"):
            save_table("team_daily_actions", edited_actions)

        st.subheader("전체 막힌 일")
        st.dataframe(blockers, use_container_width=True)

        st.subheader("AI 피드백 로그")
        st.dataframe(load_table("ai_feedback_logs"), use_container_width=True)

with tabs[10]:
    st.subheader("설정")
    st.json({
        "supabase_connected": bool(get_supabase()),
        "storage": "Supabase" if get_supabase() else "Local CSV fallback",
        "auth": "invite-code signup + local password hash",
        "ai": "NVIDIA connected" if ai_available() else "NVIDIA not connected",
        "nvidia_model": NVIDIA_MODEL,
        "do_not_build_yet": ["payment", "banking", "settlement", "unsafe crawling"],
    })

    if st.button("초기 샘플 데이터 넣기"):
        seed_data()
        st.success("초기 샘플 데이터 확인/삽입 완료")
        st.rerun()

    if is_admin():
        st.markdown("### 관리자: 팀원 관리")
        editable_users = users.drop(columns=["password_hash"], errors="ignore")
        st.dataframe(editable_users, use_container_width=True)
