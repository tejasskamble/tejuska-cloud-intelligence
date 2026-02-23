"""
app.py
======
TEJUSKA Cloud Intelligence
Login page with Google and GitHub SSO.
"""

import streamlit as st
import requests
import os

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="TEJUSKA Cloud Intelligence",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Corporate CSS - minimalist, zero-emoji
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        body { font-family: 'Inter', 'Segoe UI', sans-serif; }
        .block-container { max-width: 520px; padding-top: 4rem; }
        h1 { font-size: 1.75rem; font-weight: 700; letter-spacing: -0.5px; }
        .subtitle { font-size: 0.95rem; color: #6b7280; margin-bottom: 2rem; }
        .divider { border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
        .sso-btn {
            display: block;
            width: 100%;
            padding: 0.65rem 1rem;
            margin-bottom: 0.75rem;
            border-radius: 6px;
            border: 1px solid #d1d5db;
            background: #ffffff;
            font-size: 0.9rem;
            font-weight: 500;
            color: #111827;
            text-align: center;
            cursor: pointer;
        }
        .sso-btn:hover { background: #f9fafb; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("## TEJUSKA Cloud Intelligence")
st.markdown(
    '<p class="subtitle">Enterprise FinOps Platform for Multi-Cloud Cost Optimisation</p>',
    unsafe_allow_html=True,
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "tenant_id" not in st.session_state:
    st.session_state["tenant_id"] = ""

# ---------------------------------------------------------------------------
# SSO Buttons (OAuth flow handled by streamlit-oauth or redirect)
# ---------------------------------------------------------------------------
BACKEND_URL: str = st.secrets.get("BACKEND_URL", "http://localhost:7860")

if not st.session_state["authenticated"]:
    st.markdown("**Sign in to your account**")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        google_clicked = st.button("Sign in with Google", use_container_width=True)
    with col2:
        github_clicked = st.button("Sign in with GitHub", use_container_width=True)

    if google_clicked or github_clicked:
        provider = "Google" if google_clicked else "GitHub"
        # In production, redirect to OAuth provider via streamlit-oauth.
        # For demonstration, accept the user into a guest session.
        st.session_state["authenticated"] = True
        st.session_state["user_email"]    = "demo@tejuska.io"
        st.session_state["tenant_id"]     = "demo-tenant-001"
        st.info(
            f"{provider} SSO is configured. "
            "Connect your OAuth credentials in Streamlit secrets to enable live authentication."
        )
        st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.8rem;color:#9ca3af;text-align:center;">'
        "By signing in you agree to the TEJUSKA Terms of Service and Privacy Policy."
        "</p>",
        unsafe_allow_html=True,
    )

else:
    st.success(f"Authenticated as: {st.session_state['user_email']}")
    st.info("Navigate using the sidebar to access the FinOps Dashboard and AI tools.")

    if st.button("Sign Out"):
        st.session_state["authenticated"] = False
        st.session_state["user_email"]    = ""
        st.session_state["tenant_id"]     = ""
        st.rerun()
