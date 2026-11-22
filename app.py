import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import load_transactions
from ai_engine import (
    forecast_cashflow,
    detect_anomalies,
    calculate_business_health,
    smart_purchase_planner,
)
from local_copilot import local_finance_copilot

# ============================================================
# FINSIGHTAI — PREMIUM FINTECH WORKSPACE
# Backend functions and transaction schema are preserved.
# ============================================================
st.set_page_config(
    page_title="FinSightAI | Financial Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------- DESIGN SYSTEM ----------------------------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {
  --bg:#080d17; --panel:#101a29; --panel2:#142235; --line:rgba(160,180,205,.13);
  --text:#f3f7fc; --muted:#91a2b8; --green:#45dfad; --red:#ff7185;
  --blue:#82aaff; --gold:#f3c875;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 50% -20%,rgba(37,112,105,.20),transparent 48%),var(--bg);color:var(--text)}
[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
}
[data-testid="stToolbar"],#MainMenu,footer{visibility:hidden}
.block-container{max-width:1540px;padding:0.5rem 3.1rem 3rem}
h1,h2,h3{font-family:'Manrope',sans-serif!important;color:var(--text)!important;letter-spacing:-.04em}
p,label{color:var(--muted)}
hr{border-color:var(--line)}
/* top brand/navigation */
.topline{display:flex;align-items:center;justify-content:space-between;padding:3px 0 17px;border-bottom:1px solid var(--line);margin-bottom:18px}
.brand{display:flex;align-items:center;gap:11px}
.brand-icon{height:38px;width:38px;border-radius:12px;background:linear-gradient(145deg,#78f0c9,#1bb889);display:flex;align-items:center;justify-content:center;color:#062116;font-size:19px;font-weight:900;box-shadow:0 8px 25px #26c99530}
.brand-name{font-family:Manrope,sans-serif;font-size:19px;font-weight:800;color:#f5f8fc;letter-spacing:-.7px}
.brand-sub{font-size:8px;letter-spacing:2px;color:#8192a9;font-weight:800;margin-top:1px}
.live{font-size:10px;color:#7ce9c3;border:1px solid #45dfad35;background:#45dfad0c;border-radius:30px;padding:7px 11px;letter-spacing:1px;font-weight:800}
div[data-testid="stRadio"]>label{display:none}
div[data-testid="stRadio"] div[role="radiogroup"]{display:flex;gap:7px;flex-wrap:wrap}
div[data-testid="stRadio"] div[role="radiogroup"] label{border:1px solid transparent;border-radius:10px;padding:9px 13px;background:transparent;transition:.18s}
div[data-testid="stRadio"] div[role="radiogroup"] label:hover{background:#ffffff0a;border-color:var(--line)}
div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"]{background:linear-gradient(120deg,#1b493f,#172d39);border:1px solid #45dfad45}
div[data-testid="stRadio"] div[role="radiogroup"] label p{font-size:11px;font-weight:700;color:#b9c6d6}
div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] p{color:#7df0c7}
/* page headings and cards */
.eyebrow{font-size:9px;letter-spacing:2px;font-weight:800;color:var(--green);text-transform:uppercase;margin-bottom:7px}
.page-title{font-family:Manrope,sans-serif;font-size:31px;font-weight:800;letter-spacing:-1.3px;color:#f4f7fc;line-height:1.15}
.page-sub{font-size:12px;color:#91a2b8;margin-top:7px}
.hero{position:relative;overflow:hidden;border:1px solid #4c9e9140;border-radius:22px;padding:26px 29px;margin:17px 0 23px;background:radial-gradient(circle at 88% 20%,#45dfad24,transparent 24%),linear-gradient(112deg,#142d37,#14243a 58%,#17253a);box-shadow:0 18px 50px #0004}
.hero:after{content:"";position:absolute;width:210px;height:210px;border:1px solid #7debc31c;border-radius:50%;right:6%;top:-120px;box-shadow:0 0 0 24px #7debc308,0 0 0 48px #7debc305}
.hero-kicker{font-size:9px;letter-spacing:2px;color:#7ce9c3;font-weight:800;margin-bottom:10px}
.hero-title{font-family:Manrope,sans-serif;font-size:30px;font-weight:800;letter-spacing:-1.2px;color:#f5f8fc}
.hero-copy{font-size:12px;color:#b0c2d1;margin-top:9px;max-width:690px}
.section{display:flex;align-items:end;justify-content:space-between;margin:25px 0 12px}
.section-kicker{font-size:9px;color:var(--green);font-weight:800;letter-spacing:1.8px}
.section-title{font-family:Manrope,sans-serif;font-size:19px;font-weight:800;color:#f1f5fa;letter-spacing:-.6px;margin-top:3px}
.section-desc{font-size:11px;color:#8496ad;margin-top:3px}
.kpi{background:linear-gradient(145deg,#152338,#101a29);border:1px solid var(--line);border-radius:16px;padding:17px 18px;min-height:112px;box-shadow:0 12px 32px #0002}
.kpi-label{font-size:9px;color:#91a5bd;letter-spacing:1.35px;font-weight:800;text-transform:uppercase}
.kpi-value{font-family:Manrope,sans-serif;color:#f6f8fc;font-size:25px;font-weight:800;letter-spacing:-1px;margin-top:9px;white-space:nowrap}
.kpi-note{font-size:10px;color:#8194ac;margin-top:4px}
.panel{background:linear-gradient(145deg,rgba(20,34,52,.96),rgba(13,23,37,.96));border:1px solid var(--line);border-radius:17px;padding:17px 19px;margin-bottom:12px}
.panel-title{font-family:Manrope,sans-serif;font-size:14px;font-weight:800;color:#eef4fa}
.panel-sub{font-size:10px;color:#8193aa;margin-top:4px}
.pill{display:inline-block;border-radius:30px;padding:5px 9px;font-size:9px;font-weight:800;letter-spacing:.6px;color:#70e9bf;background:#45dfad12;border:1px solid #45dfad30}
.stButton>button,.stDownloadButton>button{border:1px solid #45dfad55;border-radius:10px;color:#062116;background:linear-gradient(135deg,#68ebbd,#27bd8e);font-weight:800;min-height:2.55rem;transition:.18s}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:#8af5d2;background:linear-gradient(135deg,#8af5d2,#3bd3a2);color:#04170f;transform:translateY(-1px);box-shadow:0 8px 22px #27bd8e25}
.stTextInput input,.stNumberInput input,.stTextArea textarea,[data-baseweb="select"]>div{background:#111e2e!important;color:#f2f6fb!important;border:1px solid #2a3b51!important;border-radius:10px!important}
[data-baseweb="popover"],[data-baseweb="menu"]{background:#142235!important}
[data-baseweb="menu"] *{color:#eaf0f8!important}
[data-testid="stDataFrame"],[data-testid="stTable"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
[data-testid="stMetric"]{background:#142236;border:1px solid var(--line);border-radius:13px;padding:13px 15px}
[data-testid="stMetricLabel"]{color:#91a4bb!important;font-size:10px!important}
[data-testid="stMetricValue"]{color:#f5f8fc!important;font-family:Manrope,sans-serif!important}
[data-testid="stChatMessage"]{background:#142236;border:1px solid var(--line);border-radius:14px}
[data-testid="stAlert"]{border-radius:12px}
[data-testid="stTabs"] button{color:#aebed0;font-weight:700}
[data-testid="stTabs"] button[aria-selected="true"]{color:var(--green)!important}
.footer{border-top:1px solid var(--line);text-align:center;padding:18px 0 2px;margin-top:28px;color:#61748d;font-size:9px;letter-spacing:1.5px}
@media(max-width:900px){.block-container{padding:1rem 1rem 2rem}.page-title{font-size:25px}.hero-title{font-size:25px}.kpi-value{font-size:20px}}
</style>
""", unsafe_allow_html=True)

# ---------------------------- HELPERS ----------------------------
def money(value):
    return f"₹{float(value):,.0f}"

def format_dates(series):
    return pd.to_datetime(series, errors="coerce").dt.strftime("%d %b %Y").fillna("")

def header(kicker, title, subtitle=""):
    st.markdown(f'<div class="eyebrow">{kicker}</div><div class="page-title">{title}</div><div class="page-sub">{subtitle}</div>', unsafe_allow_html=True)

def section(kicker, title, desc=""):
    st.markdown(f'<div class="section"><div><div class="section-kicker">{kicker}</div><div class="section-title">{title}</div><div class="section-desc">{desc}</div></div></div>', unsafe_allow_html=True)

def kpi(label, value, note=""):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)

def panel_title(title, subtitle=""):
    st.markdown(f'<div class="panel-title">{title}</div><div class="panel-sub">{subtitle}</div>', unsafe_allow_html=True)

def chart_style(fig, height=350):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans",color="#9aacc1",size=10),
        margin=dict(l=8,r=8,t=38,b=8), height=height,
        legend=dict(orientation="h",y=-.22,bgcolor="rgba(0,0,0,0)",font=dict(size=9)),
        hoverlabel=dict(bgcolor="#17263a",font_color="#f4f7fc"),
    )
    fig.update_xaxes(showgrid=False,zeroline=False,linecolor="rgba(148,163,184,.12)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.09)",zeroline=False)
    return fig

def table(data, height=360):
    st.dataframe(data,use_container_width=True,hide_index=True,height=height)

def error_box(name, exc):
    st.error(f"{name} could not be completed: {exc}")

# ---------------------------- DATA ----------------------------
try:
    df=load_transactions()
    if df is None or df.empty:
        st.error("No transaction data found. Check data/transactions.csv."); st.stop()
    df=df.copy()
    required={"date","type","category","amount"}
    missing=required-set(df.columns)
    if missing:
        st.error(f"Dataset is missing required columns: {', '.join(sorted(missing))}"); st.stop()
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    df["amount"]=pd.to_numeric(df["amount"],errors="coerce")
    df["type"]=df["type"].astype(str).str.strip().str.title()
    df=df.dropna(subset=["date","amount"])
    df=df[df["type"].isin(["Inflow","Outflow"])].copy()
    if df.empty:
        st.error("No valid Inflow/Outflow records were found."); st.stop()
    if "payment_mode" not in df.columns: df["payment_mode"]="Not specified"
    if "description" not in df.columns: df["description"]=""
except Exception as exc:
    st.error(f"Database loading failed: {exc}"); st.stop()

# ---------------------------- GLOBAL NAV ----------------------------
st.markdown("""
<div class="topline">
  <div class="brand"><div class="brand-icon">◆</div><div><div class="brand-name">FinSightAI</div><div class="brand-sub">FINANCIAL INTELLIGENCE PLATFORM</div></div></div>
  <div class="live">● SYSTEM LIVE&nbsp;&nbsp; · &nbsp;&nbsp;ARTHATON 2026</div>
</div>
""",unsafe_allow_html=True)

pages=["Overview","Cash Flow","Anomaly Detection","Business Health","AI Copilot","Purchase Planner","Transactions"]
page=st.radio("Workspace",pages,horizontal=True,label_visibility="collapsed",key="main_navigation")

with st.expander("⚙ Financial assumptions",expanded=False):
    set1,set2=st.columns([1,1])
    with set1:
        opening_balance=st.number_input("Assumed opening balance (₹)",min_value=0,value=50000,step=5000,key="opening_balance")
    with set2:
        forecast_days=st.selectbox("Forecast horizon",[7,30],index=0,key="forecast_horizon")

# ---------------------------- COMMON METRICS ----------------------------
last_30=df[df["date"]>=df["date"].max()-pd.Timedelta(days=29)]
monthly_inflow=last_30.loc[last_30["type"]=="Inflow","amount"].sum()
monthly_outflow=last_30.loc[last_30["type"]=="Outflow","amount"].sum()
total_inflow=df.loc[df["type"]=="Inflow","amount"].sum()
total_outflow=df.loc[df["type"]=="Outflow","amount"].sum()
estimated_balance=opening_balance+total_inflow-total_outflow
net_30=monthly_inflow-monthly_outflow

# ============================================================
# OVERVIEW — EXECUTIVE DASHBOARD
# ============================================================
if page=="Overview":
    st.markdown(f"""
    <div class="hero"><div class="hero-kicker">EXECUTIVE COMMAND CENTRE&nbsp; / &nbsp;{len(df):,} RECORDS CONNECTED</div>
    <div class="hero-title">Clarity for every financial decision.</div>
    <div class="hero-copy">Your business finances, brought together. Monitor liquidity, understand spending patterns and turn transaction history into your next move.</div></div>
    """,unsafe_allow_html=True)
    section("AT A GLANCE","Financial position","A consolidated snapshot of your transaction history.")
    cols=st.columns(4)
    with cols[0]: kpi("Estimated balance",money(estimated_balance),"Assumed opening balance + net history")
    with cols[1]: kpi("30-day inflow",money(monthly_inflow),"Money received")
    with cols[2]: kpi("30-day outflow",money(monthly_outflow),"Money spent")
    with cols[3]: kpi("Net 30-day cash flow",money(net_30),"Inflow less outflow")
    st.caption("Estimated balance is a modelled figure, not a verified bank balance.")
    section("CASH FLOW","Money movement","Compare incoming and outgoing money across your transaction history.")
    left,right=st.columns([1.7,1],gap="large")
    with left:
        daily=df.groupby([df["date"].dt.date,"type"],as_index=False)["amount"].sum()
        daily.columns=["Date","Type","Amount"]
        fig=px.area(daily,x="Date",y="Amount",color="Type",color_discrete_map={"Inflow":"#45dfad","Outflow":"#ff7185"})
        fig.update_traces(line=dict(width=2),opacity=.76)
        st.markdown('<div class="panel">',unsafe_allow_html=True); panel_title("Cash flow timeline","Daily inflow and outflow"); st.plotly_chart(chart_style(fig,340),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
    with right:
        expense=df[df["type"]=="Outflow"].groupby("category",as_index=False)["amount"].sum().sort_values("amount",ascending=False)
        fig=px.pie(expense,names="category",values="amount",hole=.72,color_discrete_sequence=["#45dfad","#82aaff","#f3c875","#b69cff","#ff7185","#55c6d9","#8da3b8"])
        fig.update_traces(textposition="inside",textinfo="percent")
        st.markdown('<div class="panel">',unsafe_allow_html=True); panel_title("Where money goes","Expense composition"); st.plotly_chart(chart_style(fig,340),use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
    section("ACTIVITY","Latest transactions","Most recent entries in your ledger.")
    recent=df.sort_values("date",ascending=False).head(8).copy()
    recent["date"]=format_dates(recent["date"])
    table(recent,330)
    # concise insight rail
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="panel">',unsafe_allow_html=True); panel_title("Cash flow signal","Recent 30-day position")
        if net_30>=0: st.markdown('<span class="pill">POSITIVE NET FLOW</span>',unsafe_allow_html=True); st.write("Recent inflows are higher than outflows.")
        else: st.warning("Recent outflows exceed inflows. Review collections and operating expenses.")
        st.markdown('</div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel">',unsafe_allow_html=True); panel_title("Data coverage","Loaded transaction records")
        st.markdown(f'<div style="font:800 25px Manrope;color:#f4f7fc">{len(df):,}</div><div class="panel-sub">Valid Inflow and Outflow records available for analysis.</div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ============================================================
# CASH FLOW
# ============================================================
elif page=="Cash Flow":
    header("PREDICTIVE INTELLIGENCE","Cash flow forecast",f"Modelled financial outlook for the next {forecast_days} days.")
    try:
        forecast=forecast_cashflow(df,days=forecast_days,opening_balance=opening_balance)
        if forecast is None or forecast.empty: st.warning("The forecasting model returned no results.")
        else:
            a,b,c=st.columns(3)
            with a: kpi("Predicted inflow",money(forecast["predicted_inflow"].sum()),"Forecast period")
            with b: kpi("Predicted outflow",money(forecast["predicted_outflow"].sum()),"Forecast period")
            with c: kpi("Projected closing balance",money(forecast["closing_balance"].iloc[-1]),"At end of forecast")
            section("FORECAST MODEL","Expected money movement","Daily predicted inflows and outflows.")
            chart=forecast.melt(id_vars=["date"],value_vars=["predicted_inflow","predicted_outflow"],var_name="Type",value_name="Amount")
            chart["Type"]=chart["Type"].map({"predicted_inflow":"Predicted inflow","predicted_outflow":"Predicted outflow"})
            fig=px.bar(chart,x="date",y="Amount",color="Type",barmode="group",color_discrete_map={"Predicted inflow":"#45dfad","Predicted outflow":"#ff7185"})
            st.plotly_chart(chart_style(fig,350),use_container_width=True)
            section("LIQUIDITY OUTLOOK","Projected closing balance","How the model expects your balance to move.")
            fig=px.area(forecast,x="date",y="closing_balance",markers=True,color_discrete_sequence=["#45dfad"])
            fig.update_traces(line=dict(width=3),fill="tozeroy")
            st.plotly_chart(chart_style(fig,320),use_container_width=True)
            section("MODEL OUTPUT","Daily forecast details","Raw daily estimates returned by the forecasting function.")
            shown=forecast.copy(); shown["date"]=format_dates(shown["date"]); table(shown,330)
            st.download_button("Download forecast CSV",forecast.to_csv(index=False).encode("utf-8"),"finsightai_forecast.csv","text/csv")
    except Exception as exc: error_box("Cash flow forecast",exc)

# ============================================================
# ANOMALY DETECTION
# ============================================================
elif page=="Anomaly Detection":
    header("RISK INTELLIGENCE","Anomaly detection","Identify unusual expense patterns with the Isolation Forest model.")
    try:
        anomalies=detect_anomalies(df)
        unusual=anomalies[anomalies["anomaly_status"]=="Unusual Expense"].copy()
        normal=anomalies[anomalies["anomaly_status"]=="Normal"].copy()
        a,b,c=st.columns(3)
        with a: kpi("Records analysed",f"{len(anomalies):,}","Model input")
        with b: kpi("Flagged expenses",f"{len(unusual):,}","Requires review")
        with c: kpi("Normal records",f"{len(normal):,}","Not flagged")
        if not unusual.empty:
            st.warning("An unusual transaction is not automatically fraud. Review the context before taking action.")
            section("OUTLIER DISTRIBUTION","Flagged expenses by category","Larger or statistically unusual expenses surfaced by the model.")
            fig=px.bar(unusual,x="category",y="amount",color="anomaly_score",hover_data=["date","payment_mode"],color_continuous_scale=["#ff7185","#f3c875","#45dfad"])
            st.plotly_chart(chart_style(fig,350),use_container_width=True)
            shown=unusual[["date","category","amount","payment_mode","anomaly_score"]].copy()
            shown["date"]=format_dates(shown["date"])
            shown=shown.rename(columns={"date":"Date","category":"Category","amount":"Amount (₹)","payment_mode":"Payment mode","anomaly_score":"Anomaly score"})
            section("REVIEW QUEUE","Transactions to inspect","These entries differ from the model's learned patterns.")
            table(shown,400)
            st.download_button("Export flagged transactions",shown.to_csv(index=False).encode("utf-8"),"finsightai_anomalies.csv","text/csv")
        else: st.success("No unusual expenses were detected in the current dataset.")
        st.caption("This model highlights statistical outliers; it does not establish fraud or wrongdoing.")
    except Exception as exc: error_box("Anomaly detection",exc)

# ============================================================
# BUSINESS HEALTH
# ============================================================
elif page=="Business Health":
    header("BUSINESS INTELLIGENCE","Business health","A weighted view of reserves, cash coverage and consistency.")
    try:
        health=calculate_business_health(df,opening_balance=opening_balance)
        score=max(0,min(100,float(health["health_score"])))
        left,right=st.columns([.85,1.5],gap="large")
        with left:
            st.markdown(f'<div class="panel" style="text-align:center;padding:27px 15px"><div class="eyebrow">OVERALL HEALTH SCORE</div><div style="font:800 64px Manrope;color:#45dfad">{score:.0f}<span style="font-size:18px;color:#8fa0b5">/100</span></div><span class="pill">{health["status"].upper()}</span><div class="panel-sub" style="margin-top:15px">Calculated from available transaction data</div></div>',unsafe_allow_html=True)
        with right:
            gauge=go.Figure(go.Indicator(mode="gauge+number",value=score,number={"suffix":"/100","font":{"size":34,"color":"#f4f7fc"}},gauge={"axis":{"range":[0,100],"tickcolor":"#8494a9"},"bar":{"color":"#45dfad","thickness":.28},"bgcolor":"#17263a","borderwidth":0,"steps":[{"range":[0,45],"color":"#39232f"},{"range":[45,65],"color":"#3a3426"},{"range":[65,100],"color":"#15382f"}]},title={"text":"Financial resilience","font":{"color":"#aab8ca","size":14}}))
            st.plotly_chart(chart_style(gauge,270),use_container_width=True)
        section("HEALTH BREAKDOWN","Score components","Weighted dimensions used by the health model.")
        cols=st.columns(3)
        metrics=[("Reserve score",health["reserve_score"],"40% weight"),("Coverage score",health["coverage_score"],"35% weight"),("Consistency score",health["consistency_score"],"25% weight")]
        for col,(label,value,note) in zip(cols,metrics):
            with col: kpi(label,f"{value}/100",note)
        section("OPERATING POSITION","Liquidity indicators","Supporting metrics for the current business position.")
        cols=st.columns(3)
        for col,(label,value) in zip(cols,[("Cash runway",f'{health["runway_days"]} days'),("Coverage ratio",f'{health["coverage_ratio"]}x'),("Positive cash-flow days",f'{health["positive_days"]}/30')]):
            with col: kpi(label,value,"Model output")
        section("NEXT STEPS","Decision support","Simple observations based on the returned indicators.")
        if health["reserve_score"]<60: st.warning("Consider building a larger cash reserve to improve short-term resilience.")
        else: st.success("The reserve indicator is relatively strong based on the available data.")
        if health["coverage_ratio"]<1: st.warning("Recent inflows are below outflows. Review operating costs and collections.")
        else: st.success("Recent inflows cover outflows based on the model's coverage calculation.")
        if health["consistency_score"]<60: st.warning("Monitor daily cash flow and plan for days with weaker collections.")
        else: st.success("The consistency indicator suggests a relatively steady pattern.")
        st.caption("Prototype score only; it is not a credit rating, audit or guarantee of future performance.")
    except Exception as exc: error_box("Business health",exc)

# ============================================================
# AI COPILOT
# ============================================================
elif page=="AI Copilot":
    header("CONVERSATIONAL INTELLIGENCE","Your AI finance copilot","Ask questions about your business finances in natural language.")
    st.markdown('<div class="hero"><div class="hero-kicker">LOCAL AI ASSISTANT</div><div class="hero-title">Ask. Understand. Take action.</div><div class="hero-copy">Explore cash flow, spending patterns, affordability and business performance with your locally running AI model.</div></div>',unsafe_allow_html=True)
    if "copilot_messages" not in st.session_state: st.session_state.copilot_messages=[]
    suggestions=["Summarise my recent financial performance","Are my expenses increasing?","What is my business health score?"]
    cols=st.columns(3)
    for col,suggestion in zip(cols,suggestions):
        with col:
            if st.button(suggestion,use_container_width=True,key="ask_"+suggestion):
                st.session_state["copilot_pending_prompt"]=suggestion
    for message in st.session_state.copilot_messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    question=st.chat_input("Ask FinSightAI about your business...")
    if st.session_state.get("copilot_pending_prompt"): question=st.session_state.pop("copilot_pending_prompt")
    if question:
        history=st.session_state.copilot_messages[-8:]
        st.session_state.copilot_messages.append({"role":"user","content":question})
        with st.chat_message("user"): st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Analysing your financial context..."):
                try:
                    answer=local_finance_copilot(df,question,history=history,opening_balance=opening_balance)
                except Exception as exc:
                    answer=f"I couldn't reach the local AI model. Check that Ollama is running and qwen2.5:3b is installed. Technical detail: {exc}"
                st.markdown(answer)
        st.session_state.copilot_messages.append({"role":"assistant","content":answer})
    if st.session_state.copilot_messages and st.button("Clear conversation"):
        st.session_state.copilot_messages=[]; st.rerun()

# ============================================================
# PURCHASE PLANNER
# ============================================================
elif page=="Purchase Planner":
    header("PURCHASE INTELLIGENCE","Smart purchase planner","Evaluate a planned purchase without compromising your cash reserve.")
    st.markdown('<div class="hero"><div class="hero-kicker">DECISION SUPPORT</div><div class="hero-title">Plan the purchase. Protect your runway.</div><div class="hero-copy">Compare the purchase against projected balances and a reserve for upcoming operating expenses.</div></div>',unsafe_allow_html=True)
    l,r=st.columns(2,gap="large")
    with l:
        purchase_amount=st.number_input("Purchase amount (₹)",min_value=0.0,value=25000.0,step=1000.0)
        purchase_in_days=st.number_input("Purchase planned after (days)",min_value=1,max_value=30,value=1)
    with r:
        reserve_days=st.selectbox("Maintain expense reserve for",[7,14,30],index=0,format_func=lambda v:f"{v} days")
        st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
        analyse=st.button("Analyse purchase affordability",type="primary",use_container_width=True)
    if analyse:
        if purchase_amount<=0: st.warning("Enter a purchase amount greater than zero.")
        else:
            with st.spinner("Evaluating projected affordability..."):
                try:
                    result=smart_purchase_planner(df,purchase_amount=purchase_amount,opening_balance=opening_balance,purchase_in_days=purchase_in_days,reserve_days=reserve_days)
                    section("PURCHASE ASSESSMENT","Your decision snapshot","Forecast-based estimates for the selected purchase.")
                    cols=st.columns(3)
                    for col,(label,key) in zip(cols,[("Balance before purchase","balance_before_purchase"),("Balance after purchase","balance_after_purchase"),("Maximum safe purchase","maximum_safe_purchase")]):
                        with col: kpi(label,money(result[key]),"Model estimate")
                    cols=st.columns(2)
                    for col,(label,key) in zip(cols,[("Minimum projected balance","minimum_projected_balance"),("Required safety reserve","safety_reserve")]):
                        with col: kpi(label,money(result[key]),"Model estimate")
                    if result["risk"]=="Low Risk": st.success(f'LOW RISK · {result["recommendation"]}')
                    elif result["risk"]=="Moderate Risk": st.warning(f'MODERATE RISK · {result["recommendation"]}')
                    else: st.error(f'HIGH RISK · {result["recommendation"]}')
                    st.caption("This is a model-based estimate, not a guarantee of future cash availability.")
                except Exception as exc: error_box("Purchase analysis",exc)

# ============================================================
# TRANSACTION EXPLORER
# ============================================================
elif page=="Transactions":
    header("FINANCIAL RECORDS","Transaction explorer","Search, filter and export the business ledger.")
    f1,f2,f3=st.columns([1.5,1,1])
    with f1: search=st.text_input("Search records",placeholder="Category, description or payment mode...")
    with f2: type_filter=st.selectbox("Transaction type",["All","Inflow","Outflow"])
    with f3:
        categories=["All"]+sorted(df["category"].dropna().astype(str).unique().tolist())
        category_filter=st.selectbox("Category",categories)
    filtered=df.copy()
    if search:
        mask=filtered.astype(str).apply(lambda col:col.str.contains(search,case=False,na=False,regex=False))
        filtered=filtered[mask.any(axis=1)]
    if type_filter!="All": filtered=filtered[filtered["type"]==type_filter]
    if category_filter!="All": filtered=filtered[filtered["category"].astype(str)==category_filter]
    inflow=filtered.loc[filtered["type"]=="Inflow","amount"].sum()
    outflow=filtered.loc[filtered["type"]=="Outflow","amount"].sum()
    cols=st.columns(3)
    with cols[0]: kpi("Matching records",f"{len(filtered):,}","Current filters")
    with cols[1]: kpi("Matched inflows",money(inflow),"Filtered total")
    with cols[2]: kpi("Matched outflows",money(outflow),"Filtered total")
    shown=filtered.sort_values("date",ascending=False).copy()
    shown["date"]=format_dates(shown["date"])
    shown=shown.rename(columns={"date":"Date","type":"Type","category":"Category","amount":"Amount (₹)","payment_mode":"Payment mode","description":"Description"})
    section("LEDGER","Matching transactions",f"{len(filtered):,} records match your current filters.")
    table(shown,470)
    st.download_button("Export filtered transactions",filtered.to_csv(index=False).encode("utf-8"),"finsightai_transactions.csv","text/csv")

# ---------------------------- FOOTER ----------------------------
st.markdown('<div class="footer">◆ &nbsp; FINSIGHTAI &nbsp; · &nbsp; AI-POWERED FINANCIAL INTELLIGENCE &nbsp; · &nbsp; ARTHATON 2026</div>',unsafe_allow_html=True)
