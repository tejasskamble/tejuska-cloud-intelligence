import streamlit as st
import time
import random

st.set_page_config(page_title="AI Assistant | TEJUSKA", layout="wide")

# ---------- Theme state ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

# ---------- Dynamic CSS ----------
if st.session_state.theme == "dark":
    bg_color = "#0B1120"
    text_color = "#F1F5F9"
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
    /* Copy the full CSS block from app.py here (with variables) */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    h1, h2, h3 {{ font-weight: 700; letter-spacing: -0.02em; }}
    h1 {{ background: linear-gradient(135deg, {primary_color} 0%, #A78BFA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
    .stButton button {{ border-radius: 8px; font-weight: 600; transition: all 0.2s ease; border: none; background: linear-gradient(135deg, {primary_color}, #818CF8); color: white; box-shadow: {card_shadow}; }}
    .stButton button:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px {primary_color}80; }}
    .stButton button[kind="secondary"] {{ background: transparent; border: 1px solid {primary_color}; color: {primary_color}; box-shadow: none; }}
    .stButton button[kind="secondary"]:hover {{ background: {primary_color}; color: white; }}
    div[data-testid="metric-container"] {{ background: {secondary_bg}; border-radius: 16px; padding: 1.5rem 1rem; box-shadow: {card_shadow}; border: 1px solid {border_color}; transition: all 0.2s; }}
    div[data-testid="metric-container"]:hover {{ box-shadow: 0 20px 25px -5px {primary_color}40; border-color: {primary_color}; }}
    label[data-testid="stMetricLabel"] {{ font-size: 0.9rem; font-weight: 500; color: {text_color}; opacity: 0.8; }}
    .stDataFrame {{ border-radius: 12px; overflow: hidden; border: 1px solid {border_color}; }}
    .stDataFrame table {{ font-size: 0.9rem; color: {text_color}; }}
    .stDataFrame th {{ background: linear-gradient(135deg, {primary_color}, #A78BFA); color: white; font-weight: 600; padding: 0.75rem !important; }}
    .stDataFrame td {{ padding: 0.6rem !important; border-bottom: 1px solid {border_color}; background: {secondary_bg}; }}
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

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown("## OPTIC FinOps AI Assistant – Gemini Ultra Mode")
st.markdown(
    "Chat freely with your multi-cloud FinOps assistant. "
    "Ask anything, and it will respond like a full AI expert, maintaining context and giving advice."
)
st.divider()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "thresholds" not in st.session_state:
    st.session_state.thresholds = {}

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Agentic Budget Thresholds")
    with st.form("threshold_form"):
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
        threshold = st.number_input("Cost Threshold ($)", min_value=0.01, value=1.0, step=0.5)
        user_email = st.text_input("Alert Email", value=st.session_state.get("tenant_id", ""))

        submit_threshold = st.form_submit_button("Activate Agentic Shield", type="primary")
        if submit_threshold:
            if resource_id:
                st.session_state.thresholds[resource_id] = {
                    "provider": provider,
                    "limit": threshold,
                    "email": user_email
                }
                st.success(
                    f"Shield Activated! {provider} resource '{resource_id}' "
                    f"will be monitored and alerts sent to {user_email} if cost exceeds ${threshold:.2f}."
                )
            else:
                st.error("Enter a valid Resource ID!")

with col2:
    st.markdown("### Gemini-Style AI Chat (Simulation Mode)")

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Talk freely with your FinOps AI..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Thinking like Gemini AI..."):
                time.sleep(1)
                context = " ".join([m["content"] for m in st.session_state.chat_messages[-5:]])
                dynamic_responses = [
                    f"Hey! Regarding '{user_query}', your multi-cloud setup seems optimized. Have you checked automated shields?",
                    f"I see your question: '{user_query}'. AWS, Azure, and GCP resources are under monitoring. I recommend reviewing ABACUS policies.",
                    f"Analyzing '{user_query}'... your current thresholds look good, but consider adding alerts for critical resources.",
                    f"Regarding '{user_query}', multi-cloud efficiency is high. Generating SQL insights could help further optimization.",
                    f"Interesting query '{user_query}'. Your infrastructure is stable. Setting proactive cost alerts is suggested."
                ]
                full_response = random.choice(dynamic_responses)

                streamed_text = ""
                for word in full_response.split():
                    streamed_text += word + " "
                    message_placeholder.markdown(streamed_text + "▌")
                    time.sleep(0.02)
                message_placeholder.markdown(full_response)

            st.session_state.chat_messages.append({"role": "assistant", "content": full_response})

with st.expander("View Active Thresholds"):
    if st.session_state.thresholds:
        for rid, info in st.session_state.thresholds.items():
            st.write(f"{rid}: {info}")
    else:
        st.write("No thresholds set yet.")
