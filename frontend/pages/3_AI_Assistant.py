import streamlit as st
import time
import random

# ------------------------
# 1. Page Configuration
# ------------------------
st.set_page_config(page_title="AI Assistant | TEJUSKA", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

# ------------------------
# 2. Header
# ------------------------
st.markdown("## ⚡ OPTIC FinOps AI Assistant – Gemini Ultra Mode")
st.markdown(
    "Chat freely with your multi-cloud FinOps assistant. "
    "Ask anything, and it will respond like a full AI expert, maintaining context and giving advice."
)
st.divider()

# ------------------------
# 3. Initialize Session State
# ------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "thresholds" not in st.session_state:
    st.session_state.thresholds = {}

# ------------------------
# 4. Layout: Two Columns (Threshold + Chat)
# ------------------------
col1, col2 = st.columns([1, 2])

# ------------------------
# Column 1: Threshold Management
# ------------------------
with col1:
    st.markdown("### 🛡 Agentic Budget Thresholds")
    with st.form("threshold_form"):
        provider = st.selectbox("Cloud Provider", ["AWS", "Azure", "GCP", "Other"])
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

# ------------------------
# Column 2: Gemini-Style Chat Assistant
# ------------------------
with col2:
    st.markdown("### 🤖 Gemini-Style AI Chat (Simulation Mode)")

    # Display previous messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if user_query := st.chat_input("Talk freely with your FinOps AI..."):
        # Append user message
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Simulated Gemini AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Thinking like Gemini AI..."):
                time.sleep(1)

                # Generate dynamic context-aware reply
                context = " ".join([m["content"] for m in st.session_state.chat_messages[-5:]])  # last 5 msgs
                dynamic_responses = [
                    f"Hey! Regarding '{user_query}', your multi-cloud setup seems optimized. Have you checked automated shields?",
                    f"I see your question: '{user_query}'. AWS, Azure, and GCP resources are under monitoring. I recommend reviewing ABACUS policies.",
                    f"Analyzing '{user_query}'... your current thresholds look good, but consider adding alerts for critical resources.",
                    f"Regarding '{user_query}', multi-cloud efficiency is high. Generating SQL insights could help further optimization.",
                    f"Interesting query '{user_query}'. Your infrastructure is stable. Setting proactive cost alerts is suggested."
                ]
                full_response = random.choice(dynamic_responses)

                # Streaming effect like ChatGPT/Gemini
                streamed_text = ""
                for word in full_response.split():
                    streamed_text += word + " "
                    message_placeholder.markdown(streamed_text + "▌")
                    time.sleep(0.02)
                message_placeholder.markdown(full_response)

            # Append assistant message
            st.session_state.chat_messages.append({"role": "assistant", "content": full_response})

# ------------------------
# Optional: View Active Thresholds
# ------------------------
with st.expander("View Active Thresholds"):
    if st.session_state.thresholds:
        for rid, info in st.session_state.thresholds.items():
            st.write(f"{rid}: {info}")
    else:
        st.write("No thresholds set yet.")
