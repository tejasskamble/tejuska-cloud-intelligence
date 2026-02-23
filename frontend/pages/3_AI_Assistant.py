"""
3_AI_Assistant.py
=================
TEJUSKA Cloud Intelligence
OPTIC AI Assistant - Natural language cloud cost queries powered by LLM + Text-to-SQL.
"""

import streamlit as st
import requests

st.set_page_config(
    page_title="AI Assistant | TEJUSKA",
    layout="wide",
)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page to access this section.")
    st.stop()

BACKEND_URL: str = st.secrets.get("BACKEND_URL", "http://localhost:7860")
TENANT_ID: str   = st.session_state.get("tenant_id", "")

st.markdown("# OPTIC AI Assistant")
st.markdown(
    "Ask any question about your cloud costs in plain English. "
    "OPTIC translates your query to SQL, retrieves the data, and returns a concise answer."
)
st.divider()

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for message in st.session_state["chat_history"]:
    role  = message["role"]
    label = "You" if role == "user" else "OPTIC"
    with st.chat_message(role):
        st.write(message["content"])
        if role == "assistant" and message.get("sql"):
            with st.expander("View Generated SQL"):
                st.code(message["sql"], language="sql")

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
user_input: str = st.chat_input("Ask about your cloud spend...")

if user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    with st.spinner("OPTIC is processing your query..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/query",
                json={"tenant_id": TENANT_ID, "query": user_input},
                timeout=60,
            )
            if response.status_code == 200:
                data    = response.json()
                answer  = data.get("answer", "No answer returned.")
                sql     = data.get("sql", "")
                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": answer, "sql": sql}
                )
            else:
                st.session_state["chat_history"].append(
                    {
                        "role":    "assistant",
                        "content": f"Error from backend (HTTP {response.status_code}): {response.text}",
                        "sql":     "",
                    }
                )
        except requests.exceptions.ConnectionError:
            st.session_state["chat_history"].append(
                {
                    "role":    "assistant",
                    "content": "Could not reach the backend. Verify BACKEND_URL in secrets.",
                    "sql":     "",
                }
            )

    st.rerun()
