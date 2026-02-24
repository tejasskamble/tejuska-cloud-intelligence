import streamlit as st
from utils.ui_components import render_profile_menu

st.set_page_config(page_title="Cloud Connect | TEJUSKA", layout="wide")

# ---------- Theme state ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

# ---------- Dynamic CSS ----------
if st.session_state.theme == "dark":
    bg_color = "#0F172A"
    text_color = "#F8FAFC"
    secondary_bg = "#1E293B"
    primary_color = "#818CF8"
    accent_success = "#10B981"
    accent_error = "#EF4444"
    border_color = "#334155"
    card_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.3)"
else:
    bg_color = "#FFFFFF"
    text_color = "#0F172A"
    secondary_bg = "#F1F5F9"
    primary_color = "#6366F1"
    accent_success = "#059669"
    accent_error = "#DC2626"
    border_color = "#E2E8F0"
    card_shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.05)"

st.markdown(f"""
<style>
    /* Copy the full CSS block from app.py (with variables) */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    h1, h2, h3, h4, h5, h6, p, li, .stMarkdown {{ color: {text_color} !important; }}
    h1 {{ background: linear-gradient(135deg, {primary_color} 0%, #A78BFA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
    .stButton button {{ border-radius: 8px; font-weight: 600; transition: all 0.2s ease; border: none; background: linear-gradient(135deg, {primary_color}, #818CF8); color: white; box-shadow: {card_shadow}; }}
    .stButton button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px {primary_color}80; }}
    .stButton button[kind="secondary"] {{ background: transparent; border: 1px solid {primary_color}; color: {primary_color}; box-shadow: none; }}
    .stButton button[kind="secondary"]:hover {{ background: {primary_color}; color: white; }}
    div[data-testid="metric-container"] {{ background: {secondary_bg}; border-radius: 16px; padding: 1.5rem 1rem; box-shadow: {card_shadow}; border: 1px solid {border_color}; transition: all 0.2s; }}
    div[data-testid="metric-container"]:hover {{ box-shadow: 0 20px 25px -5px {primary_color}40; border-color: {primary_color}; }}
    label[data-testid="stMetricLabel"] {{ font-size: 0.9rem; font-weight: 500; color: {text_color} !important; opacity: 0.8; }}
    .stDataFrame {{ border-radius: 12px; overflow: hidden; border: 1px solid {border_color}; }}
    .stDataFrame table {{ font-size: 0.9rem; color: {text_color} !important; }}
    .stDataFrame th {{ background: linear-gradient(135deg, {primary_color}, #A78BFA); color: white; font-weight: 600; padding: 0.75rem !important; }}
    .stDataFrame td {{ padding: 0.6rem !important; border-bottom: 1px solid {border_color}; background: {secondary_bg}; color: {text_color} !important; }}
    .stDataFrame tr:hover td {{ background-color: {primary_color}20; }}
    .status-active, .status-inactive {{ display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }}
    .status-active {{ background: {accent_success}; box-shadow: 0 0 0 2px {accent_success}40; }}
    .status-inactive {{ background: {accent_error}; box-shadow: 0 0 0 2px {accent_error}40; }}
    .pricing-card {{ background: {secondary_bg}; border-radius: 24px; padding: 2rem 1.5rem; border: 1px solid {border_color}; transition: transform 0.2s, border-color 0.2s; }}
    .pricing-card:hover {{ transform: scale(1.02); border-color: {primary_color}; }}
    .pricing-card h4 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: {primary_color}; }}
    .pricing-card ul {{ list-style-type: none; padding-left: 0; color: {text_color}; }}
    .pricing-card li {{ margin-bottom: 0.5rem; }}
    .provider-icon {{ width: 24px; height: 24px; vertical-align: middle; margin-right: 8px; display: inline-block; }}
    .social-icon {{ width: 22px; height: 22px; margin-right: 12px; vertical-align: middle; }}
    .github-icon {{ fill: {text_color}; }}
    .divider {{ display: flex; align-items: center; text-align: center; margin: 1.5rem 0; color: {text_color}; opacity: 0.5; }}
    .divider::before, .divider::after {{ content: ''; flex: 1; border-bottom: 1px solid {border_color}; }}
    .divider:not(:empty)::before {{ margin-right: .5em; }}
    .divider:not(:empty)::after {{ margin-left: .5em; }}
    .stTextInput input, .stTextInput textarea {{ border-radius: 8px; border: 1px solid {border_color}; background: {secondary_bg}; color: {text_color}; }}
    .stTextInput input:focus {{ border-color: {primary_color}; box-shadow: 0 0 0 2px {primary_color}40; }}
    .css-1d391kg, .css-1wrcr25 {{ background-color: {secondary_bg}; }}
</style>
""", unsafe_allow_html=True)

