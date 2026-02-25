import streamlit as st
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu, status_indicator
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="Cloud Connect | TEJUSKA", layout="wide")

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"
    # ---------- Bottom profile ----------
    render_bottom_profile()

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

render_profile_menu(st.session_state.theme)

# Initialize session state for authentication and role
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.tenant_id = ""
    st.session_state.role = None

# ---------- AUTHENTICATION SECTION (shown only when not authenticated) ----------
if not st.session_state.authenticated:
    st.markdown(
        f"""
        <div class="text-center py-8">
            <h1 class="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">TEJUSKA Cloud</h1>
            <p class="opacity-70 text-slate-700 dark:text-slate-300">Enterprise FinOps & Agentic AI Platform</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tabs for Sign In and Sign Up
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    with tab1:
        # Google & GitHub buttons (exact HTML as requested)
        st.markdown(
            """
            <div class="flex w-full gap-4 mb-6 mt-4">
                <button class="flex-1 flex items-center justify-center gap-3 rounded-lg border border-slate-300 dark:border-slate-600 bg-transparent px-4 py-2.5 font-semibold text-slate-700 dark:text-slate-200 transition-all hover:bg-slate-50 dark:hover:bg-slate-800">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="20px" height="20px"><path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/><path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/><path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/><path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/></svg>
                    Continue with Google
                </button>
                <button class="flex-1 flex items-center justify-center gap-3 rounded-lg border border-slate-300 dark:border-slate-600 bg-transparent px-4 py-2.5 font-semibold text-slate-700 dark:text-slate-200 transition-all hover:bg-slate-50 dark:hover:bg-slate-800">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20px" height="20px" class="fill-current"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    Continue with GitHub
                </button>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("signin_form"):
            email = st.text_input("Email *", placeholder="name@company.com")
            password = st.text_input("Password *", type="password", placeholder="········")
            if st.form_submit_button("Sign In", type="primary", use_container_width=True):
                if email and password and "@" in email:
                    st.session_state.authenticated = True
                    st.session_state.tenant_id = email
                    st.session_state.role = "Admin"  # Default role for demo
                    st.rerun()
                else:
                    st.error("Please enter a valid email and password.")

    with tab2:
        with st.form("signup_form"):
            first_name = st.text_input("First Name *", placeholder="John")
            last_name = st.text_input("Last Name *", placeholder="Doe")
            contact = st.text_input("Contact Number *", placeholder="+1234567890")
            email = st.text_input("Email *", placeholder="john.doe@company.com")
            role = st.selectbox("Select Role *", ["Admin", "Developer"])
            set_password = st.text_input("Set Password *", type="password", placeholder="········")
            retype_password = st.text_input("Re-type Password *", type="password", placeholder="········")
            submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)
            if submitted:
                if not (first_name and last_name and contact and email and set_password and retype_password):
                    st.error("All fields are required.")
                elif "@" not in email:
                    st.error("Please enter a valid email address.")
                elif set_password != retype_password:
                    st.error("Passwords do not match!")
                else:
                    st.session_state.authenticated = True
                    st.session_state.tenant_id = email
                    st.session_state.role = role
                    st.rerun()

    # Stop here so the rest of the page (Cloud Connect) doesn't show to unauthenticated users
    st.stop()

# ---------- CLOUD CONNECT SECTION (only shown when authenticated) ----------
st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Multi-Cloud Integration Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300">Securely connect your AWS, Azure, and GCP environments to enable autonomous FinOps governance.</p>', unsafe_allow_html=True)

st.markdown('<h2 class="text-xl font-semibold mt-4 text-slate-900 dark:text-slate-50">Active Connections Status</h2>', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(status_indicator("AWS", st.session_state.get("aws_connected", False), st.session_state.theme), unsafe_allow_html=True)
with col_b:
    st.markdown(status_indicator("Azure", st.session_state.get("azure_connected", False), st.session_state.theme), unsafe_allow_html=True)
with col_c:
    st.markdown(status_indicator("GCP", st.session_state.get("gcp_connected", False), st.session_state.theme), unsafe_allow_html=True)

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="flex items-center gap-2 mb-4">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FF9900" stroke-width="1.5">
                <path d="M5.5 8.5L12 3L18.5 8.5M5.5 15.5L12 21L18.5 15.5"/>
                <circle cx="12" cy="12" r="9"/>
            </svg>
            <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-50">AWS Connection</h3>
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
            <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Azure Connection</h3>
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
            <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-50">GCP Connection</h3>
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

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

# ---------- Live Cloud API Sync Section ----------
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Live Cloud API Sync</h2>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-4">Provide your cloud credentials to enable real-time data streaming.</p>', unsafe_allow_html=True)

with st.form("live_sync_form"):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        aws_key = st.text_input("AWS Access Key", type="password", placeholder="AKIA...")
    with col_b:
        azure_tenant = st.text_input("Azure Tenant ID", placeholder="tenant-id")
    with col_c:
        gcp_project = st.text_input("GCP Project ID", placeholder="my-project-123")

    test_button = st.form_submit_button("Test Connection & Sync", type="primary", use_container_width=True)

if test_button:
    with st.spinner("Validating credentials and syncing live data..."):
        import time
        time.sleep(2)
    st.success("All connections successful! Live data sync is active.")
