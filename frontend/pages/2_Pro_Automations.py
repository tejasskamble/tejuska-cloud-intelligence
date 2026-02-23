"""
2_Pro_Automations.py
====================
TEJUSKA Cloud Intelligence
Pro Automations - Trigger ABACUS AI for autonomous resource optimisation.
Available on Pro and Enterprise plans.
"""

import streamlit as st
import requests

st.set_page_config(
    page_title="Pro Automations | TEJUSKA",
    layout="wide",
)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

BACKEND_URL: str = st.secrets.get("BACKEND_URL", "http://localhost:7860")
TENANT_ID: str   = st.session_state.get("tenant_id", "")

st.markdown("# Pro Automations")
st.markdown(
    "Use the ABACUS engine to evaluate cloud resources and trigger "
    "autonomous right-sizing or termination actions."
)
st.divider()

# ---------------------------------------------------------------------------
# Auto-termination panel
# ---------------------------------------------------------------------------
st.markdown("### Resource Evaluation")
with st.form("auto_terminate_form"):
    resource_id = st.text_input(
        "Cloud Resource ID",
        placeholder="e.g. i-0abc123def456 or projects/my-proj/instances/vm-001",
    )
    dry_run = st.checkbox("Dry Run (simulate without executing)", value=True)
    submitted = st.form_submit_button("Evaluate Resource")

if submitted:
    if not resource_id.strip():
        st.error("Resource ID must not be empty.")
    else:
        with st.spinner("Sending evaluation request to ABACUS engine..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/v1/auto-terminate",
                    json={
                        "tenant_id":   TENANT_ID,
                        "resource_id": resource_id.strip(),
                        "dry_run":     dry_run,
                    },
                    timeout=30,
                )
                if response.status_code == 202:
                    st.success(
                        "Evaluation scheduled. The ABACUS engine is processing the request. "
                        "Results will appear in the audit log below."
                    )
                else:
                    st.error(f"Backend returned HTTP {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend. Verify BACKEND_URL in secrets.")

st.divider()

# ---------------------------------------------------------------------------
# Saved automation rules (static for now)
# ---------------------------------------------------------------------------
st.markdown("### Active Automation Rules")
st.info(
    "Define budget policies in the Enterprise plan to enable ABACUS to act "
    "autonomously without manual triggers."
)

import pandas as pd
rules_df = pd.DataFrame({
    "Rule Name":          ["Terminate idle EC2 > 30 days", "Rightsize GCP VMs < 5% CPU"],
    "Provider":           ["AWS", "GCP"],
    "Condition":          ["CPU < 2% for 30 days", "CPU avg < 5% over 7 days"],
    "Action":             ["Terminate", "Downsize"],
    "Status":             ["Active", "Active"],
})
st.dataframe(rules_df, use_container_width=True, hide_index=True)
