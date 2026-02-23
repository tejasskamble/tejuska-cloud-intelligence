import streamlit as st

# 1. Page Configuration (Must be the first command)
st.set_page_config(
    page_title="TEJUSKA Cloud Intelligence",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Enterprise SaaS Custom CSS
st.markdown("""
<style>
    /* Hide default Streamlit branding and buttons */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
   .stDeployButton {display:none;}
    
    /* Center and style the main login block */
   .block-container {
        padding-top: 4rem;
        max-width: 28rem;
    }
    
   .saas-header {
        text-align: center;
        font-family: 'Inter', -apple-system, sans-serif;
        margin-bottom: 2rem;
    }
   .saas-title {
        font-size: 32px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 5px;
    }
   .saas-subtitle {
        font-size: 15px;
        color: #64748b;
        font-weight: 400;
    }
    
    /* Social Login Buttons */
   .social-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 10px;
        margin-bottom: 12px;
        border-radius: 6px;
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s ease;
    }
   .google-btn {
        background-color: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
    }
   .google-btn:hover { background-color: #f8fafc; border-color: #94a3b8; }
    
   .github-btn {
        background-color: #24292e;
        color: #ffffff;
        border: 1px solid #24292e;
    }
   .github-btn:hover { background-color: #1b1f23; }
    
   .social-icon {
        width: 20px;
        height: 20px;
        margin-right: 12px;
    }
   .github-icon { filter: invert(1); }
    
   .divider {
        text-align: center;
        margin: 20px 0;
        color: #94a3b8;
        font-size: 14px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.tenant_id = ""

# 4. Authentication UI
if not st.session_state.authenticated:
    
    # Header
    st.markdown("""
        <div class="saas-header">
            <div class="saas-title">TEJUSKA Cloud</div>
            <div class="saas-subtitle">Enterprise FinOps & Agentic AI Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Custom Google & GitHub Buttons using official logos
    st.markdown("""
        <a href="#" class="social-btn google-btn">
            <img class="social-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/>
            Continue with Google
        </a>
        <a href="#" class="social-btn github-btn">
            <img class="social-icon github-icon" src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg"/>
            Continue with GitHub
        </a>
        <div class="divider">OR SIGN IN WITH EMAIL</div>
    """, unsafe_allow_html=True)
    
    # Secure Email Login Form
    with st.form("login_form"):
        email_input = st.text_input("Work Email", placeholder="name@company.com")
        password_input = st.text_input("Password", type="password", placeholder="••••••••")
        
        submit_button = st.form_submit_button("Sign In to Workspace", type="primary", use_container_width=True)
        
        if submit_button:
            if email_input and "@" in email_input:
                # Login logic
                st.session_state.authenticated = True
                st.session_state.tenant_id = email_input
                st.rerun()
            else:
                st.error("Please enter a valid corporate email address.")

else:
    # 5. Post-Login Screen
    st.success(f"Successfully authenticated as: **{st.session_state.tenant_id}**")
    st.info("Your secure session is active. Please expand the sidebar menu (top left) to access the FinOps Dashboard and AI Assistant.")
    
    if st.button("Sign Out", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.tenant_id = ""
        st.rerun()
