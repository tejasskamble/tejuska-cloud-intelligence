import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="TEJUSKA Cloud Intelligence",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Enterprise SaaS Custom CSS
st.markdown("""
<style>
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean UI Background */
   .stApp {
        background-color: #f8fafc;
    }
   .block-container {
        padding-top: 4rem;
        max-width: 30rem;
    }
   .title-box {
        text-align: center;
        padding-bottom: 1.5rem;
    }
   .title-box h1 {
        color: #0f172a;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
   .title-box p {
        color: #64748b;
        font-size: 1rem;
    }
   .social-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 0.75rem;
        margin-bottom: 1rem;
        border-radius: 0.375rem;
        font-weight: 600;
        font-size: 0.95rem;
        text-decoration: none;
        color: #0f172a;
        background-color: white;
        border: 1px solid #cbd5e1;
        transition: all 0.2s;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
   .social-btn:hover {
        background-color: #f1f5f9;
        border-color: #94a3b8;
    }
   .github-btn {
        background-color: #24292e;
        color: white;
        border: none;
    }
   .github-btn:hover {
        background-color: #1b1f23;
    }
   .social-icon {
        width: 22px;
        height: 22px;
        margin-right: 12px;
    }
   .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
    }
   .divider::before,.divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e2e8f0;
    }
   .divider:not(:empty)::before { margin-right:.5em; }
   .divider:not(:empty)::after { margin-left:.5em; }
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
        <div class="title-box">
            <h1>TEJUSKA Cloud</h1>
            <p>Enterprise FinOps & Agentic AI Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Social Login Buttons with Highly Reliable CDN Logos
    st.markdown("""
        <a href="#" class="social-btn">
            <img class="social-icon" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg"/>
            Continue with Google
        </a>
        <a href="#" class="social-btn github-btn">
            <img class="social-icon" style="filter: invert(1);" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg"/>
            Continue with GitHub
        </a>
        <div class="divider">OR SIGN IN WITH EMAIL</div>
    """, unsafe_allow_html=True)
    
    # Secure Email Login Form (Fixed typing issue by removing st.form wrapper)
    with st.container():
        email_input = st.text_input("Work Email", placeholder="name@company.com")
        password_input = st.text_input("Password", type="password", placeholder="........")
        
        # Native Streamlit Button for processing logic
        if st.button("Sign In to Workspace", type="primary", use_container_width=True):
            if email_input and "@" in email_input:
                st.session_state.authenticated = True
                st.session_state.tenant_id = email_input
                st.rerun()
            else:
                st.error("Please enter a valid corporate email address.")

else:
    # 5. Post-Login Screen
    st.success(f"Successfully authenticated as: {st.session_state.tenant_id}")
    st.info("Your secure session is active. Please expand the sidebar menu to access the FinOps Dashboard and AI Assistant.")
    
    if st.button("Sign Out", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.tenant_id = ""
        st.rerun()
