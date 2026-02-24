import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import inject_tailwind, render_profile_menu, metric_card

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

bg_class = "bg-slate-50" if st.session_state.theme == "light" else "bg-slate-900"
text_class = "text-slate-900" if st.session_state.theme == "light" else "text-slate-50"

st.markdown(f'<div class="{bg_class} min-h-screen {text_class} p-6">', unsafe_allow_html=True)

render_profile_menu(st.session_state.theme)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold">FinOps Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70">Real-time multi-cloud cost visibility across AWS, GCP, and Azure — standardised to the FOCUS 1.1 specification.</p>', unsafe_allow_html=True)

# Metrics row using custom metric cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_card("Total Spend MTD", "$12,340.50", "-8.2% vs last month", st.session_state.theme), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Projected Month-End", "$15,200.00", None, st.session_state.theme), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Potential Savings", "$2,100.00", "Identified by ABACUS", st.session_state.theme), unsafe_allow_html=True)
with col4:
    st.markdown(metric_card("Active Resources", "148", None, st.session_state.theme), unsafe_allow_html=True)

st.markdown('<hr class="my-6 border-slate-300">', unsafe_allow_html=True)

st.markdown('<h2 class="text-xl font-semibold">Cost by Cloud Provider</h2>', unsafe_allow_html=True)
sample_data = pd.DataFrame({
    "Provider": ["AWS", "GCP", "Azure"],
    "Billed Cost": [7800.25, 2900.10, 1640.15],
})
fig = px.bar(sample_data, x="Provider", y="Billed Cost", color="Provider", labels={"Billed Cost": "Billed Cost (USD)"}, template="plotly_white")
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown('<h2 class="text-xl font-semibold mt-6">Daily Spend Trend (Last 30 Days)</h2>', unsafe_allow_html=True)
dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq="D")
costs = (pd.Series(range(30)).apply(lambda x: 380 + (x % 7) * 45 + (x % 3) * 20))
trend_df = pd.DataFrame({"Date": dates, "Cost (USD)": costs})
fig2 = px.line(trend_df, x="Date", y="Cost (USD)", template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

st.markdown('<h2 class="text-xl font-semibold mt-6">Top Services by Spend</h2>', unsafe_allow_html=True)
services_df = pd.DataFrame({
    "Service": ["Amazon EC2", "Amazon S3", "Cloud Run", "Cloud SQL", "Azure VMs"],
    "Provider": ["AWS", "AWS", "GCP", "GCP", "Azure"],
    "Billed Cost ($)": [4200.10, 1200.50, 980.30, 760.20, 640.15],
    "% of Total": ["34.1%", "9.7%", "7.9%", "6.2%", "5.2%"],
})
st.dataframe(services_df, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)
