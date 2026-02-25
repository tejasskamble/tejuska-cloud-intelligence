import streamlit as st
import pandas as pd
import numpy as np
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu, metric_card

st.set_page_config(page_title="GreenOps | TEJUSKA", layout="wide")

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
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Sustainability & Carbon Footprint (GreenOps)</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Track and optimize the environmental impact of your cloud infrastructure.</p>', unsafe_allow_html=True)

# Metric cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(metric_card("Total CO2e Emissions (MT)", "24.8", None, st.session_state.theme), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Energy Consumed (kWh)", "38,450", None, st.session_state.theme), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Equivalent Trees Planted", "412", None, st.session_state.theme), unsafe_allow_html=True)

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

# Emissions by provider chart
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Emissions by Cloud Provider</h2>', unsafe_allow_html=True)
emissions_data = pd.DataFrame({
    "Provider": ["AWS", "Azure", "GCP"],
    "CO2e (MT)": [12.4, 7.8, 4.6]
})
st.bar_chart(emissions_data.set_index("Provider"))

# AI recommendation card
st.markdown(
    """
    <div class="p-4 mt-4 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
        <p class="text-sm text-slate-500 dark:text-slate-400">AI Sustainability Tip</p>
        <p class="text-base text-slate-900 dark:text-slate-50">Moving workload from us-east-1 to eu-north-1 (Sweden) will reduce carbon emissions by 42% due to renewable energy grids.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional: Emissions trend over time
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mt-6">Monthly CO2e Trend</h2>', unsafe_allow_html=True)
dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq="M")
trend = np.random.normal(25, 3, 12).cumsum()
trend_df = pd.DataFrame({"Date": dates, "CO2e (MT)": trend})
st.line_chart(trend_df.set_index("Date"))
