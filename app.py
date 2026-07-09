
from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd
import streamlit as st

try:
    from supabase import create_client
except Exception:
    create_client = None

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
}

.stApp {
  background: var(--bg) !important;
  color: var(--text) !important;
}

.block-container {
  max-width: 1480px !important;
  padding-top: 1.35rem !important;
  padding-bottom: 4rem !important;
}

header[data-testid="stHeader"] {
  background: transparent !important;
}

h1, h2, h3, h4, h5, h6 {
  color: var(--text) !important;
  letter-spacing: -0.03em;
}

p, span, div, label {
  color: var(--text);
}

/* Main header */
.arion-header {
  background: linear-gradient(135deg, #ffffff 0%, #eef2ff 100%);
  border: 1px solid #dbeafe;
  border-radius: 28px;
  padding: 30px 34px;
  margin-bottom: 24px;
  box-shadow: 0 16px 45px rgba(79,70,229,.08);
}

.arion-title {
  font-size: 2.15rem;
  line-height: 1.15;
  font-weight: 950;
  color: #111827;
  letter-spacing: -0.055em;
  margin-bottom: 10px;
}

.arion-subtitle {
  color: #4b5563;
  font-size: 1.02rem;
  line-height: 1.65;
  margin: 0;
}

/* Cards */
.arion-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 22px;
  padding: 22px 24px;
  margin: 14px 0;
  box-shadow: 0 10px 28px rgba(15,23,42,.045);
}

.arion-card h3 {
  margin-top: 0;
  color: #111827 !important;
}

/* Login helper */
.login-guide {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 22px;
  padding: 20px 22px;
  margin: 12px 0 18px 0;
  box-shadow: 0 10px 28px rgba(15,23,42,.045);
}

.login-guide-title {
  font-size: 1.15rem;
  font-weight: 950;
  color: #111827;
  margin-bottom: 6px;
}

.login-guide-desc {
  color: #6b7280;
  line-height: 1.6;
}

/* Inputs */
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

/* Buttons */
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

.stButton > button *,
button[kind="primary"] *,
button[data-testid="baseButton-primary"] * {
  color: #ffffff !important;
}

/* Form submit buttons */
[data-testid="stFormSubmitButton"] button {
  min-height: 42px !important;
  border-radius: 14px !important;
  border: 1px solid var(--primary) !important;
  background: var(--primary) !important;
  color: #ffffff !important;
  font-weight: 900 !important;
}

[data-testid="stFormSubmitButton"] button * {
  color: #ffffff !important;
}

/* Metrics */
[data-testid="stMetric"] {
  background: #ffffff !important;
  border: 1px solid var(--border) !important;
  border-radius: 20px !important;
  padding: 18px !important;
  box-shadow: 0 10px 28px rgba(15,23,42,.045);
}

[data-testid="stMetricLabel"] {
  color: var(--muted) !important;
  font-weight: 800 !important;
}

[data-testid="stMetricValue"] {
  color: #111827 !important;
  font-size: 1.65rem !important;
  font-weight: 950 !important;
}

/* Tabs */
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

.stTabs [aria-selected="true"] {
  background: var(--primary-soft) !important;
  color: var(--primary) !important;
}

/* Tables */
[data-testid="stDataFrame"], [data-testid="stDataEditor"] {
  border-radius: 20px !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
  background: #ffffff !important;
  box-shadow: 0 10px 28px rgba(15,23,42,.04);
}

/* Alerts */
div[data-testid="stAlert"] {
  border-radius: 18px !important;
  border: 1px solid var(--border) !important;
}

