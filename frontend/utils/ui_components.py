"""
ui_components.py
================
Reusable UI components for TEJUSKA Cloud Intelligence.
"""

import streamlit as st

def render_profile_menu():
    """
    Renders a GitHub‑style profile popover in the top‑right corner.
    Only visible when the user is authenticated.
    """
    if not st.session_state.get("authenticated", False):
        return

    # Custom CSS to position the popover trigger at top‑right
    st.markdown(
        """
        <style>
        div[data-testid="profile-menu-container"] {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 999;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Use a container to hold the popover trigger
    with st.container():
        st.markdown(
            '<div data-testid="profile-menu-container">',
            unsafe_allow_html=True,
        )
        # Popover trigger: user icon SVG (fill uses currentColor to adapt to theme)
        with st.popover(""):
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="8" r="4" />
                        <path d="M5 20v-2a7 7 0 0 1 14 0v2" />
                    </svg>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Popover content
            st.markdown(f"**Signed in as**  \n{st.session_state.tenant_id}")
            st.divider()
            if st.button("Profile", key="profile_btn", use_container_width=True):
                st.info("Profile page – under construction")
            if st.button("Settings", key="settings_btn", use_container_width=True):
                st.info("Settings – under construction")
            if st.button("Sign out", key="signout_btn", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.tenant_id = ""
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)"""
ui_components.py
================
Reusable UI components for TEJUSKA Cloud Intelligence.
"""

import streamlit as st

def render_profile_menu():
    """
    Renders a GitHub‑style profile popover in the top‑right corner.
    Only visible when the user is authenticated.
    """
    if not st.session_state.get("authenticated", False):
        return

    # Custom CSS to position the popover trigger at top‑right
    st.markdown(
        """
        <style>
        div[data-testid="profile-menu-container"] {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 999;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Use a container to hold the popover trigger
    with st.container():
        st.markdown(
            '<div data-testid="profile-menu-container">',
            unsafe_allow_html=True,
        )
        # Popover trigger: user icon SVG (fill uses currentColor to adapt to theme)
        with st.popover(""):
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="8" r="4" />
                        <path d="M5 20v-2a7 7 0 0 1 14 0v2" />
                    </svg>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Popover content
            st.markdown(f"**Signed in as**  \n{st.session_state.tenant_id}")
            st.divider()
            if st.button("Profile", key="profile_btn", use_container_width=True):
                st.info("Profile page – under construction")
            if st.button("Settings", key="settings_btn", use_container_width=True):
                st.info("Settings – under construction")
            if st.button("Sign out", key="signout_btn", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.tenant_id = ""
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
