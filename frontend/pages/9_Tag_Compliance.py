import streamlit as st
import pandas as pd
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu, metric_card

st.set_page_config(page_title="Tag Compliance | TEJUSKA", layout="wide")

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

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Cloud Resource Tagging & Compliance</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Identify and remediate untagged or non‑compliant resources across AWS, Azure, and GCP.</p>', unsafe_allow_html=True)

# Metrics cards
total_resources = 458
untagged_resources = 27
compliance_score = round((total_resources - untagged_resources) / total_resources * 100)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(metric_card("Total Resources", f"{total_resources}", None, st.session_state.theme), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Untagged Resources (Critical)", f"{untagged_resources}", None, st.session_state.theme), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Compliance Score", f"{compliance_score}%", None, st.session_state.theme), unsafe_allow_html=True)

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Non‑Compliant Resources</h2>', unsafe_allow_html=True)

# Dummy non-compliant resources data
non_compliant = pd.DataFrame({
    "Resource ID": ["i-12345", "vol-xyz12", "db-abcde", "snap-001", "lb-555"],
    "Type": ["EC2 Instance", "EBS Volume", "RDS Instance", "Snapshot", "Load Balancer"],
    "Cloud Provider": ["AWS", "AWS", "AWS", "Azure", "GCP"],
    "Missing Tags": ["Environment, Owner", "Project", "Environment", "Owner", "CostCenter, Project"],
    "Monthly Cost": [45.20, 8.00, 120.50, 2.50, 67.30]
})

st.dataframe(
    non_compliant,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Monthly Cost": st.column_config.NumberColumn(format="$%.2f")
    }
)

st.markdown('<hr class="my-6 border-slate-300 dark:border-slate-700">', unsafe_allow_html=True)

st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Bulk Tag Remediation</h2>', unsafe_allow_html=True)

with st.form("tag_remediation_form"):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        resource_id = st.text_input("Resource ID", placeholder="e.g., i-12345")
    with col_b:
        tag_key = st.text_input("Tag Key", placeholder="Environment")
    with col_c:
        tag_value = st.text_input("Tag Value", placeholder="Production")

    submit_tags = st.form_submit_button("Apply Tag", type="primary", use_container_width=True)

if submit_tags:
    if resource_id and tag_key and tag_value:
        st.success(f"Tag '{tag_key}: {tag_value}' applied to resource {resource_id}.")
    else:
        st.error("All fields are required.")
