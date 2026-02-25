import streamlit as st
import time
from utils.ui_components import inject_tailwind, get_theme_css
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="DevOps Pipeline Estimator | TEJUSKA", layout="wide")

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
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">CI/CD Pre-Deployment Cost Estimator</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Shift‑left FinOps: estimate infrastructure cost changes before merging code.</p>', unsafe_allow_html=True)

# File uploader – native, no wrapper
uploaded_file = st.file_uploader(
    "Upload Terraform Plan (.json) or CloudFormation Template",
    type=["json", "yaml", "yml", "txt"],
    help="Upload your infrastructure-as-code artifact to analyze cost impact."
)

# Analyze button – native Streamlit button (styling via global CSS)
if st.button("Run CI/CD Cost Analysis", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.error("Please upload a file first.")
    else:
        with st.spinner("Analyzing infrastructure changes..."):
            time.sleep(2.5)  # Simulate processing

        # Simulated result
        current_cost = 4200
        new_cost = 4550
        change = new_cost - current_cost
        change_pct = (change / current_cost) * 100

        # Display result card using Tailwind (custom HTML)
        st.markdown(
            f"""
            <div class="p-6 mt-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-md">
                <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-50 mb-3">Cost Impact Analysis</h3>
                <div class="grid grid-cols-3 gap-4 text-center">
                    <div>
                        <p class="text-sm text-slate-500 dark:text-slate-400">Current Infra Cost</p>
                        <p class="text-2xl font-bold text-slate-900 dark:text-slate-50">${current_cost}/mo</p>
                    </div>
                    <div>
                        <p class="text-sm text-slate-500 dark:text-slate-400">New Estimated Cost</p>
                        <p class="text-2xl font-bold text-slate-900 dark:text-slate-50">${new_cost}/mo</p>
                    </div>
                    <div>
                        <p class="text-sm text-slate-500 dark:text-slate-400">Net Change</p>
                        <p class="text-2xl font-bold {'text-emerald-600 dark:text-emerald-400' if change < 0 else 'text-amber-600 dark:text-amber-400'}">
                            {change:+,.0f}/mo ({change_pct:+.1f}%)
                        </p>
                    </div>
                </div>
                <div class="mt-4 p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg text-sm text-blue-800 dark:text-blue-200">
                    ℹ️ The estimated increase is due to additional storage and compute resources in the new deployment.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Optional: Additional guidance
st.markdown(
    """
    <div class="mt-8 text-sm text-slate-500 dark:text-slate-400">
        <p><strong>How it works:</strong> We parse your IaC, simulate resource changes, and estimate monthly costs using current cloud pricing.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
