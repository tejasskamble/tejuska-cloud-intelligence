import streamlit as st
import time
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

# Initialize chat history
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello Admin, I am your Tejuska FinOps Agent. I can analyze cost spikes or optimize your DevOps pipelines. How can I help?"}
    ]

# Page title
st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">FinOps GenAI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Your intelligent copilot for cloud cost optimization.</p>', unsafe_allow_html=True)

# Quick prompts – Tailwind-styled buttons (using st.button for functionality)
st.markdown('<p class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Quick prompts:</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Analyze yesterday's AWS spike", key="q1", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": "Analyze yesterday's AWS spike"})
        # Simulate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1)
            response = "I've analyzed the AWS cost spike. It appears to be caused by a new EC2 instance type in us-east-1. You could save ~$320 by switching to reserved instances."
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
with col2:
    if st.button("Find idle resources", key="q2", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": "Find idle resources"})
        with st.chat_message("assistant"):
            with st.spinner("Scanning..."):
                time.sleep(1.5)
            response = "I found 3 idle resources: an unattached EBS volume (gp2, 100GB) in eu-west-1, an idle t3.micro EC2 instance running for 7 days with <1% CPU, and an unused elastic IP. Terminating them could save $87/month."
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
with col3:
    if st.button("Optimize dev pipeline", key="q3", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": "Optimize dev pipeline"})
        with st.chat_message("assistant"):
            with st.spinner("Analyzing pipeline..."):
                time.sleep(2)
            response = "Your CI/CD pipeline uses on-demand runners. Switching to spot instances for non‑production jobs could reduce costs by 60‑70%. Estimated monthly saving: $210."
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()

# Display chat history
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your cloud costs..."):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(1.5)
        # Simulate varied response
        response = f"Regarding '{prompt}': I've analyzed your recent usage. Consider reviewing your DevOps pipelines for rightsizing opportunities. Would you like a detailed report?"
        st.markdown(response)
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
