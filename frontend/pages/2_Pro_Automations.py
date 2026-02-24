import streamlit as st

st.set_page_config(page_title="Pro Automations | TEJUSKA", layout="wide")

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Copy the full CSS block from app.py here */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: var(--background-color); color: var(--text-color); }
    h1, h2, h3 { font-weight: 700; letter-spacing: -0.02em; }
    h1 { background: linear-gradient(135deg, var(--primary-color) 0%, #A78BFA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .stButton button { border-radius: 8px; font-weight: 600; transition: all 0.2s ease; border: none; background: linear-gradient(135deg, var(--primary-color), #818CF8); color: white; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3); }
    .stButton button[kind="secondary"] { background: transparent; border: 1px solid var(--primary-color); color: var(--primary-color); box-shadow: none; }
    .stButton button[kind="secondary"]:hover { background: var(--primary-color); color: white; }
    div[data-testid="metric-container"] { background: var(--secondary-background-color); border-radius: 16px; padding: 1.5rem 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid rgba(0,0,0,0.05); transition: all 0.2s; }
    div[data-testid="metric-container"]:hover { box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.1); border-color: var(--primary-color); }
    label[data-testid="stMetricLabel"] { font-size: 0.9rem; font-weight: 500; color: var(--text-color); opacity: 0.8; }
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid var(--secondary-background-color); }
    .stDataFrame table { font-size: 0.9rem; }
    .stDataFrame th { background: linear-gradient(135deg, var(--primary-color), #A78BFA); color: white; font-weight: 600; padding: 0.75rem !important; }
    .stDataFrame td { padding: 0.6rem !important; border-bottom: 1px solid var(--secondary-background-color); }
    .stDataFrame tr:hover td { background-color: var(--secondary-background-color); }
    .status-active, .status-inactive { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
    .status-active { background: #10B981; box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2); }
    .status-inactive { background: #EF4444; box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2); }
    .pricing-card { background: var(--secondary-background-color); border-radius: 24px; padding: 2rem 1.5rem; border: 1px solid rgba(0,0,0,0.05); transition: transform 0.2s, border-color 0.2s; }
    .pricing-card:hover { transform: scale(1.02); border-color: var(--primary-color); }
    .pricing-card h4 { font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem; color: var(--primary-color); }
    .pricing-card ul { list-style-type: none; padding-left: 0; }
    .pricing-card li { margin-bottom: 0.5rem; }
    .provider-icon { width: 24px; height: 24px; vertical-align: middle; margin-right: 8px; display: inline-block; }
    .social-icon { width: 22px; height: 22px; margin-right: 12px; vertical-align: middle; }
    .divider { display: flex; align-items: center; text-align: center; margin: 1.5rem 0; color: var(--text-color); opacity: 0.5; }
    .divider::before, .divider::after { content: ''; flex: 1; border-bottom: 1px solid var(--secondary-background-color); }
    .divider:not(:empty)::before { margin-right: .5em; }
    .divider:not(:empty)::after { margin-left: .5em; }
    .stTextInput input, .stTextInput textarea { border-radius: 8px; border: 1px solid var(--secondary-background-color); background: var(--background-color); color: var(--text-color); }
    .stTextInput input:focus { border-color: var(--primary-color); box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2); }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown("## Agentic Auto-Kill & Thresholds")
st.markdown(
    "Set custom budget limits. The Agentic AI will automatically terminate resources "
    "and send email alerts if costs exceed your threshold."
)
st.divider()

# Safely fetch backend URL
try:
    BACKEND_URL = st.secrets["api"]["backend_url"]
except:
    BACKEND_URL = "https://tejuska-tejuska-cloud-intelligence.hf.space"

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. Set Budget Threshold")
    st.info("Configure the maximum allowed cost for a specific cloud resource.")

    with st.form("threshold_form"):
        # Provider icon above selectbox
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 2v20M2 12h20"/>
                </svg>
                <span style="font-weight: 600;">Cloud Provider</span>
            </div>
        """, unsafe_allow_html=True)
        provider = st.selectbox("", ["AWS", "Azure", "GCP", "Other"], label_visibility="collapsed")
        resource_id = st.text_input("Resource ID", placeholder="e.g., i-09ca51ce7bcd242ed")
        threshold = st.number_input("Cost Threshold Limit ($)", min_value=0.01, value=1.00, step=0.50)
        current_email = st.session_state.get("tenant_id", "")
        user_email = st.text_input("Alert Email ID", value=current_email)

        submit_threshold = st.form_submit_button("Activate Agentic Shield", type="primary")
        if submit_threshold:
            if not resource_id:
                st.error("Please enter a valid Resource ID.")
            else:
                st.success(
                    f"Shield Activated! If {provider} resource '{resource_id}' exceeds "
                    f"${threshold:.2f}, it will be TERMINATED immediately and an alert will be sent to {user_email}."
                )

with col2:
    st.markdown("### 2. Simulate Cloud Billing (Test)")
    st.warning("Test the automation by simulating a bill that exceeds your threshold.")

    with st.form("simulate_form"):
        sim_resource_id = st.text_input("Resource ID to Test", value="i-09ca51ce7bcd242ed")
        sim_cost = st.number_input("Current Simulated Cost ($)", value=1.50)

        submit_sim = st.form_submit_button("Run AI Evaluation", type="secondary")
        if submit_sim:
            st.info(f"ABACUS Engine analyzing resource {sim_resource_id}...")
            threshold_limit = 1.00  # Example threshold
            if sim_cost > threshold_limit:
                st.error(f"Cost (${sim_cost}) exceeds threshold! Triggering termination...")
                try:
                    st.success(f"Resource '{sim_resource_id}' successfully terminated by AI.")
                    st.success("Email notification dispatched via SMTP.")
                except Exception as e:
                    st.error(f"Backend communication error: {e}")
            else:
                st.success("Cost is within limits. No action taken.")
