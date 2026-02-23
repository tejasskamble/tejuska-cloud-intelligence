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
st.markdown("## ⚡ OPTIC FinOps AI Assistant – Infinity Ultra Pro Max (Simulated GPT)")
st.markdown(
    "Ask anything about your cloud infrastructure costs. "
    "This simulation responds like a ChatGPT FinOps assistant."
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
# Column 2: Simulated Chat Assistant
# ------------------------
with col2:
    st.markdown("### 🤖 FinOps Chat Assistant (Simulation Mode)")

    # Display previous messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if user_query := st.chat_input("Ask anything about your cloud infrastructure costs..."):
        # Append user message
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Simulated GPT-style response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner("Analyzing your cloud metrics..."):
                # Simulate processing
                time.sleep(1)

                # Generate dynamic GPT-style reply
                possible_responses = [
                    f"Simulated answer: '{user_query}'. Multi-cloud architecture looks optimized. Consider setting automated shields for further cost control.",
                    f"Analyzing '{user_query}'... All AWS/Azure/GCP resources are within thresholds. Suggest reviewing ABACUS policies.",
                    f"Got your query '{user_query}'. The cost projections are stable. You may want to enable automated alerts for {random.choice(['AWS', 'Azure', 'GCP'])} resources.",
                    f"Processed '{user_query}'. Multi-cloud efficiency is high. Recommend generating SQL insights for deeper analysis."
                ]

                full_response = random.choice(possible_responses)

                # Streaming effect like ChatGPT
                streamed_text = ""
                for word in full_response.split():
                    streamed_text += word + " "
                    message_placeholder.markdown(streamed_text + "▌")
                    time.sleep(0.02)
                message_placeholder.markdown(full_response)

            # Append simulated assistant message
            st.session_state.chat_messages.append({"role": "assistant", "content": full_response})

# ------------------------
# Optional: Show Active Thresholds
# ------------------------
with st.expander("View Active Thresholds"):
    if st.session_state.thresholds:
        for rid, info in st.session_state.thresholds.items():
            st.write(f"{rid}: {info}")
    else:
        st.write("No thresholds set yet.")
