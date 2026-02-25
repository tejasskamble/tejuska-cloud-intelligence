import streamlit as st
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu
from utils.sidebar import render_bottom_profile

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
    # ---------- Bottom profile ----------
    render_bottom_profile()

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
                    st.session_state.role = "Admin"  # Default role
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

    # OAuth buttons (exact HTML)
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

else:
    # Already authenticated
    st.markdown(
        f'<div class="text-center py-8"><p class="text-xl text-slate-900 dark:text-slate-50">Authenticated as: {st.session_state.tenant_id}</p><p class="opacity-70 text-slate-700 dark:text-slate-300">Expand the sidebar to access the FinOps Dashboard, Automations, AI Assistant, and more.</p></div>',
        unsafe_allow_html=True,
    )
    if st.button("Sign Out", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.tenant_id = ""
        st.session_state.role = None
        st.rerun()
