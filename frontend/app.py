import streamlit as st
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu

st.set_page_config(
    page_title="TEJUSKA Cloud Intelligence",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- Inject Tailwind ----------
inject_tailwind()

# ---------- Theme state ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

# ---------- Inject dynamic CSS based on theme ----------
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# ---------- Session state ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.tenant_id = ""

# ---------- Global profile menu ----------
render_profile_menu(st.session_state.theme)

# ---------- Login / Sign Up UI ----------
if not st.session_state.authenticated:
    # Header (custom HTML)
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
        with st.form("signin_form"):
            email = st.text_input("Email *", placeholder="name@company.com")
            password = st.text_input("Password *", type="password", placeholder="········")
            if st.form_submit_button("Sign In", type="primary", use_container_width=True):
                if email and password and "@" in email:
                    st.session_state.authenticated = True
                    st.session_state.tenant_id = email
                    st.rerun()
                else:
                    st.error("Please enter a valid email and password.")

    with tab2:
        with st.form("signup_form"):
            first_name = st.text_input("First Name *", placeholder="John")
            last_name = st.text_input("Last Name *", placeholder="Doe")
            contact = st.text_input("Contact Number *", placeholder="+1234567890")
            email = st.text_input("Email *", placeholder="john.doe@company.com")
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
                    # Simulate successful registration
                    st.success("Account created! Please sign in.")

    # OAuth buttons (side‑by‑side, sleek)
    st.markdown(
        """
        <div class="flex items-center my-6">
            <div class="flex-1 border-t border-slate-300 dark:border-slate-700"></div>
            <span class="px-4 opacity-50 text-slate-700 dark:text-slate-300">OR CONTINUE WITH</span>
            <div class="flex-1 border-t border-slate-300 dark:border-slate-700"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="flex w-full gap-4 mb-5">
            <!-- Google button -->
            <button class="flex-1 flex items-center justify-center gap-2 rounded-lg border border-slate-300 bg-transparent px-4 py-2 font-semibold text-slate-700 transition-all hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800">
                <svg class="h-5 w-5" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Google
            </button>
            <!-- GitHub button -->
            <button class="flex-1 flex items-center justify-center gap-2 rounded-lg border border-slate-300 bg-transparent px-4 py-2 font-semibold text-slate-700 transition-all hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800">
                <svg class="h-5 w-5 fill-current" viewBox="0 0 24 24">
                    <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.03-2.682-.103-.253-.447-1.27.098-2.646 0 0 .84-.269 2.75 1.025.8-.223 1.65-.334 2.5-.334.85 0 1.7.111 2.5.334 1.91-1.294 2.75-1.025 2.75-1.025.545 1.376.201 2.393.099 2.646.64.698 1.03 1.591 1.03 2.682 0 3.841-2.337 4.687-4.565 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
                </svg>
                GitHub
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    # Already authenticated
    st.markdown(
        f'<div class="text-center py-8"><p class="text-xl text-slate-900 dark:text-slate-50">Authenticated as: {st.session_state.tenant_id}</p><p class="opacity-70 text-slate-700 dark:text-slate-300">Expand the sidebar to access the FinOps Dashboard, Automations, AI Assistant, and more.</p></div>',
        unsafe_allow_html=True,
    )
    if st.button("Sign Out", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.tenant_id = ""
        st.rerun()
