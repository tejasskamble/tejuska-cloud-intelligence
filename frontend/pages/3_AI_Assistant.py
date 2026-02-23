import streamlit as st
import openai
import time

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
st.markdown("## ⚡ OPTIC FinOps AI Assistant – Infinity Ultra Pro Max")
st.markdown(
    "Ask anything about your cloud infrastructure costs. "
    "The Agentic AI can analyze multi-cloud metrics, generate SQL insights, and give recommendations."
)
st.divider()

# ------------------------
# 3. OpenAI API Setup
# ------------------------
try:
    openai.api_key = st.secrets["openai"]["api_key"]
except:
    st.warning("OpenAI API key not found! Using local simulation mode.")
    openai.api_key = None

# ------------------------
# 4. Initialize Chat & Threshold Session State
# ------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "thresholds" not in st.session_state:
    st.session_state.thresholds = {}  # cloud resource thresholds

# ------------------------
# 5. Layout: Two Columns (Threshold + Chat)
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
        user_email = st.text_input(
            "Alert Email", value=st.session_state.get("tenant_id", "")
        )

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
# Column 2: ChatGPT Assistant
# ------------------------
with col2:
    st.markdown("### 🤖 FinOps Chat Assistant")

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

        # GPT response / fallback simulation
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Analyzing multi-cloud metrics & FinOps insights..."):
                try:
                    if openai.api_key:
                        # Prepare system + chat context
                        system_prompt = {
                            "role": "system",
                            "content": (
                                "You are an expert FinOps AI assistant. Analyze cloud costs, thresholds, "
                                "resource utilization, and give recommendations. "
                                "You may generate SQL queries or provide guidance for AWS, Azure, GCP resources."
                            )
                        }
                        messages = [system_prompt] + st.session_state.chat_messages

                        # GPT call
                        response = openai.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=messages,
                            temperature=0.3,
                            max_tokens=800
                        )
                        full_response = response.choices[0].message.content
                    else:
                        raise Exception("API key missing, using simulated response.")

                except Exception as e:
                    # Fallback simulation
                    lower_query = user_query.lower()
                    if "aws" in lower_query or "ec2" in lower_query:
                        full_response = (
                            "Based on simulated telemetry, your AWS EC2 instances are running within "
                            "$1 threshold. Projected monthly spend looks stable. No anomalies detected."
                        )
                    elif "terminate" in lower_query or "kill" in lower_query:
                        full_response = (
                            "Simulation: Resource termination requires exact Resource ID in 'Pro Automations' tab."
                        )
                    else:
                        full_response = (
                            f"Simulated answer: '{user_query}'. Multi-cloud architecture looks optimized. "
                            "Consider setting automated shields for further cost control."
                        )

                # Streaming effect
                streamed_text = ""
                for word in full_response.split():
                    streamed_text += word + " "
                    message_placeholder.markdown(streamed_text + "▌")
                    time.sleep(0.01)
                message_placeholder.markdown(full_response)

            # Append assistant message to session
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": full_response}
            )

# ------------------------
# Optional: Show Current Thresholds
# ------------------------
with st.expander("View Active Thresholds"):
    if st.session_state.thresholds:
        for rid, info in st.session_state.thresholds.items():
            st.write(f"{rid}: {info}")
    else:
        st.write("No thresholds set yet.")
