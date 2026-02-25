import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu, metric_card

st.set_page_config(
    page_title="FinOps Dashboard | TEJUSKA",
    layout="wide",
)

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

render_profile_menu(st.session_state.theme)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

# Premium report generation button
col_btn, col_badge = st.columns([3, 1])
with col_btn:
    if st.button("📄 Generate Monthly FinOps Report (PDF)", type="primary", use_container_width=True):
        st.success("Your report is being generated. Download will start shortly.")
with col_badge:
    st.markdown(
        """
        <div class="bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200 text-sm font-medium px-3 py-1 rounded-full text-center">
            Data: Live Sync Active
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">FinOps Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300">Real-time multi-cloud cost visibility across AWS, GCP, and Azure — standardised to the FOCUS 1.1 specification.</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_card("Total Spend MTD", "$12,340.50", "-8.2% vs last month", st.session_state.theme), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Projected Month-End", "$15,200.00", None, st.session_state.theme), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Potential Savings", "$2,100.00", "Identified by ABACUS", st.session_state.theme), unsafe_allow_html=True)
with col4:
    st.markdown(metric_card("Active Resources", "148", None, st.session_state.theme), unsafe_allow_html=True)

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Cost by Cloud Provider</h2>', unsafe_allow_html=True)
sample_data = pd.DataFrame({
    "Provider": ["AWS", "GCP", "Azure"],
    "Billed Cost": [7800.25, 2900.10, 1640.15],
})
fig = px.bar(sample_data, x="Provider", y="Billed Cost", color="Provider", labels={"Billed Cost": "Billed Cost (USD)"}, template="plotly_white")
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown('<h2 class="text-xl font-semibold mt-6 text-slate-900 dark:text-slate-50">Daily Spend Trend (Last 30 Days)</h2>', unsafe_allow_html=True)
dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq="D")
costs = (pd.Series(range(30)).apply(lambda x: 380 + (x % 7) * 45 + (x % 3) * 20))
trend_df = pd.DataFrame({"Date": dates, "Cost (USD)": costs})
fig2 = px.line(trend_df, x="Date", y="Cost (USD)", template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

st.markdown('<h2 class="text-xl font-semibold mt-6 text-slate-900 dark:text-slate-50">Top Services by Spend</h2>', unsafe_allow_html=True)
services_df = pd.DataFrame({
    "Service": ["Amazon EC2", "Amazon S3", "Cloud Run", "Cloud SQL", "Azure VMs"],
    "Provider": ["AWS", "AWS", "GCP", "GCP", "Azure"],
    "Billed Cost ($)": [4200.10, 1200.50, 980.30, 760.20, 640.15],
    "% of Total": ["34.1%", "9.7%", "7.9%", "6.2%", "5.2%"],
})
st.dataframe(services_df, use_container_width=True, hide_index=True)

# ---------- NEW: AI-Powered Optimization Recommendations ----------
st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">AI-Powered Optimization Recommendations</h2>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-4">Zombie resources detected – idle or unattached assets that can be safely terminated.</p>', unsafe_allow_html=True)

# Simulated zombie resources data
zombie_data = pd.DataFrame({
    "Resource ID": ["vol-0a1b2c3d4e5f67890", "i-1234567890abcdef0", "eipalloc-0123456789abcdef"],
    "Type": ["EBS Volume (gp2, 100GB)", "EC2 t3.micro", "Elastic IP"],
    "Region": ["us-east-1", "eu-west-1", "ap-southeast-2"],
    "Monthly Cost": [8.00, 21.50, 3.60],
    "Status": ["Unattached", "CPU < 1% for 7 days", "Unassociated"]
})

st.dataframe(
    zombie_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Monthly Cost": st.column_config.NumberColumn(format="$%.2f")
    }
)

# Termination button with custom red styling
col_btn1, _ = st.columns([1, 3])
with col_btn1:
    if st.button("Terminate Selected Idle Resources (Save $450/mo)", key="terminate_btn", use_container_width=True):
        st.success("Selected resources have been terminated. Estimated savings: $450/month.")

# Add custom CSS to make the button red (warning style)
st.markdown(
    """
    <style>
        div[data-testid="baseButton-secondary"] button[kind="secondary"] {
            background-color: #ef4444 !important;
            border-color: #dc2626 !important;
            color: white !important;
        }
        div[data-testid="baseButton-secondary"] button[kind="secondary"]:hover {
            background-color: #dc2626 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
