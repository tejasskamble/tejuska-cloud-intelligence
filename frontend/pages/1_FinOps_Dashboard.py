"""
1_FinOps_Dashboard.py
=====================
TEJUSKA Cloud Intelligence
FinOps Dashboard - Multi-cloud billing overview, cost trends, and anomaly alerts.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FinOps Dashboard | TEJUSKA",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Authentication gate
# ---------------------------------------------------------------------------
if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

BACKEND_URL: str = st.secrets.get("BACKEND_URL", "http://localhost:7860")
TENANT_ID: str   = st.session_state.get("tenant_id", "")

# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------
st.markdown("# FinOps Dashboard")
st.markdown(
    "Real-time multi-cloud cost visibility across AWS, GCP, and Azure — "
    "standardised to the FOCUS 1.1 specification."
)
st.divider()

# ---------------------------------------------------------------------------
# Key metrics row (placeholders until live DB is connected)
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Spend MTD",      value="$12,340.50",  delta="-8.2% vs last month")
col2.metric(label="Projected Month-End",  value="$15,200.00")
col3.metric(label="Potential Savings",    value="$2,100.00",   delta="Identified by ABACUS")
col4.metric(label="Active Resources",     value="148")

st.divider()

# ---------------------------------------------------------------------------
# Cost breakdown chart
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Daily spend trend
# ---------------------------------------------------------------------------
st.markdown("### Daily Spend Trend (Last 30 Days)")
dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq="D")
costs = (
    pd.Series(range(30)).apply(lambda x: 380 + (x % 7) * 45 + (x % 3) * 20)
)
trend_df = pd.DataFrame({"Date": dates, "Cost (USD)": costs})
fig2 = px.line(
    trend_df, x="Date", y="Cost (USD)", template="plotly_white"
)
fig2.update_layout(font_family="Inter, Segoe UI, sans-serif")
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Top services table
# ---------------------------------------------------------------------------
st.markdown("### Top Services by Spend")
services_df = pd.DataFrame({
    "Service":        ["Amazon EC2", "Amazon S3", "Cloud Run", "Cloud SQL", "Azure VMs"],
    "Provider":       ["AWS", "AWS", "GCP", "GCP", "Azure"],
    "Billed Cost ($)": [4200.10, 1200.50, 980.30, 760.20, 640.15],
    "% of Total":     ["34.1%", "9.7%", "7.9%", "6.2%", "5.2%"],
})
st.dataframe(services_df, use_container_width=True, hide_index=True)
