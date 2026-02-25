import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu, metric_card
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="GreenOps | TEJUSKA", layout="wide")

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"
    render_bottom_profile()

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

render_profile_menu(st.session_state.theme)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Sustainability & Carbon Footprint (GreenOps)</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Track and optimize the environmental impact and CO2 emissions of your cloud infrastructure.</p>', unsafe_allow_html=True)

# Metric cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(metric_card("Total CO2e Emissions (MT)", "124.5", "-3.2% vs last month", st.session_state.theme), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Energy Consumed (kWh)", "12,450", None, st.session_state.theme), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Equivalent Trees Planted", "2,045", None, st.session_state.theme), unsafe_allow_html=True)

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

# Emissions by provider chart
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Emissions by Cloud Provider</h2>', unsafe_allow_html=True)

emissions_data = pd.DataFrame({
    "Provider": ["AWS", "Azure", "GCP"],
    "CO2e (MT)": [68.2, 34.8, 21.5]
})
fig = px.bar(emissions_data, x="Provider", y="CO2e (MT)", color="Provider",
             labels={"CO2e (MT)": "Metric Tons CO2e"}, template="plotly_white")
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# AI Tip Card
st.markdown(
    """
    <div class="p-5 mt-6 bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/30 dark:to-teal-900/30 rounded-xl border border-emerald-200 dark:border-emerald-800">
        <div class="flex items-start gap-3">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-1">
                <path d="M12 8v8m-4-4h8" />
                <circle cx="12" cy="12" r="10" />
            </svg>
            <div>
                <p class="font-semibold text-emerald-900 dark:text-emerald-200">AI Tip</p>
                <p class="text-emerald-800 dark:text-emerald-300">Moving workload from us-east-1 to eu-north-1 (Sweden) will reduce carbon emissions by 42% due to renewable energy grids.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