/* Status badges */
.badge { display:inline-block; border-radius:999px; padding:4px 10px; font-weight:900; font-size:.78rem; }
.high { background:#fef2f2; color:#b91c1c; border:1px solid #fecaca; }
.medium { background:#fffbeb; color:#92400e; border:1px solid #fde68a; }
.low { background:#ecfdf5; color:#047857; border:1px solid #a7f3d0; }

/* Make dark theme leftovers readable */
section[data-testid="stSidebar"] {
  background: #ffffff !important;
}
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

# -----------------------------
# Config / Secrets
# -----------------------------
def get_secret(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, os.environ.get(name, default))
    except Exception:
        return os.environ.get(name, default)

TEAM_PASSWORD = get_secret("TEAM_PASSWORD", "change-me")
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_SERVICE_KEY = get_secret("SUPABASE_SERVICE_KEY")

# -----------------------------
# Schemas
# -----------------------------
SCHEMAS: Dict[str, List[str]] = {
    "team_members": ["name","role","area","projects","contact","status","today_priority","memo"],
    "team_daily_actions": ["date","owner","area","project","task","goal","revenue_link","priority","status","estimated_minutes","actual_result","blocker","help_request","next_action","founder_review","memo"],
    "app_portfolio": ["project_name","type","status","core_role","revenue_model","connected_sns","current_metric","next_action","priority","memo"],
    "revenue_streams": ["revenue_source","linked_project","revenue_type","status","expected_revenue","actual_revenue","cost","net_profit","required_preparation","risk","next_action","priority","memo"],
    "social_marketing": ["campaign_name","source_content","linked_project","linked_offer","channel","format","hook","status","upload_date","views","saves","comments","clicks","inquiries","sales","next_action","memo"],
    "commerce_tests": ["product_name","sales_method","category","source","cost_price","expected_price","shipping_fee","expected_margin","certification_risk","cs_risk","return_risk","content_potential","test_status","linked_content","result","next_action","memo"],
    "blockers": ["date","owner","project","blocker","needed_help","urgency","status","founder_decision_required","resolution_memo"],
    "completion_reports": ["date","owner","project","completed_task","result","proof_link","next_task","memo"],
    "weekly_team_goals": ["week","team_goal","focus_project","focus_revenue_stream","content_target","product_target","revenue_target","status","memo"],
}

def empty_df(key: str) -> pd.DataFrame:
    return pd.DataFrame(columns=SCHEMAS[key])

# -----------------------------
# Supabase + local fallback storage
# -----------------------------
@st.cache_resource
def get_supabase():
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY or create_client is None:
        return None
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

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

def load_table(key: str) -> pd.DataFrame:
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
            st.error(f"Supabase에서 {key} 불러오기 실패: {e}")

    p = local_path(key)
    if p.exists():
        try:
            return normalize_df(key, pd.read_csv(p, encoding="utf-8-sig"))
        except Exception:
            return empty_df(key)
    return empty_df(key)

def save_table(key: str, df: pd.DataFrame):
    df = normalize_df(key, df.copy())
    client = get_supabase()
    data_records = []
    for _, row in df.iterrows():
        clean = {col: ("" if pd.isna(row.get(col)) else row.get(col)) for col in SCHEMAS[key]}
        data_records.append({"table_key": key, "data": clean})

    if client:
        try:
            # MVP: overwrite table_key. Simple and predictable for small internal teams.
            client.table("arion_records").delete().eq("table_key", key).execute()
            if data_records:
                client.table("arion_records").insert(data_records).execute()
            st.success("공용 DB에 저장했습니다.")
            return
        except Exception as e:
            st.error(f"Supabase 저장 실패: {e}")

    df.to_csv(local_path(key), index=False, encoding="utf-8-sig")
    st.success("로컬 CSV에 저장했습니다. Supabase 설정 전에는 팀원들과 자동 공유되지 않습니다.")

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
            {"date":today,"owner":"대표","area":"전략","project":"ARION Team OS","task":"팀 공용 링크 버전 배포 확인","goal":"팀원 접속 가능","revenue_link":"전체 운영 효율","priority":"high","status":"todo","estimated_minutes":30,"actual_result":"","blocker":"","help_request":"","next_action":"Streamlit 링크 공유","founder_review":"yes","memo":""},
            {"date":today,"owner":"콘텐츠담당","area":"SNS","project":"AETHER/VEIL","task":"오늘 업로드할 숏폼 주제 1개 선정","goal":"SNS 유입 시작","revenue_link":"상품 분석 리포트 홍보","priority":"medium","status":"todo","estimated_minutes":20,"actual_result":"","blocker":"","help_request":"","next_action":"후킹 문구 작성","founder_review":"no","memo":""},
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
            {"date":today,"owner":"대표","project":"사업운영","blocker":"사업용 계좌/카드 안정화 전 결제 기능 보류","needed_help":"결제/정산 기능 제외 유지","urgency":"high","status":"open","founder_decision_required":"yes","resolution_memo":"내부 운영 MVP만 개발"},
        ]),
        "completion_reports": pd.DataFrame([
            {"date":today,"owner":"대표","project":"ARION Team OS","completed_task":"팀 공용 링크 버전 제작 결정","result":"Supabase/Streamlit 구조로 전환","proof_link":"","next_task":"배포","memo":""},
        ]),
        "weekly_team_goals": pd.DataFrame([
            {"week":week,"team_goal":"ARION Team OS 공용 링크 배포 및 팀원 온보딩","focus_project":"Growth OS / Seller OS","focus_revenue_stream":"AI 상품 분석 리포트, 위탁판매","content_target":5,"product_target":10,"revenue_target":99000,"status":"active","memo":"이번 주는 공용 운영 구조 구축 우선"},
        ]),
    }
    for key, df in samples.items():
        current = load_table(key)
        if current.empty:
            save_table(key, df)

