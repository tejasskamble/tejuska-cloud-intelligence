import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FinOps Dashboard | TEJUSKA",
    layout="wide",
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Copy the full CSS block from app.py here */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: var(--background-color); color: var(--text-color); }
    h1, h2, h3 { font-weight: 700; letter-spacing: -0.02em; }
    h1 { background: linear-gradient(135deg, var(--primary-color) 0%, #A78BFA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .stButton button { border-radius: 8px; font-weight: 600; transition: all 0.2s ease; border: none; background: linear-gradient(135deg, var(--primary-color), #818CF8); color: white; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3); }
    .stButton button[kind="secondary"] { background: transparent; border: 1px solid var(--primary-color); color: var(--primary-color); box-shadow: none; }
    .stButton button[kind="secondary"]:hover { background: var(--primary-color); color: white; }
    div[data-testid="metric-container"] { background: var(--secondary-background-color); border-radius: 16px; padding: 1.5rem 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid rgba(0,0,0,0.05); transition: all 0.2s; }
    div[data-testid="metric-container"]:hover { box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.1); border-color: var(--primary-color); }
    label[data-testid="stMetricLabel"] { font-size: 0.9rem; font-weight: 500; color: var(--text-color); opacity: 0.8; }
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid var(--secondary-background-color); }
    .stDataFrame table { font-size: 0.9rem; }
    .stDataFrame th { background: linear-gradient(135deg, var(--primary-color), #A78BFA); color: white; font-weight: 600; padding: 0.75rem !important; }
    .stDataFrame td { padding: 0.6rem !important; border-bottom: 1px solid var(--secondary-background-color); }
    .stDataFrame tr:hover td { background-color: var(--secondary-background-color); }
    .status-active, .status-inactive { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
    .status-active { background: #10B981; box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2); }
    .status-inactive { background: #EF4444; box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2); }
    .pricing-card { background: var(--secondary-background-color); border-radius: 24px; padding: 2rem 1.5rem; border: 1px solid rgba(0,0,0,0.05); transition: transform 0.2s, border-color 0.2s; }
    .pricing-card:hover { transform: scale(1.02); border-color: var(--primary-color); }
    .pricing-card h4 { font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: var(--primary-color); }
    .pricing-card ul { list-style-type: none; padding-left: 0; }
    .pricing-card li { margin-bottom: 0.5rem; }
    .provider-icon { width: 24px; height: 24px; vertical-align: middle; margin-right: 8px; display: inline-block; }
    .social-icon { width: 22px; height: 22px; margin-right: 12px; vertical-align: middle; }
    .divider { display: flex; align-items: center; text-align: center; margin: 1.5rem 0; color: var(--text-color); opacity: 0.5; }
    .divider::before, .divider::after { content: ''; flex: 1; border-bottom: 1px solid var(--secondary-background-color); }
    .divider:not(:empty)::before { margin-right: .5em; }
    .divider:not(:empty)::after { margin-left: .5em; }
    .stTextInput input, .stTextInput textarea { border-radius: 8px; border: 1px solid var(--secondary-background-color); background: var(--background-color); color: var(--text-color); }
    .stTextInput input:focus { border-color: var(--primary-color); box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2); }
</style>
""", unsafe_allow_html=True)

# ==================== AUTHENTICATION GATE ====================
if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

BACKEND_URL: str = st.secrets.get("BACKEND_URL", "http://localhost:7860")
TENANT_ID: str   = st.session_state.get("tenant_id", "")

# ==================== PAGE HEADER ====================
st.markdown("# FinOps Dashboard")
st.markdown(
    "Real-time multi-cloud cost visibility across AWS, GCP, and Azure — "
    "standardised to the FOCUS 1.1 specification."
)
st.divider()

# ==================== KEY METRICS ====================
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Spend MTD",      value="$12,340.50",  delta="-8.2% vs last month")
col2.metric(label="Projected Month-End",  value="$15,200.00")
col3.metric(label="Potential Savings",    value="$2,100.00",   delta="Identified by ABACUS")
col4.metric(label="Active Resources",     value="148")

st.divider()

# ==================== COST BREAKDOWN CHART ====================
st.markdown("### Cost by Cloud Provider")
sample_data = pd.DataFrame({
    "Provider":    ["AWS", "GCP", "Azure"],
    "Billed Cost": [7800.25, 2900.10, 1640.15],
})
fig = px.bar(
    sample_data,
    x="Provider",
    y="Billed Cost",
    color="Provider",
    labels={"Billed Cost": "Billed Cost (USD)"},
    template="plotly_white",
)
fig.update_layout(showlegend=False, font_family="Inter, Segoe UI, sans-serif")
st.plotly_chart(fig, use_container_width=True)

# ==================== DAILY SPEND TREND ====================
st.markdown("### Daily Spend Trend (Last 30 Days)")
dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq="D")
costs = (pd.Series(range(30)).apply(lambda x: 380 + (x % 7) * 45 + (x % 3) * 20))
trend_df = pd.DataFrame({"Date": dates, "Cost (USD)": costs})
fig2 = px.line(trend_df, x="Date", y="Cost (USD)", template="plotly_white")
fig2.update_layout(font_family="Inter, Segoe UI, sans-serif")
st.plotly_chart(fig2, use_container_width=True)

# ==================== TOP SERVICES TABLE ====================
st.markdown("### Top Services by Spend")
services_df = pd.DataFrame({
    "Service":        ["Amazon EC2", "Amazon S3", "Cloud Run", "Cloud SQL", "Azure VMs"],
    "Provider":       ["AWS", "AWS", "GCP", "GCP", "Azure"],
    "Billed Cost ($)": [4200.10, 1200.50, 980.30, 760.20, 640.15],
    "% of Total":     ["34.1%", "9.7%", "7.9%", "6.2%", "5.2%"],
})
st.dataframe(services_df, use_container_width=True, hide_index=True)
