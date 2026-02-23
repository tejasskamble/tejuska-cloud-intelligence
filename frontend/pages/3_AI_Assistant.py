import streamlit as st
import requests
import time

# 1. Page Configuration
st.set_page_config(page_title="AI Assistant | TEJUSKA", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

# 2. Header Section
st.markdown("## OPTIC FinOps AI Assistant")
st.markdown("Interact with your cloud financial data using natural language. The Agentic AI translates your queries into SQL to fetch real-time insights.")
st.divider()

# Safely fetch backend URL
try:
    BACKEND_URL = st.secrets["api"]["backend_url"]
except:
    BACKEND_URL = "https://tejuska-tejuska-cloud-intelligence.hf.space"

# 3. Initialize Chat History in Session State
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages =

# 4. Display previous chat messages
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input & Processing
if user_query := st.chat_input("Ask anything about your cloud infrastructure costs..."):
    
    # Append user message to state and display
    st.session_state.chat_messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Assistant response generation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Analyzing FOCUS 1.1 telemetry and reasoning..."):
            try:
                # In production, this hits your FastAPI LangChain endpoint
                # response = requests.post(f"{BACKEND_URL}/chat", json={"query": user_query, "tenant": st.session_state.tenant_id}, timeout=15)
                # full_response = response.json().get("answer")
                
                # Simulated AI Reasoning for Demonstration purposes
                time.sleep(2)
                if "aws" in user_query.lower() or "ec2" in user_query.lower():
                    full_response = f"Based on the latest telemetry, your AWS EC2 instances are running within the defined $1.00 threshold. The current projected spend for the month is stable. I have monitored 'i-09ca51ce7bcd242ed' and found no anomalies."
                elif "terminate" in user_query.lower() or "kill" in user_query.lower():
                    full_response = "I can execute resource termination via the ABACUS engine. However, you need to initiate the exact Resource ID in the 'Pro Automations' tab to ensure strict compliance and safety protocols."
                else:
                    full_response = f"I have processed your query: '{user_query}'. According to our multi-cloud database, your overall architecture is highly optimized. I recommend reviewing the 'Pro Automations' tab to set up automated shields for further cost savings."
            except Exception as e:
                full_response = "I am currently unable to reach the database reasoning engine. Please check the backend connection."

            # Streaming effect (typing animation) like ChatGPT
            streamed_text = ""
            for word in full_response.split():
                streamed_text += word + " "
                time.sleep(0.04)
                message_placeholder.markdown(streamed_text + "▌")
            
            # Final output without cursor
            message_placeholder.markdown(full_response)
            
    # Append assistant message to state
    st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