# -----------------------------
# Access gate
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    header("👥 ARION Team OS", "팀원이 링크로 접속해서 오늘 할 일, 수익흐름, 앱 포트폴리오, 막힌 일을 함께 확인하는 공용 운영 OS")
    st.markdown(
        """
<div class="login-guide">
  <div class="login-guide-title">팀 공용 비밀번호로 입장</div>
  <div class="login-guide-desc">
    팀원에게 공유한 비밀번호를 입력하세요. 비밀번호는 Streamlit Cloud의 Secrets에서 <b>TEAM_PASSWORD</b> 값을 바꾸면 언제든 변경할 수 있습니다.
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    if TEAM_PASSWORD == "change-me":
        st.warning("현재 기본 비밀번호 `change-me` 상태입니다. 배포 전 Streamlit Secrets에서 TEAM_PASSWORD를 반드시 바꾸세요.")
    password = st.text_input("팀 공용 비밀번호", type="password", placeholder="비밀번호 입력")
    col_login, col_help = st.columns([1, 5])
    with col_login:
        login_clicked = st.button("입장하기", type="primary")
    with col_help:
        st.caption("비밀번호를 바꾼 뒤에는 앱을 새로고침하면 새 비밀번호가 적용됩니다.")
    if login_clicked:
        if password == TEAM_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 맞지 않습니다.")
    st.stop()

header("👥 ARION Team OS", "팀 공용 링크 버전: 오늘 할 일, 담당자, 수익흐름, 앱 포트폴리오, SNS 실행을 한 곳에서 공유합니다.")

with st.sidebar:
    st.markdown("### ARION Team OS")
    st.caption("팀 공용 운영 화면")
    if st.button("로그아웃"):
        st.session_state.authenticated = False
        st.rerun()

if not get_supabase():
    st.warning("Supabase가 연결되지 않았습니다. 지금은 로컬 CSV로 작동합니다. 팀 공용 링크로 쓰려면 Streamlit Secrets에 SUPABASE_URL / SUPABASE_SERVICE_KEY를 넣어야 합니다.")

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

tabs = st.tabs([
    "처음 보는 사람용 안내",
    "대표 대시보드",
    "팀원 오늘 할 일",
    "앱 포트폴리오",
    "수익흐름",
    "SNS 마케팅",
    "구매대행/위탁판매",
    "막힌 일",
    "완료 보고",
    "주간 목표",
    "설정",
])

with tabs[0]:
    st.markdown(
        """
<div class="arion-card">
<h3>ARION은 무엇인가?</h3>
<p>ARION은 여러 앱과 AI 시스템을 운영하면서 SNS 마케팅, 상품 분석 리포트, 위탁판매/구매대행, 향후 SaaS로 현금흐름을 만드는 프로젝트입니다.</p>
</div>
<div class="arion-card">
<h3>팀원이 해야 할 것</h3>
<ol>
<li>본인 이름으로 오늘 할 일을 확인합니다.</li>
<li>진행 상태를 todo → doing → done 또는 blocked로 바꿉니다.</li>
<li>막힌 일이 있으면 “막힌 일” 탭에 적습니다.</li>
<li>완료한 일은 “완료 보고” 탭에 남깁니다.</li>
<li>수익과 연결되는 업무를 우선 처리합니다.</li>
</ol>
</div>
""",
        unsafe_allow_html=True,
    )

    st.subheader("ARION 전체 지도")
    map_df = apps[["project_name","core_role","revenue_model","next_action","priority"]] if not apps.empty else pd.DataFrame()
    st.dataframe(map_df, use_container_width=True)

with tabs[1]:
    today = str(date.today())
    today_df = actions[actions["date"].astype(str) == today] if not actions.empty else pd.DataFrame()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("팀원 수", len(team))
    c2.metric("오늘 할 일", len(today_df))
    c3.metric("완료", today_df["status"].astype(str).eq("done").sum() if not today_df.empty else 0)
    c4.metric("막힌 일", today_df["status"].astype(str).eq("blocked").sum() if not today_df.empty else 0)

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("앱/프로젝트", len(apps))
    c6.metric("수익원", len(revenue))
    c7.metric("SNS 캠페인", len(social))
    c8.metric("대표 확인 필요", today_df["founder_review"].astype(str).eq("yes").sum() if not today_df.empty else 0)

    st.subheader("팀원별 오늘 상태")
    if not today_df.empty:
        st.dataframe(today_df.groupby(["owner","status"]).size().reset_index(name="count"), use_container_width=True)

    st.subheader("대표가 봐야 할 일")
    if not today_df.empty and "founder_review" in today_df:
        st.dataframe(today_df[today_df["founder_review"].astype(str).eq("yes")], use_container_width=True)

with tabs[2]:
    st.subheader("팀원 오늘 할 일")
    owners = ["전체"] + sorted(actions["owner"].dropna().astype(str).unique().tolist()) if not actions.empty and "owner" in actions else ["전체"]
    owner = st.selectbox("담당자 필터", owners)
    status = st.selectbox("상태 필터", ["전체","todo","doing","done","blocked","moved"])
    view = actions.copy()
    if owner != "전체":
        view = view[view["owner"].astype(str) == owner]
    if status != "전체":
        view = view[view["status"].astype(str) == status]
    edited = st.data_editor(view, use_container_width=True, num_rows="dynamic")
    if st.button("팀원 할 일 저장"):
        if owner == "전체" and status == "전체":
            save_table("team_daily_actions", edited)
        else:
            st.warning("필터가 걸린 상태에서는 전체 데이터 손실을 막기 위해 저장하지 않았습니다. 담당자/상태를 전체로 바꾸고 저장하세요.")

    st.markdown("### 새 할 일 추가")
    with st.form("add_action"):
        new_owner = st.selectbox("담당자", sorted(team["name"].dropna().astype(str).unique().tolist()) if not team.empty else ["대표"])
        col1, col2 = st.columns(2)
        with col1:
            new_project = st.text_input("프로젝트")
            new_task = st.text_input("할 일")
            new_goal = st.text_input("목표 결과")
        with col2:
            new_revenue = st.text_input("수익 연결")
            new_priority = st.selectbox("우선순위", ["high","medium","low"])
            new_review = st.selectbox("대표 확인 필요", ["yes","no"])
        submitted = st.form_submit_button("할 일 추가")
    if submitted and new_task:
        new_row = pd.DataFrame([{
            "date": str(date.today()),
            "owner": new_owner,
            "area": "",
            "project": new_project,
            "task": new_task,
            "goal": new_goal,
            "revenue_link": new_revenue,
            "priority": new_priority,
            "status": "todo",
            "estimated_minutes": 30,
            "actual_result": "",
            "blocker": "",
            "help_request": "",
            "next_action": "",
            "founder_review": new_review,
            "memo": "",
        }])
        save_table("team_daily_actions", pd.concat([actions.drop(columns=["_record_id"], errors="ignore"), new_row], ignore_index=True))
        st.rerun()

with tabs[3]:
    st.subheader("앱 포트폴리오")
    edited = st.data_editor(apps, use_container_width=True, num_rows="dynamic")
    if st.button("앱 포트폴리오 저장"):
        save_table("app_portfolio", edited)

with tabs[4]:
    st.subheader("수익흐름")
    rev = revenue.copy()
    if not rev.empty:
        rev["actual_revenue"] = pd.to_numeric(rev["actual_revenue"], errors="coerce").fillna(0)
        rev["cost"] = pd.to_numeric(rev["cost"], errors="coerce").fillna(0)
        rev["net_profit"] = rev["actual_revenue"] - rev["cost"]
    edited = st.data_editor(rev, use_container_width=True, num_rows="dynamic")
    if st.button("수익흐름 저장"):
        save_table("revenue_streams", edited)

with tabs[5]:
    st.subheader("SNS 마케팅")
    edited = st.data_editor(social, use_container_width=True, num_rows="dynamic")
    if st.button("SNS 저장"):
        save_table("social_marketing", edited)

with tabs[6]:
    st.subheader("구매대행/위탁판매")
    st.warning("고위험 상품, 재고 선구매, 무단 크롤링은 피하세요.")
    edited = st.data_editor(commerce, use_container_width=True, num_rows="dynamic")
    if st.button("커머스 테스트 저장"):
        save_table("commerce_tests", edited)

with tabs[7]:
    st.subheader("막힌 일 / 도움 요청")
    edited = st.data_editor(blockers, use_container_width=True, num_rows="dynamic")
    if st.button("막힌 일 저장"):
        save_table("blockers", edited)

with tabs[8]:
    st.subheader("완료 보고")
    edited = st.data_editor(reports, use_container_width=True, num_rows="dynamic")
    if st.button("완료 보고 저장"):
        save_table("completion_reports", edited)

with tabs[9]:
    st.subheader("주간 팀 목표")
    edited = st.data_editor(weekly, use_container_width=True, num_rows="dynamic")
    if st.button("주간 목표 저장"):
        save_table("weekly_team_goals", edited)

with tabs[10]:
    st.subheader("설정")
    st.write("공용 링크 버전 상태")
    st.json({
        "supabase_connected": bool(get_supabase()),
        "storage": "Supabase" if get_supabase() else "Local CSV fallback",
        "auth": "shared password only",
        "do_not_build_yet": ["payment", "banking", "settlement", "customer login", "unsafe crawling"],
    })
    if st.button("초기 샘플 데이터 넣기"):
        seed_data()
        st.success("초기 샘플 데이터 확인/삽입 완료")
        st.rerun()