# ---------- Global profile menu ----------
render_profile_menu()

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown("## Multi-Cloud Integration Hub")
st.markdown("Securely connect your AWS, Azure, and GCP environments to enable autonomous FinOps governance.")
st.divider()

st.markdown("### Active Connections Status")
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.session_state.get("aws_connected"):
        st.markdown('<div><span class="status-active"></span> AWS: Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div><span class="status-inactive"></span> AWS: Disconnected</div>', unsafe_allow_html=True)
with col_b:
    if st.session_state.get("azure_connected"):
        st.markdown('<div><span class="status-active"></span> Azure: Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div><span class="status-inactive"></span> Azure: Disconnected</div>', unsafe_allow_html=True)
with col_c:
    if st.session_state.get("gcp_connected"):
        st.markdown('<div><span class="status-active"></span> GCP: Active</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div><span class="status-inactive"></span> GCP: Disconnected</div>', unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FF9900" stroke-width="1.5">
                <path d="M5.5 8.5L12 3L18.5 8.5M5.5 15.5L12 21L18.5 15.5"/>
                <circle cx="12" cy="12" r="9"/>
            </svg>
            <h4 style="margin: 0;">AWS Connection</h4>
        </div>
    """, unsafe_allow_html=True)
    with st.form("aws_connect_form"):
        aws_access_key = st.text_input("Access Key ID", type="password")
        aws_secret_key = st.text_input("Secret Access Key", type="password")
        aws_region = st.selectbox("Region", ["ap-south-1 (Mumbai)", "us-east-1 (N. Virginia)"])
        submit_aws = st.form_submit_button("Connect AWS", type="primary", use_container_width=True)
        if submit_aws and aws_access_key:
            st.session_state["aws_connected"] = True
            st.rerun()

with col2:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0078D4" stroke-width="1.5">
                <rect x="4" y="4" width="16" height="16" rx="2"/>
                <path d="M8 8h8v8H8z"/>
            </svg>
            <h4 style="margin: 0;">Azure Connection</h4>
        </div>
    """, unsafe_allow_html=True)
    with st.form("azure_connect_form"):
        tenant_id = st.text_input("Tenant ID", type="password")
        client_id = st.text_input("Client ID", type="password")
        client_secret = st.text_input("Client Secret", type="password")
        submit_azure = st.form_submit_button("Connect Azure", type="primary", use_container_width=True)
        if submit_azure and tenant_id:
            st.session_state["azure_connected"] = True
            st.rerun()

with col3:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                <circle cx="7" cy="12" r="3" fill="#EA4335"/>
                <circle cx="12" cy="17" r="3" fill="#34A853"/>
                <circle cx="17" cy="12" r="3" fill="#4285F4"/>
                <circle cx="12" cy="7" r="3" fill="#FBBC05"/>
            </svg>
            <h4 style="margin: 0;">GCP Connection</h4>
        </div>
    """, unsafe_allow_html=True)
    with st.form("gcp_connect_form"):
        gcp_project = st.text_input("Project ID")
        gcp_json = st.file_uploader("Upload Service Account JSON", type=["json"])
        submit_gcp = st.form_submit_button("Connect GCP", type="primary", use_container_width=True)
        if submit_gcp and gcp_project:
            st.session_state["gcp_connected"] = True
            st.rerun()
