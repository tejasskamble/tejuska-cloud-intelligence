import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.ui_components import inject_tailwind, get_theme_css, metric_card
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="Predictive Cost Analytics | TEJUSKA", layout="wide")

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"
    render_bottom_profile()

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Predictive Cost Analytics (ARIMA/LSTM)</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300">ML‑based forecasting of future cloud spend.</p>', unsafe_allow_html=True)

# Forecast horizon slider
horizon = st.select_slider(
    "Forecast Horizon",
    options=[7, 15, 30, 90],
    value=30,
    help="Number of days to forecast ahead"
)

# Metric cards
col1, col2 = st.columns(2)
with col1:
    st.markdown(metric_card("Predicted Next Month Bill", "$18,450", None, st.session_state.theme), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Est. Savings Opportunity", "$1,230", "via rightsizing", st.session_state.theme), unsafe_allow_html=True)

# Mock historical + forecasted data
np.random.seed(42)
dates_hist = pd.date_range(end=pd.Timestamp.today(), periods=90, freq="D")
historical = 10000 + np.cumsum(np.random.randn(90) * 200) + np.linspace(0, 5000, 90)

# Forecast: simple linear trend + noise
future_dates = pd.date_range(start=dates_hist[-1] + pd.Timedelta(days=1), periods=horizon, freq="D")
trend = np.linspace(historical[-1], historical[-1] * 1.2, horizon)
forecast = trend + np.random.randn(horizon) * 300

# Combine for plotting
df_hist = pd.DataFrame({"Date": dates_hist, "Cost": historical, "Type": "Historical"})
df_fore = pd.DataFrame({"Date": future_dates, "Cost": forecast, "Type": "Forecast"})
df_all = pd.concat([df_hist, df_fore], ignore_index=True)

# Plotly line chart with two colors
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_hist["Date"], y=df_hist["Cost"],
    mode="lines", name="Historical",
    line=dict(color="#6366F1", width=2)
))
fig.add_trace(go.Scatter(
    x=df_fore["Date"], y=df_fore["Cost"],
    mode="lines", name="Forecast",
    line=dict(color="#F59E0B", width=2, dash="dash")
))
fig.update_layout(
    template="plotly_white",
    xaxis_title="Date",
    yaxis_title="Cost (USD)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# Optional: show data table
with st.expander("View Raw Forecast Data"):
    st.dataframe(df_fore, use_container_width=True)
