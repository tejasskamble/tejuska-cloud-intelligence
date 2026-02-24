import streamlit as st
from utils.ui_components import inject_tailwind, render_profile_menu, status_indicator

st.set_page_config(page_title="Cloud Connect | TEJUSKA", layout="wide")

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
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold">Multi-Cloud Integration Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70">Securely connect your AWS, Azure, and GCP environments to enable autonomous FinOps governance.</p>', unsafe_allow_html=True)

st.markdown('<h2 class="text-xl font-semibold mt-4">Active Connections Status</h2>', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(status_indicator("AWS", st.session_state.get("aws_connected", False), st.session_state.theme), unsafe_allow_html=True)
with col_b:
    st.markdown(status_indicator("Azure", st.session_state.get("azure_connected", False), st.session_state.theme), unsafe_allow_html=True)
with col_c:
    st.markdown(status_indicator("GCP", st.session_state.get("gcp_connected", False), st.session_state.theme), unsafe_allow_html=True)

st.markdown('<hr class="my-6 border-slate-300">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="flex items-center gap-2 mb-4">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FF9900" stroke-width="1.5">
                <path d="M5.5 8.5L12 3L18.5 8.5M5.5 15.5L12 21L18.5 15.5"/>
                <circle cx="12" cy="12" r="9"/>
            </svg>
            <h3 class="text-lg font-semibold">AWS Connection</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("aws_connect_form"):
        aws_access_key = st.text_input("Access Key ID", type="password")
        aws_secret_key = st.text_input("Secret Access Key", type="password")
        aws_region = st.selectbox("Region", ["ap-south-1 (Mumbai)", "us-east-1 (N. Virginia)"])
        submit_aws = st.form_submit_button("Connect AWS", type="primary", use_container_width=True)
        if submit_aws and aws_access_key:
            st.session_state["aws_connected"] = True
            st.rerun()

with col2:
    st.markdown(
        """
        <div class="flex items-center gap-2 mb-4">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#0078D4" stroke-width="1.5">
                <rect x="4" y="4" width="16" height="16" rx="2"/>
                <path d="M8 8h8v8H8z"/>
            </svg>
            <h3 class="text-lg font-semibold">Azure Connection</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("azure_connect_form"):
        tenant_id = st.text_input("Tenant ID", type="password")
        client_id = st.text_input("Client ID", type="password")
        client_secret = st.text_input("Client Secret", type="password")
        submit_azure = st.form_submit_button("Connect Azure", type="primary", use_container_width=True)
        if submit_azure and tenant_id:
            st.session_state["azure_connected"] = True
            st.rerun()

with col3:
    st.markdown(
        """
        <div class="flex items-center gap-2 mb-4">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                <circle cx="7" cy="12" r="3" fill="#EA4335"/>
                <circle cx="12" cy="17" r="3" fill="#34A853"/>
                <circle cx="17" cy="12" r="3" fill="#4285F4"/>
                <circle cx="12" cy="7" r="3" fill="#FBBC05"/>
            </svg>
            <h3 class="text-lg font-semibold">GCP Connection</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("gcp_connect_form"):
        gcp_project = st.text_input("Project ID")
        gcp_json = st.file_uploader("Upload Service Account JSON", type=["json"])
        submit_gcp = st.form_submit_button("Connect GCP", type="primary", use_container_width=True)
        if submit_gcp and gcp_project:
            st.session_state["gcp_connected"] = True
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
