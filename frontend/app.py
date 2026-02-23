import streamlit as st
from supabase import create_client, Client

# 1. Page Configuration
st.set_page_config(
    page_title="TEJUSKA Cloud Intelligence",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Connect to REAL Supabase Database (FOUNDER'S FIX)
@st.cache_resource
def init_supabase() -> Client:
    try:
        # Fetching the exact string values from the [api] dictionary block
        url = st.secrets["api"]
        key = st.secrets["api"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Critical Error: Supabase connection failed. Details: {e}")
        st.stop()

supabase = init_supabase()

# 3. Enterprise SaaS Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
 .stApp { background-color: #f8fafc; }
 .block-container { padding-top: 4rem; max-width: 30rem; }
 .title-box { text-align: center; padding-bottom: 1.5rem; }
 .title-box h1 { color: #0f172a; font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem; }
 .title-box p { color: #64748b; font-size: 1rem; }
 .social-btn {
        display: flex; align-items: center; justify-content: center;
        width: 100%; padding: 0.75rem; margin-bottom: 1rem;
        border-radius: 0.375rem; font-weight: 600; font-size: 0.95rem;
        text-decoration: none; color: #0f172a; background-color: white;
        border: 1px solid #cbd5e1; transition: all 0.2s;
    }
 .social-btn:hover { background-color: #f1f5f9; border-color: #94a3b8; }
 .github-btn { background-color: #24292e; color: white; border: none; }
 .github-btn:hover { background-color: #1b1f23; }
 .social-icon { width: 22px; height: 22px; margin-right: 12px; }
 .divider {
        display: flex; align-items: center; text-align: center;
        margin: 1.5rem 0; color: #94a3b8; font-size: 0.85rem; font-weight: 500;
    }
 .divider::before,.divider::after { content: ''; flex: 1; border-bottom: 1px solid #e2e8f0; }
 .divider:not(:empty)::before { margin-right:.5em; }
 .divider:not(:empty)::after { margin-left:.5em; }
</style>
""", unsafe_allow_html=True)

# 4. Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.tenant_id = ""

# 5. REAL Authentication UI
if not st.session_state.authenticated:
    st.markdown("""
        <div class="title-box">
            <h1>TEJUSKA Cloud</h1>
            <p>Enterprise FinOps & Agentic AI Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <a href="#" class="social-btn">
            <img class="social-icon" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg"/>
            Continue with Google (Setup Required)
        </a>
        <a href="#" class="social-btn github-btn">
            <img class="social-icon" style="filter: invert(1);" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg"/>
            Continue with GitHub (Setup Required)
        </a>
        <div class="divider">OR SECURE EMAIL LOGIN</div>
    """, unsafe_allow_html=True)
    
    with st.container():
        email_input = st.text_input("Work Email", placeholder="name@company.com")
        password_input = st.text_input("Password", type="password", placeholder="Min 6 characters")
        
        if st.button("Sign In / Create Account", type="primary", use_container_width=True):
            if email_input and len(password_input) >= 6:
                try:
                    response = supabase.auth.sign_in_with_password({"email": email_input, "password": password_input})
                    st.session_state.authenticated = True
                    st.session_state.tenant_id = response.user.email
                    st.rerun()
                except Exception as e:
                    error_msg = str(e)
                    if "Invalid login credentials" in error_msg:
                        try:
                            res = supabase.auth.sign_up({"email": email_input, "password": password_input})
                            st.success("New secure account created! Please click the button again to login.")
                        except Exception as ex:
                            st.error(f"Registration failed: {ex}")
                    else:
                        st.error(f"Authentication Error: {error_msg}")
            else:
                st.error("Please enter a valid email and a password of at least 6 characters.")

else:
    # 6. Post-Login Screen
    st.success(f"Secure session active for: {st.session_state.tenant_id}")
    st.info("Navigation unlocked. Use the sidebar menu to access your FinOps Dashboards.")
    
    if st.button("Secure Sign Out", type="secondary"):
        supabase.auth.sign_out()
        st.session_state.authenticated = False
        st.session_state.tenant_id = ""
        st.rerun()
