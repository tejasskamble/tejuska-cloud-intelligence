import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_profile_menu

st.set_page_config(
    page_title="FinOps Dashboard | TEJUSKA",
    layout="wide",
)

# ---------- Theme state ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

# ---------- Dynamic CSS ----------
if st.session_state.theme == "dark":
    bg_color = "#0F172A"
    text_color = "#F8FAFC"
    secondary_bg = "#1E293B"
    primary_color = "#818CF8"
    accent_success = "#10B981"
    accent_error = "#EF4444"
    border_color = "#334155"
    card_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.3)"
else:
    bg_color = "#FFFFFF"
    text_color = "#0F172A"
    secondary_bg = "#F1F5F9"
    primary_color = "#6366F1"
    accent_success = "#059669"
    accent_error = "#DC2626"
    border_color = "#E2E8F0"
    card_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.05)"

st.markdown(f"""
<style>
    /* Copy the full CSS block from app.py (with variables) */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    h1, h2, h3, h4, h5, h6, p, li, .stMarkdown {{ color: {text_color} !important; }}
    h1 {{ background: linear-gradient(135deg, {primary_color} 0%, #A78BFA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
    .stButton button {{ border-radius: 8px; font-weight: 600; transition: all 0.2s ease; border: none; background: linear-gradient(135deg, {primary_color}, #818CF8); color: white; box-shadow: {card_shadow}; }}
    .stButton button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px {primary_color}80; }}
    .stButton button[kind="secondary"] {{ background: transparent; border: 1px solid {primary_color}; color: {primary_color}; box-shadow: none; }}
    .stButton button[kind="secondary"]:hover {{ background: {primary_color}; color: white; }}
    div[data-testid="metric-container"] {{ background: {secondary_bg}; border-radius: 16px; padding: 1.5rem 1rem; box-shadow: {card_shadow}; border: 1px solid {border_color}; transition: all 0.2s; }}
    div[data-testid="metric-container"]:hover {{ box-shadow: 0 20px 25px -5px {primary_color}40; border-color: {primary_color}; }}
    label[data-testid="stMetricLabel"] {{ font-size: 0.9rem; font-weight: 500; color: {text_color} !important; opacity: 0.8; }}
    .stDataFrame {{ border-radius: 12px; overflow: hidden; border: 1px solid {border_color}; }}
    .stDataFrame table {{ font-size: 0.9rem; color: {text_color} !important; }}
    .stDataFrame th {{ background: linear-gradient(135deg, {primary_color}, #A78BFA); color: white; font-weight: 600; padding: 0.75rem !important; }}
    .stDataFrame td {{ padding: 0.6rem !important; border-bottom: 1px solid {border_color}; background: {secondary_bg}; color: {text_color} !important; }}
    .stDataFrame tr:hover td {{ background-color: {primary_color}20; }}
    .status-active, .status-inactive {{ display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }}
    .status-active {{ background: {accent_success}; box-shadow: 0 0 0 2px {accent_success}40; }}
    .status-inactive {{ background: {accent_error}; box-shadow: 0 0 0 2px {accent_error}40; }}
    .pricing-card {{ background: {secondary_bg}; border-radius: 24px; padding: 2rem 1.5rem; border: 1px solid {border_color}; transition: transform 0.2s, border-color 0.2s; }}
    .pricing-card:hover {{ transform: scale(1.02); border-color: {primary_color}; }}
    .pricing-card h4 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: {primary_color}; }}
    .pricing-card ul {{ list-style-type: none; padding-left: 0; color: {text_color}; }}
    .pricing-card li {{ margin-bottom: 0.5rem; }}
    .provider-icon {{ width: 24px; height: 24px; vertical-align: middle; margin-right: 8px; display: inline-block; }}
    .social-icon {{ width: 22px; height: 22px; margin-right: 12px; vertical-align: middle; }}
    .github-icon {{ fill: {text_color}; }}
    .divider {{ display: flex; align-items: center; text-align: center; margin: 1.5rem 0; color: {text_color}; opacity: 0.5; }}
    .divider::before, .divider::after {{ content: ''; flex: 1; border-bottom: 1px solid {border_color}; }}
    .divider:not(:empty)::before {{ margin-right: .5em; }}
    .divider:not(:empty)::after {{ margin-left: .5em; }}
    .stTextInput input, .stTextInput textarea {{ border-radius: 8px; border: 1px solid {border_color}; background: {secondary_bg}; color: {text_color}; }}
    .stTextInput input:focus {{ border-color: {primary_color}; box-shadow: 0 0 0 2px {primary_color}40; }}
    .css-1d391kg, .css-1wrcr25 {{ background-color: {secondary_bg}; }}
</style>
""", unsafe_allow_html=True)

# ---------- Global profile menu ----------
render_profile_menu()

# ---------- Authentication gate ----------
if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

BACKEND_URL: str = st.secrets.get("BACKEND_URL", "http://localhost:7860")
TENANT_ID: str   = st.session_state.get("tenant_id", "")

st.markdown("# FinOps Dashboard")
st.markdown(
    "Real-time multi-cloud cost visibility across AWS, GCP, and Azure — "
    "standardised to the FOCUS 1.1 specification."
)
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Spend MTD",      value="$12,340.50",  delta="-8.2% vs last month")
col2.metric(label="Projected Month-End",  value="$15,200.00")
col3.metric(label="Potential Savings",    value="$2,100.00",   delta="Identified by ABACUS")
col4.metric(label="Active Resources",     value="148")

st.divider()

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

st.markdown("### Daily Spend Trend (Last 30 Days)")
dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq="D")
costs = (pd.Series(range(30)).apply(lambda x: 380 + (x % 7) * 45 + (x % 3) * 20))
trend_df = pd.DataFrame({"Date": dates, "Cost (USD)": costs})
fig2 = px.line(trend_df, x="Date", y="Cost (USD)", template="plotly_white")
fig2.update_layout(font_family="Inter, Segoe UI, sans-serif")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Top Services by Spend")
services_df = pd.DataFrame({
    "Service":        ["Amazon EC2", "Amazon S3", "Cloud Run", "Cloud SQL", "Azure VMs"],
    "Provider":       ["AWS", "AWS", "GCP", "GCP", "Azure"],
    "Billed Cost ($)": [4200.10, 1200.50, 980.30, 760.20, 640.15],
    "% of Total":     ["34.1%", "9.7%", "7.9%", "6.2%", "5.2%"],
})
st.dataframe(services_df, use_container_width=True, hide_index=True)
