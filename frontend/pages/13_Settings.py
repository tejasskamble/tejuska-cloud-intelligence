import streamlit as st
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="Settings | TEJUSKA", layout="wide")

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"
    # Other sidebar items can go here...
    render_bottom_profile()  # <-- always last

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

render_profile_menu(st.session_state.theme)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Global Settings & Preferences</h1>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["My Account", "Cloud API Keys", "Notifications", "Security"])

with tab1:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Account Information</h2>', unsafe_allow_html=True)
    with st.form("account_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value="Admin User")
            email = st.text_input("Email", value="admin@tejuska.io")
        with col2:
            role = st.selectbox("Role", ["FinOps Admin", "Developer", "Viewer"], index=0)
        if st.form_submit_button("Update Profile", type="primary"):
            st.success("Profile updated successfully.")

with tab2:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Cloud Provider Credentials</h2>', unsafe_allow_html=True)
    st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-4">Keys are stored encrypted. Existing keys are masked.</p>', unsafe_allow_html=True)

    with st.form("aws_keys"):
        st.markdown("#### AWS")
        aws_key = st.text_input("AWS Access Key ID", value="AKIA••••••••••••••••", type="password")
        aws_secret = st.text_input("AWS Secret Access Key", value="••••••••••••••••••••", type="password")
        if st.form_submit_button("Validate & Save AWS Keys"):
            st.success("AWS keys validated and saved.")

    with st.form("azure_keys"):
        st.markdown("#### Azure")
        azure_tenant = st.text_input("Azure Tenant ID", value="••••••••-••••-••••-••••-••••••••••••", type="password")
        azure_client = st.text_input("Azure Client ID", value="••••••••-••••-••••-••••-••••••••••••", type="password")
        azure_secret = st.text_input("Azure Client Secret", value="••••••••••••••••••••", type="password")
        if st.form_submit_button("Validate & Save Azure Keys"):
            st.success("Azure keys validated and saved.")

    with st.form("gcp_keys"):
        st.markdown("#### GCP")
        gcp_project = st.text_input("GCP Project ID", value="my-project-123")
        gcp_json = st.file_uploader("Upload Service Account JSON", type=["json"])
        if st.form_submit_button("Validate & Save GCP Keys"):
            st.success("GCP keys validated and saved.")

with tab3:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Notification Preferences</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        email_alerts = st.toggle("Email Alerts on Anomalies", value=True)
        weekly_reports = st.toggle("Weekly PDF Reports", value=False)
    with col2:
        auto_kill_approvals = st.toggle("Agentic Auto‑Kill Approvals", value=True)
        slack_integration = st.toggle("Slack Notifications", value=False)
    if st.button("Save Notification Settings", type="primary"):
        st.success("Notification preferences saved.")

with tab4:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Password & Security</h2>', unsafe_allow_html=True)
    with st.form("password_form"):
        current_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password", type="password")
        confirm_pw = st.text_input("Confirm New Password", type="password")
        if st.form_submit_button("Change Password", type="primary"):
            if new_pw != confirm_pw:
                st.error("Passwords do not match.")
            else:
                st.success("Password changed successfully.")

    st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Two‑Factor Authentication (2FA)</h2>', unsafe_allow_html=True)
    enable_2fa = st.toggle("Enable 2FA", value=False)
    if enable_2fa:
        st.info("2FA setup instructions would appear here (QR code, etc.).")
