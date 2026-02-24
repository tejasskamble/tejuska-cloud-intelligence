"""
ui_components.py
================
Reusable UI components built with Tailwind CSS for TEJUSKA Cloud Intelligence.
"""

import streamlit as st

def inject_tailwind():
    """Inject Tailwind CSS CDN into the app."""
    st.markdown(
        '<script src="https://cdn.tailwindcss.com"></script>',
        unsafe_allow_html=True,
    )

def get_theme_css(theme: str) -> str:
    """
    Returns a CSS string that overrides Streamlit's default colors based on the theme.
    This ensures all native Streamlit components (metrics, dataframes, etc.) inherit the theme.
    """
    if theme == "dark":
        return """
        <style>
            .stApp {
                background-color: #0F172A !important;  /* slate-900 */
                color: #F8FAFC !important;            /* slate-50 */
            }
            /* Metric cards */
            div[data-testid="metric-container"] {
                background-color: #1E293B !important;  /* slate-800 */
                color: #F8FAFC !important;
                border: 1px solid #334155 !important;  /* slate-700 */
            }
            label[data-testid="stMetricLabel"] {
                color: #F8FAFC !important;
                opacity: 0.8;
            }
            /* DataFrames */
            .stDataFrame {
                background-color: #1E293B !important;
                color: #F8FAFC !important;
            }
            .stDataFrame table {
                color: #F8FAFC !important;
            }
            .stDataFrame th {
                background: #818CF8 !important;
                color: white !important;
            }
            .stDataFrame td {
                background-color: #1E293B !important;
                color: #F8FAFC !important;
                border-bottom: 1px solid #334155 !important;
            }
            /* Input fields */
            .stTextInput input, .stTextInput textarea {
                background-color: #1E293B !important;
                color: #F8FAFC !important;
                border: 1px solid #334155 !important;
            }
            .stTextInput input:focus {
                border-color: #818CF8 !important;
            }
            /* Buttons */
            .stButton button {
                background: linear-gradient(135deg, #818CF8, #A78BFA) !important;
                color: white !important;
                border: none !important;
            }
            .stButton button[kind="secondary"] {
                background: transparent !important;
                border: 1px solid #818CF8 !important;
                color: #818CF8 !important;
            }
            .stButton button[kind="secondary"]:hover {
                background: #818CF8 !important;
                color: white !important;
            }
            /* Expander */
            .streamlit-expanderHeader {
                color: #F8FAFC !important;
                background-color: #1E293B !important;
            }
        </style>
        """
    else:
        return """
        <style>
            .stApp {
                background-color: #F8FAFC !important;  /* slate-50 */
                color: #0F172A !important;             /* slate-900 */
            }
            /* Metric cards */
            div[data-testid="metric-container"] {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border: 1px solid #E2E8F0 !important;  /* slate-200 */
            }
            label[data-testid="stMetricLabel"] {
                color: #0F172A !important;
                opacity: 0.8;
            }
            /* DataFrames */
            .stDataFrame {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }
            .stDataFrame table {
                color: #0F172A !important;
            }
            .stDataFrame th {
                background: #6366F1 !important;
                color: white !important;
            }
            .stDataFrame td {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border-bottom: 1px solid #E2E8F0 !important;
            }
            /* Input fields */
            .stTextInput input, .stTextInput textarea {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
                border: 1px solid #E2E8F0 !important;
            }
            .stTextInput input:focus {
                border-color: #6366F1 !important;
            }
            /* Buttons */
            .stButton button {
                background: linear-gradient(135deg, #6366F1, #818CF8) !important;
                color: white !important;
                border: none !important;
            }
            .stButton button[kind="secondary"] {
                background: transparent !important;
                border: 1px solid #6366F1 !important;
                color: #6366F1 !important;
            }
            .stButton button[kind="secondary"]:hover {
                background: #6366F1 !important;
                color: white !important;
            }
            /* Expander */
            .streamlit-expanderHeader {
                color: #0F172A !important;
                background-color: #FFFFFF !important;
            }
        </style>
        """

def render_profile_menu(theme: str):
    """
    Renders a GitHub‑style profile popover in the top‑right corner.
    Only visible when the user is authenticated.
    """
    if not st.session_state.get("authenticated", False):
        return

    text_color = "text-slate-900 dark:text-slate-50"

    # Fixed container for the popover trigger
    st.markdown(
        f"""
        <div class="fixed top-4 right-4 z-50">
            <div class="{text_color} cursor-pointer">
        """,
        unsafe_allow_html=True,
    )

    # Popover trigger: user icon SVG (stroke uses currentColor)
    with st.popover(""):
        st.markdown(
            f"""
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="{text_color}">
                <circle cx="12" cy="8" r="4" />
                <path d="M5 20v-2a7 7 0 0 1 14 0v2" />
            </svg>
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

    st.markdown("</div></div>", unsafe_allow_html=True)

def metric_card(label: str, value: str, delta: str = None, theme: str = "light") -> str:
    """
    Returns an HTML string for a metric card styled with Tailwind.
    """
    bg = "bg-white dark:bg-slate-800"
    text = "text-slate-900 dark:text-slate-50"
    border = "border-slate-200 dark:border-slate-700"
    shadow = "shadow-md dark:shadow-lg"

    delta_html = ""
    if delta:
        delta_color = "text-emerald-600 dark:text-emerald-400"
        delta_html = f'<p class="text-sm {delta_color}">{delta}</p>'

    return f"""
    <div class="p-6 rounded-xl {bg} {border} border {shadow} transition hover:shadow-xl">
        <p class="text-sm font-medium opacity-70">{label}</p>
        <p class="text-2xl font-bold {text}">{value}</p>
        {delta_html}
    </div>
    """

def pricing_card(title: str, price: str, features: list, theme: str = "light") -> str:
    """
    Returns an HTML string for a pricing card.
    """
    bg = "bg-white dark:bg-slate-800"
    text = "text-slate-900 dark:text-slate-50"
    border = "border-slate-200 dark:border-slate-700"
    primary = "text-indigo-600 dark:text-indigo-400"

    features_list = "".join([f'<li class="flex items-center gap-2"><span class="text-emerald-500">✓</span> {f}</li>' for f in features])

    return f"""
    <div class="p-8 rounded-2xl {bg} {border} border {text} transition hover:scale-105 hover:border-indigo-500">
        <h4 class="text-2xl font-bold {primary}">{title}</h4>
        <p class="text-lg font-semibold mt-2">{price}</p>
        <ul class="mt-4 space-y-2">
            {features_list}
        </ul>
    </div>
    """

def status_indicator(provider: str, is_connected: bool, theme: str = "light") -> str:
    """
    Returns HTML for a status indicator with colored circle.
    """
    text = "text-slate-900 dark:text-slate-50"
    circle = "bg-emerald-500" if is_connected else "bg-red-500"
    status = "Active" if is_connected else "Disconnected"
    return f"""
    <div class="flex items-center gap-2 {text}">
        <span class="w-3 h-3 rounded-full {circle} shadow-lg"></span>
        <span>{provider}: {status}</span>
    </div>
    """
