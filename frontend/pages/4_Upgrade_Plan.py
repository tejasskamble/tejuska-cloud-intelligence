import streamlit as st
from utils.ui_components import inject_tailwind, render_profile_menu, pricing_card

st.set_page_config(
    page_title="Upgrade Plan | TEJUSKA",
    layout="wide",
)

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

bg_class = "bg-slate-50" if st.session_state.theme == "light" else "bg-slate-900"
text_class = "text-slate-900" if st.session_state.theme == "light" else "text-slate-50"

st.markdown(f'<div class="{bg_class} min-h-screen {text_class} p-6">', unsafe_allow_html=True)

render_profile_menu(st.session_state.theme)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold">Upgrade Your Plan</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70">Unlock the full power of TEJUSKA Cloud Intelligence. All plans include a 14-day free trial. No credit card required for the Free tier.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(pricing_card("Free", "$0 / month", ["1 cloud account connected", "30-day billing history", "OPTIC AI queries: 10 per day", "Email support"], st.session_state.theme), unsafe_allow_html=True)
    st.button("Current Plan", disabled=True, key="free_btn", use_container_width=True)

with col2:
    st.markdown(pricing_card("Pro", "$99 / month", ["Up to 10 cloud accounts", "12-month billing history", "Unlimited OPTIC AI queries", "ABACUS automations", "Slack and Email alerts", "Priority support"], st.session_state.theme), unsafe_allow_html=True)
    if st.button("Upgrade to Pro", key="pro_btn", use_container_width=True):
        st.info("Stripe Checkout integration: configure STRIPE_SECRET_KEY in backend secrets and create a Price object in your Stripe Dashboard, then link the checkout URL here.")

with col3:
    st.markdown(pricing_card("Enterprise", "Custom Pricing", ["Unlimited cloud accounts", "Unlimited history", "Custom GNN model training", "Dedicated infrastructure", "SLA guarantee", "Dedicated customer success manager"], st.session_state.theme), unsafe_allow_html=True)
    if st.button("Contact Sales", key="enterprise_btn", use_container_width=True):
        st.info("Email: sales@tejuska.io")

st.markdown('<hr class="my-6 border-slate-300">', unsafe_allow_html=True)
st.markdown('<p class="text-sm opacity-70">**Payment processing** is handled securely by Stripe (global) and Razorpay (India). TEJUSKA does not store card details.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
