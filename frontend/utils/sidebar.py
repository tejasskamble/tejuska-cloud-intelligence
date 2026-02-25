"""
sidebar.py
==========
Reusable bottom‑profile component for the sidebar.
"""

import streamlit as st

def render_bottom_profile():
    """
    Renders a sticky profile card at the bottom of the sidebar.
    Must be called at the very end of the sidebar block in every page.
    """
    # Inject CSS to make the sidebar a flex column and push the last element to bottom
    st.sidebar.markdown(
        """
        <style>
        section[data-testid="stSidebar"] > div {
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
        }
        .profile-card {
            margin-top: auto;
            padding: 1rem 0.5rem;
            border-top: 1px solid rgba(128, 128, 128, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Profile card HTML – adapts to light/dark via Tailwind classes
    profile_html = """
    <div class="profile-card flex items-center gap-3 text-slate-900 dark:text-slate-50">
        <!-- Avatar SVG (circle) -->
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="8" r="4" />
            <path d="M5 20v-2a7 7 0 0 1 14 0v2" />
        </svg>
        <div class="flex-1">
            <div class="font-semibold">Admin</div>
            <div class="text-xs opacity-60">FinOps Admin</div>
        </div>
        <div class="flex gap-2">
            <a href="#" class="text-sm hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="3" />
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H5.78a1.65 1.65 0 0 0-1.51 1 1.65 1.65 0 0 0 .33 1.82l.04.04A10 10 0 0 0 12 17.66a10 10 0 0 0 6.36-2.62l.04-.04z" />
                    <path d="M12 9v4" />
                </svg>
            </a>
            <a href="#" class="text-sm hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                    <polyline points="16 17 21 12 16 7" />
                    <line x1="21" y1="12" x2="9" y2="12" />
                </svg>
            </a>
        </div>
    </div>
    """
    st.sidebar.markdown(profile_html, unsafe_allow_html=True)
