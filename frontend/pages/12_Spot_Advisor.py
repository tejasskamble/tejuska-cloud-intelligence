import streamlit as st
import pandas as pd
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="Spot Advisor | TEJUSKA", layout="wide")

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

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">AI Spot Instance Migration Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Leverage volatile spot markets safely to reduce compute costs by up to 80%.</p>', unsafe_allow_html=True)

# Eligible workloads table
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Eligible Stateless Workloads</h2>', unsafe_allow_html=True)

eligible_df = pd.DataFrame({
    "Instance ID": ["i-0a1b2c3d4e5f", "i-1b2c3d4e5f6a", "i-2c3d4e5f6a7b", "i-3d4e5f6a7b8c"],
    "Current Type": ["t3.medium (On-Demand)", "c5.large (On-Demand)", "m5.xlarge (On-Demand)", "r5.large (On-Demand)"],
    "Suggested Spot Type": ["t3.medium (Spot)", "c5.large (Spot)", "m5.xlarge (Spot)", "r5.large (Spot)"],
    "Potential Monthly Savings": [32.40, 58.20, 112.50, 47.80],
    "Interruption Risk": ["Low", "Medium", "High", "Low"]
})

def risk_color(risk):
    colors = {
        "Low": "text-emerald-600 dark:text-emerald-400",
        "Medium": "text-amber-600 dark:text-amber-400",
        "High": "text-rose-600 dark:text-rose-400"
    }
    return colors.get(risk, "")

# Display with colored risk
for idx, row in eligible_df.iterrows():
    st.markdown(
        f"""
        <div class="p-3 mb-2 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-between">
            <div class="flex-1">
                <span class="font-mono text-sm">{row['Instance ID']}</span>
            </div>
            <div class="flex-1 text-sm">
                {row['Current Type']} → <span class="font-semibold text-indigo-600 dark:text-indigo-400">{row['Suggested Spot Type']}</span>
            </div>
            <div class="flex-1 text-sm font-medium">
                ${row['Potential Monthly Savings']}/mo
            </div>
            <div class="flex-1 text-sm font-medium {risk_color(row['Interruption Risk'])}">
                {row['Interruption Risk']} Risk
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Form to trigger migration
st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Trigger Spot Migration</h2>', unsafe_allow_html=True)

with st.form("spot_migration_form"):
    selected_instance = st.selectbox("Select Workload", eligible_df["Instance ID"].tolist())
    risk_ack = st.checkbox("I acknowledge the interruption risk and have designed for fault tolerance")
    submitted = st.form_submit_button("Trigger Agentic Spot Migration Pipeline", type="primary", use_container_width=True)

if submitted:
    if risk_ack:
        with st.spinner("Initiating spot migration..."):
            import time
            time.sleep(2)
        st.success(f"Migration initiated for {selected_instance}. Spot request submitted.")
    else:
        st.error("Please acknowledge the interruption risk to proceed.")
