"""
4_Upgrade_Plan.py
=================
TEJUSKA Cloud Intelligence
Plan Upgrade Page - Stripe/Razorpay payment integration.
"""

import streamlit as st
import requests

st.set_page_config(
    page_title="Upgrade Plan | TEJUSKA",
    layout="wide",
)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

BACKEND_URL: str = st.secrets.get("BACKEND_URL", "http://localhost:7860")
TENANT_ID: str   = st.session_state.get("tenant_id", "")

st.markdown("# Upgrade Your Plan")
st.markdown(
    "Unlock the full power of TEJUSKA Cloud Intelligence. "
    "All plans include a 14-day free trial. No credit card required for the Free tier."
)
st.divider()

# ---------------------------------------------------------------------------
# Pricing tiers
# ---------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Free")
    st.markdown("**$0 / month**")
    st.markdown(
        "- 1 cloud account connected\n"
        "- 30-day billing history\n"
        "- OPTIC AI queries: 10 per day\n"
        "- Email support"
    )
    st.button("Current Plan", disabled=True, key="free_btn")

with col2:
    st.markdown("#### Pro")
    st.markdown("**$99 / month**")
    st.markdown(
        "- Up to 10 cloud accounts\n"
        "- 12-month billing history\n"
        "- Unlimited OPTIC AI queries\n"
        "- ABACUS automations\n"
        "- Slack and Email alerts\n"
        "- Priority support"
    )
    if st.button("Upgrade to Pro", key="pro_btn"):
        st.info(
            "Stripe Checkout integration: configure STRIPE_SECRET_KEY in backend secrets "
            "and create a Price object in your Stripe Dashboard, then link the checkout URL here."
        )

with col3:
    st.markdown("#### Enterprise")
    st.markdown("**Custom Pricing**")
    st.markdown(
        "- Unlimited cloud accounts\n"
        "- Unlimited history\n"
        "- Custom GNN model training\n"
        "- Dedicated infrastructure\n"
        "- SLA guarantee\n"
        "- Dedicated customer success manager"
    )
    if st.button("Contact Sales", key="enterprise_btn"):
        st.info("Email: sales@tejuska.io")

st.divider()
st.markdown(
    "**Payment processing** is handled securely by Stripe (global) and "
    "Razorpay (India). TEJUSKA does not store card details."
)
