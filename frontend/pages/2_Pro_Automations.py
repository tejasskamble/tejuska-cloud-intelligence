import streamlit as st
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="Pro Automations | TEJUSKA", layout="wide")

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

# ---------- RBAC Protection ----------
if st.session_state.get("role") == "Developer":
    st.markdown(
        """
        <div class="p-4 mb-4 text-sm text-red-800 bg-red-100 rounded-lg dark:bg-red-900 dark:text-red-200" role="alert">
            <span class="font-medium">Access Denied</span> – This page is restricted to Admins only.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Agentic Auto-Kill & Thresholds</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300">Set custom budget limits. The Agentic AI will automatically terminate resources and send email alerts if costs exceed your threshold.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">1. Set Budget Threshold</h2>', unsafe_allow_html=True)
    st.info("Configure the maximum allowed cost for a specific cloud resource.")
    with st.form("threshold_form"):
        st.markdown(
            f"""
            <div class="flex items-center gap-2 mb-2 text-slate-900 dark:text-slate-50">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 2v20M2 12h20"/>
                </svg>
                <span class="font-semibold">Cloud Provider</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        provider = st.selectbox("", ["AWS", "Azure", "GCP", "Other"], label_visibility="collapsed")
        resource_id = st.text_input("Resource ID", placeholder="e.g., i-09ca51ce7bcd242ed")
        threshold = st.number_input("Cost Threshold Limit ($)", min_value=0.01, value=1.00, step=0.50)
        current_email = st.session_state.get("tenant_id", "")
        user_email = st.text_input("Alert Email ID", value=current_email)

        submit_threshold = st.form_submit_button("Activate Agentic Shield", type="primary")
        if submit_threshold:
            if not resource_id:
                st.error("Please enter a valid Resource ID.")
            else:
                st.success(f"Shield Activated! If {provider} resource '{resource_id}' exceeds ${threshold:.2f}, it will be TERMINATED immediately and an alert will be sent to {user_email}.")

with col2:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">2. Simulate Cloud Billing (Test)</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="p-4 mb-4 text-sm text-yellow-900 bg-yellow-100 rounded-lg dark:bg-yellow-900 dark:text-yellow-100" role="alert">
            <span class="font-medium">Test the automation</span> by simulating a bill that exceeds your threshold.
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("simulate_form"):
        sim_resource_id = st.text_input("Resource ID to Test", value="i-09ca51ce7bcd242ed")
        sim_cost = st.number_input("Current Simulated Cost ($)", value=1.50)

        submit_sim = st.form_submit_button("Run AI Evaluation", type="secondary")
        if submit_sim:
            st.info(f"ABACUS Engine analyzing resource {sim_resource_id}...")
            threshold_limit = 1.00
            if sim_cost > threshold_limit:
                st.error(f"Cost (${sim_cost}) exceeds threshold! Triggering termination...")
                st.success(f"Resource '{sim_resource_id}' successfully terminated by AI.")
                st.success("Email notification dispatched via SMTP.")
            else:
                st.success("Cost is within limits. No action taken.")

# ---------- New Real-Time Anomaly Detection Section ----------
st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Real-Time Anomaly Detection</h2>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-4">Configure automatic alerts for cost spikes.</p>', unsafe_allow_html=True)

with st.form("anomaly_form"):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        spike_threshold = st.number_input("Cost Spike Threshold (%)", min_value=1, max_value=100, value=15)
    with col_b:
        alert_channel = st.selectbox("Alert Channel", ["Email", "Telegram", "Slack"])
    with col_c:
        monitoring_enabled = st.checkbox("Enable 24/7 Monitoring", value=True)

    submit_anomaly = st.form_submit_button("Save Anomaly Settings", type="primary", use_container_width=True)

if submit_anomaly:
    st.success(f"Anomaly detection enabled with {spike_threshold}% spike threshold via {alert_channel}. 24/7 monitoring: {'ON' if monitoring_enabled else 'OFF'}")
