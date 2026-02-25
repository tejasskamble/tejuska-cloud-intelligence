import streamlit as st
import time
import random
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu

st.set_page_config(page_title="AI Assistant | TEJUSKA", layout="wide")

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

render_profile_menu(st.session_state.theme)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">OPTIC FinOps AI Assistant – Gemini Ultra Mode</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300">Chat freely with your multi-cloud FinOps assistant. Ask anything, and it will respond like a full AI expert, maintaining context and giving advice.</p>', unsafe_allow_html=True)

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "thresholds" not in st.session_state:
    st.session_state.thresholds = {}

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Agentic Budget Thresholds</h2>', unsafe_allow_html=True)
    with st.form("threshold_form"):
        st.markdown(
            f"""
            <div class="flex items-center gap-2 mb-2 text-slate-900 dark:text-slate-50">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 2v20M2 12h20"/>
                </svg>
                <span class="font-semibold">Cloud Provider</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        provider = st.selectbox("", ["AWS", "Azure", "GCP", "Other"], label_visibility="collapsed")
        resource_id = st.text_input("Resource ID", placeholder="e.g., i-09ca51ce7bcd242ed")
        threshold = st.number_input("Cost Threshold ($)", min_value=0.01, value=1.0, step=0.5)
        user_email = st.text_input("Alert Email", value=st.session_state.get("tenant_id", ""))

        submit_threshold = st.form_submit_button("Activate Agentic Shield", type="primary")
        if submit_threshold:
            if resource_id:
                st.session_state.thresholds[resource_id] = {"provider": provider, "limit": threshold, "email": user_email}
                st.success(f"Shield Activated! {provider} resource '{resource_id}' will be monitored and alerts sent to {user_email} if cost exceeds ${threshold:.2f}.")
            else:
                st.error("Enter a valid Resource ID!")

with col2:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50">Gemini-Style AI Chat (Simulation Mode)</h2>', unsafe_allow_html=True)

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
                # Simulate AI response
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
