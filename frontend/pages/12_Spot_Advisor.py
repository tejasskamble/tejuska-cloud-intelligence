import streamlit as st
import pandas as pd
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu

st.set_page_config(page_title="Spot Advisor | TEJUSKA", layout="wide")

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

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">AI Spot Instance Migration Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Leverage volatile spot markets safely to reduce compute costs by up to 80%.</p>', unsafe_allow_html=True)

# Data table of eligible workloads
eligible_workloads = pd.DataFrame({
    "Instance ID": ["i-0a1b2c3d4e5f6", "i-1a2b3c4d5e6f7", "i-2a3b4c5d6e7f8", "i-3a4b5c6d7e8f9", "i-4a5b6c7d8e9f0"],
    "Current Type (On-Demand)": ["m5.large", "c5.xlarge", "r5.large", "t3.medium", "m5.xlarge"],
    "Suggested Type (Spot)": ["m5.large", "c5.xlarge", "r5.large", "t3.medium", "m5.xlarge"],
    "Potential Monthly Savings ($)": [42.50, 89.20, 63.80, 15.30, 112.00],
    "Interruption Risk": ["Low", "Medium", "Low", "High", "Low"]
})

# Define a function to color-code risk
def color_risk(val):
    colors = {"Low": "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200",
              "Medium": "bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200",
              "High": "bg-rose-100 text-rose-800 dark:bg-rose-900 dark:text-rose-200"}
    return colors.get(val, "")

# Display table with custom HTML for risk badges
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Eligible Stateless Workloads</h2>', unsafe_allow_html=True)

# Convert DataFrame to HTML with risk badges
html_rows = ""
for _, row in eligible_workloads.iterrows():
    risk_badge = f'<span class="px-2 py-1 text-xs font-semibold rounded-full {color_risk(row["Interruption Risk"])}">{row["Interruption Risk"]}</span>'
    html_rows += f"""
    <tr class="border-b border-slate-200 dark:border-slate-700">
        <td class="px-4 py-2">{row['Instance ID']}</td>
        <td class="px-4 py-2">{row['Current Type (On-Demand)']}</td>
        <td class="px-4 py-2">{row['Suggested Type (Spot)']}</td>
        <td class="px-4 py-2">${row['Potential Monthly Savings ($)']:.2f}</td>
        <td class="px-4 py-2">{risk_badge}</td>
    </tr>
    """

st.markdown(
    f"""
    <table class="min-w-full text-sm text-left text-slate-900 dark:text-slate-50">
        <thead class="bg-slate-100 dark:bg-slate-800">
            <tr>
                <th class="px-4 py-2">Instance ID</th>
                <th class="px-4 py-2">Current Type (On-Demand)</th>
                <th class="px-4 py-2">Suggested Type (Spot)</th>
                <th class="px-4 py-2">Potential Monthly Savings ($)</th>
                <th class="px-4 py-2">Interruption Risk</th>
            </tr>
        </thead>
        <tbody>
            {html_rows}
        </tbody>
    </table>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

# Spot migration form
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Trigger Spot Migration</h2>', unsafe_allow_html=True)

with st.form("spot_migration_form"):
    selected_instance = st.selectbox("Select Instance ID", eligible_workloads["Instance ID"].tolist())
    confirmation = st.checkbox("I confirm that this workload is stateless and can handle interruptions.")
    submitted = st.form_submit_button("Trigger Agentic Spot Migration Pipeline", type="primary", use_container_width=True)

if submitted:
    if confirmation:
        st.success(f"Migration pipeline triggered for {selected_instance}. Spot instance will be provisioned and workload drained.")
    else:
        st.error("Please confirm that the workload is stateless.")
