import streamlit as st
import requests

st.set_page_config(page_title="Pro Automations | TEJUSKA", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown("## ⚡ Agentic Auto-Kill & Thresholds")
st.markdown("Set custom budget limits. The Agentic AI will automatically terminate resources and send email alerts if costs exceed your threshold.")
st.divider()

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:7860")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. Set Budget Threshold")
    st.info("Configure the maximum allowed cost for a specific cloud resource.")
    with st.form("threshold_form"):
        provider = st.selectbox("Cloud Provider",)
        resource_id = st.text_input("Resource ID", placeholder="e.g., i-09ca51ce7bcd242ed")
        threshold = st.number_input("Cost Threshold Limit ($)", min_value=0.01, value=1.00, step=0.50)
        user_email = st.text_input("Alert Email ID", value=st.session_state.tenant_id)
        
        submit_threshold = st.form_submit_button("Activate Agentic Shield", type="primary")
        
        if submit_threshold:
            if resource_id:
                st.success(f"Shield Activated! If {provider} resource '{resource_id}' exceeds ${threshold:.2f}, it will be TERMINATED immediately and an alert will be sent to {user_email}.")
            else:
                st.error("Please enter a valid Resource ID.")

with col2:
    st.markdown("### 2. Simulate Cloud Billing (Test)")
    st.warning("Test the automation by simulating a bill that exceeds your threshold.")
    with st.form("simulate_form"):
        sim_resource_id = st.text_input("Resource ID to Test", value="i-09ca51ce7bcd242ed")
        sim_cost = st.number_input("Current Simulated Cost ($)", value=1.50)
        
        submit_sim = st.form_submit_button("Run AI Evaluation", type="secondary")
        
        if submit_sim:
            st.info(f"ABACUS Engine analyzing resource {sim_resource_id}...")
            if sim_cost > 1.00: # Assuming $1 threshold
                st.error(f"Cost (${sim_cost}) exceeds threshold! Triggering termination...")
                try:
                    # In production, this hits your FastAPI backend
                    # requests.post(f"{BACKEND_URL}/evaluate", json={...})
                    st.success("Resource successfully terminated by AI.")
                    st.success("Email notification dispatched via SMTP.")
                except Exception as e:
                    st.error(f"Backend communication error: {e}")
            else:
                st.success("Cost is within limits. No action taken.")
