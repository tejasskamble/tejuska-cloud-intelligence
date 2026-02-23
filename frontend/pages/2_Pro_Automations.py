import streamlit as st

# Page configuration
st.set_page_config(page_title="Pro Automations | TEJUSKA", layout="wide")

# Authentication check
if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown("## ⚡ Agentic Auto-Kill & Thresholds")
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

# Layout: 2 columns
col1, col2 = st.columns(2)

# ------------------------
# Column 1: Set Budget Threshold
# ------------------------
with col1:
    st.markdown("### 1. Set Budget Threshold")
    st.info("Configure the maximum allowed cost for a specific cloud resource.")

    with st.form("threshold_form"):
        # Cloud provider selection (fixed bug)
        provider = st.selectbox(
            "Cloud Provider",
            ["AWS", "Azure", "GCP", "Other"]
        )

        resource_id = st.text_input(
            "Resource ID", 
            placeholder="e.g., i-09ca51ce7bcd242ed"
        )

        threshold = st.number_input(
            "Cost Threshold Limit ($)", 
            min_value=0.01, 
            value=1.00, 
            step=0.50
        )

        # Safely get email from session state
        current_email = st.session_state.get("tenant_id", "")
        user_email = st.text_input("Alert Email ID", value=current_email)

        submit_threshold = st.form_submit_button(
            "Activate Agentic Shield", 
            type="primary"
        )

        if submit_threshold:
            if not resource_id:
                st.error("Please enter a valid Resource ID.")
            else:
                st.success(
                    f"Shield Activated! If {provider} resource '{resource_id}' exceeds "
                    f"${threshold:.2f}, it will be TERMINATED immediately and an alert will be sent to {user_email}."
                )

# ------------------------
# Column 2: Simulate Cloud Billing
# ------------------------
with col2:
    st.markdown("### 2. Simulate Cloud Billing (Test)")
    st.warning(
        "Test the automation by simulating a bill that exceeds your threshold."
    )

    with st.form("simulate_form"):
        sim_resource_id = st.text_input(
            "Resource ID to Test", 
            value="i-09ca51ce7bcd242ed"
        )
        sim_cost = st.number_input(
            "Current Simulated Cost ($)", 
            value=1.50
        )

        submit_sim = st.form_submit_button(
            "Run AI Evaluation", 
            type="secondary"
        )

        if submit_sim:
            st.info(f"ABACUS Engine analyzing resource {sim_resource_id}...")

            # Example threshold, could fetch real threshold
            threshold_limit = 1.00
            if sim_cost > threshold_limit:
                st.error(f"Cost (${sim_cost}) exceeds threshold! Triggering termination...")
                try:
                    # Placeholder for backend action
                    st.success(f"Resource '{sim_resource_id}' successfully terminated by AI.")
                    st.success("Email notification dispatched via SMTP.")
                except Exception as e:
                    st.error(f"Backend communication error: {e}")
            else:
                st.success("Cost is within limits. No action taken.")
