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

def render_profile_menu(theme: str):
    """
    Renders a GitHub‑style profile popover in the top‑right corner.
    Only visible when the user is authenticated.
    """
    if not st.session_state.get("authenticated", False):
        return

    # Choose text color based on theme
    text_color = "text-slate-900" if theme == "light" else "text-slate-50"

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
    bg = "bg-white" if theme == "light" else "bg-slate-800"
    text = "text-slate-900" if theme == "light" else "text-slate-50"
    border = "border-slate-200" if theme == "light" else "border-slate-700"
    shadow = "shadow-md" if theme == "light" else "shadow-lg"

    delta_html = ""
    if delta:
        delta_color = "text-emerald-600" if theme == "light" else "text-emerald-400"
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
    bg = "bg-white" if theme == "light" else "bg-slate-800"
    text = "text-slate-900" if theme == "light" else "text-slate-50"
    border = "border-slate-200" if theme == "light" else "border-slate-700"
    primary = "text-indigo-600" if theme == "light" else "text-indigo-400"

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
    text = "text-slate-900" if theme == "light" else "text-slate-50"
    circle = "bg-emerald-500" if is_connected else "bg-red-500"
    status = "Active" if is_connected else "Disconnected"
    return f"""
    <div class="flex items-center gap-2 {text}">
        <span class="w-3 h-3 rounded-full {circle} shadow-lg"></span>
        <span>{provider}: {status}</span>
    </div>
    """
