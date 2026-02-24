import streamlit as st
from utils.ui_components import render_profile_menu

st.set_page_config(
    page_title="TEJUSKA Cloud Intelligence",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- Theme state ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # default

# Theme toggle in sidebar (sidebar is collapsed but can be expanded)
with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

# ---------- Dynamic CSS based on theme ----------
if st.session_state.theme == "dark":
    bg_color = "#0F172A"               # deep dark
    text_color = "#F8FAFC"              # bright white
    secondary_bg = "#1E293B"            # dark card background
    primary_color = "#818CF8"           # indigo accent
    accent_success = "#10B981"
    accent_error = "#EF4444"
    border_color = "#334155"
    card_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.3)"
else:
    bg_color = "#FFFFFF"                # crisp white
    text_color = "#0F172A"               # deep dark
    secondary_bg = "#F1F5F9"             # light gray for cards
    primary_color = "#6366F1"
    accent_success = "#059669"
    accent_error = "#DC2626"
    border_color = "#E2E8F0"
    card_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.05)"

st.markdown(f"""
<style>
    /* Hide Streamlit branding */
    #MainMenu, footer, header {{visibility: hidden;}}

    /* Use theme variables */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6, p, li, .stMarkdown {{
        color: {text_color} !important;
    }}
    h1 {{
        background: linear-gradient(135deg, {primary_color} 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    /* Buttons */
    .stButton button {{
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
        border: none;
        background: linear-gradient(135deg, {primary_color}, #818CF8);
        color: white;
        box-shadow: {card_shadow};
    }}
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px {primary_color}80;
    }}
    .stButton button[kind="secondary"] {{
        background: transparent;
        border: 1px solid {primary_color};
        color: {primary_color};
        box-shadow: none;
    }}
    .stButton button[kind="secondary"]:hover {{
        background: {primary_color};
        color: white;
    }}

    /* Metric cards */
    div[data-testid="metric-container"] {{
        background: {secondary_bg};
        border-radius: 16px;
        padding: 1.5rem 1rem;
        box-shadow: {card_shadow};
        border: 1px solid {border_color};
        transition: all 0.2s;
    }}
    div[data-testid="metric-container"]:hover {{
        box-shadow: 0 20px 25px -5px {primary_color}40;
        border-color: {primary_color};
    }}
    label[data-testid="stMetricLabel"] {{
        font-size: 0.9rem;
        font-weight: 500;
        color: {text_color} !important;
        opacity: 0.8;
    }}

    /* DataFrames */
    .stDataFrame {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {border_color};
    }}
    .stDataFrame table {{
        font-size: 0.9rem;
        color: {text_color} !important;
    }}
    .stDataFrame th {{
        background: linear-gradient(135deg, {primary_color}, #A78BFA);
        color: white;
        font-weight: 600;
        padding: 0.75rem !important;
    }}
    .stDataFrame td {{
        padding: 0.6rem !important;
        border-bottom: 1px solid {border_color};
        background: {secondary_bg};
        color: {text_color} !important;
    }}
    .stDataFrame tr:hover td {{
        background-color: {primary_color}20;
    }}

    /* Status indicators */
    .status-active, .status-inactive {{
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    .status-active {{
        background: {accent_success};
        box-shadow: 0 0 0 2px {accent_success}40;
    }}
    .status-inactive {{
        background: {accent_error};
        box-shadow: 0 0 0 2px {accent_error}40;
    }}

    /* Pricing cards */
    .pricing-card {{
        background: {secondary_bg};
        border-radius: 24px;
        padding: 2rem 1.5rem;
        border: 1px solid {border_color};
        transition: transform 0.2s, border-color 0.2s;
    }}
    .pricing-card:hover {{
        transform: scale(1.02);
        border-color: {primary_color};
    }}
    .pricing-card h4 {{
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: {primary_color};
    }}
    .pricing-card ul {{
        list-style-type: none;
        padding-left: 0;
        color: {text_color};
    }}
    .pricing-card li {{
        margin-bottom: 0.5rem;
    }}

    /* Icons */
    .provider-icon {{
        width: 24px;
        height: 24px;
        vertical-align: middle;
        margin-right: 8px;
        display: inline-block;
    }}
    .social-icon {{
        width: 22px;
        height: 22px;
        margin-right: 12px;
        vertical-align: middle;
    }}
    /* GitHub icon fill adapts to theme */
    .github-icon {{
        fill: {text_color};
    }}

    /* Divider */
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: {text_color};
        opacity: 0.5;
    }}
    .divider::before, .divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid {border_color};
    }}
    .divider:not(:empty)::before {{ margin-right: .5em; }}
    .divider:not(:empty)::after {{ margin-left: .5em; }}

    /* Input fields */
    .stTextInput input, .stTextInput textarea {{
        border-radius: 8px;
        border: 1px solid {border_color};
        background: {secondary_bg};
        color: {text_color};
    }}
    .stTextInput input:focus {{
        border-color: {primary_color};
        box-shadow: 0 0 0 2px {primary_color}40;
    }}

    /* Sidebar */
    .css-1d391kg, .css-1wrcr25 {{
        background-color: {secondary_bg};
    }}
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.tenant_id = ""

# ---------- Global profile menu (only if authenticated) ----------
render_profile_menu()

# ---------- Login UI ----------
if not st.session_state.authenticated:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 2rem;">
            <h1>TEJUSKA Cloud</h1>
            <p style="opacity: 0.7;">Enterprise FinOps & Agentic AI Platform</p>
        </div>
    """, unsafe_allow_html=True)

    # Social login buttons with inline SVGs
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <a href="#" style="display: flex; align-items: center; justify-content: center; padding: 0.75rem; border-radius: 8px; background: white; border: 1px solid #cbd5e1; color: #0f172a; text-decoration: none; font-weight: 600; transition: all 0.2s;">
                <svg class="social-icon" viewBox="0 0 24 24" width="22" height="22">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
            </a>
            <a href="#" style="display: flex; align-items: center; justify-content: center; padding: 0.75rem; border-radius: 8px; background: #24292e; color: white; text-decoration: none; font-weight: 600; transition: all 0.2s;">
                <svg class="social-icon github-icon" viewBox="0 0 24 24" width="22" height="22" fill="white">
                    <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.03-2.682-.103-.253-.447-1.27.098-2.646 0 0 .84-.269 2.75 1.025.8-.223 1.65-.334 2.5-.334.85 0 1.7.111 2.5.334 1.91-1.294 2.75-1.025 2.75-1.025.545 1.376.201 2.393.099 2.646.64.698 1.03 1.591 1.03 2.682 0 3.841-2.337 4.687-4.565 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
                </svg>
                Continue with GitHub
            </a>
        </div>
        <div class="divider">OR SIGN IN WITH EMAIL</div>
    """, unsafe_allow_html=True)

    with st.container():
        email = st.text_input("Work Email", placeholder="name@company.com")
        password = st.text_input("Password", type="password", placeholder="········")
        if st.button("Sign In to Workspace", type="primary", use_container_width=True):
            if email and "@" in email:
                st.session_state.authenticated = True
                st.session_state.tenant_id = email
                st.rerun()
            else:
                st.error("Please enter a valid corporate email address.")
else:
    st.success(f"Authenticated as: {st.session_state.tenant_id}")
    st.info("Expand the sidebar to access the FinOps Dashboard, Automations, AI Assistant, and more.")
    if st.button("Sign Out", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.tenant_id = ""
        st.rerun()
