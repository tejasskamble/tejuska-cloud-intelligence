import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu

st.set_page_config(page_title="Audit Logs | TEJUSKA", layout="wide")

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

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Agentic AI Action Logs & Audit Trail</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Transparent record of all automated remediations and notifications executed by the Agentic AI.</p>', unsafe_allow_html=True)

# Filter section
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Filter Logs</h2>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
    end_date = st.date_input("End Date", value=date.today())
with col2:
    action_type = st.selectbox("Action Type", ["All", "Terminated", "Downsized", "Alerted"])
with col3:
    cloud_provider = st.selectbox("Cloud Provider", ["All", "AWS", "Azure", "GCP"])

# Dummy log data
log_data = pd.DataFrame({
    "Timestamp": pd.date_range(start="2025-02-01", periods=15, freq="D").strftime("%Y-%m-%d %H:%M"),
    "AI Agent ID": ["AGENT-001", "AGENT-002", "AGENT-001", "AGENT-003", "AGENT-001",
                    "AGENT-002", "AGENT-003", "AGENT-001", "AGENT-002", "AGENT-001",
                    "AGENT-003", "AGENT-002", "AGENT-001", "AGENT-003", "AGENT-002"],
    "Action Performed": ["Terminated idle EC2", "Alerted cost spike", "Downsized RDS instance",
                         "Terminated unattached EBS", "Alerted anomaly", "Terminated idle EC2",
                         "Alerted budget", "Downsized Lambda", "Alerted forecast", "Terminated orphaned snapshot",
                         "Alerted anomaly", "Downsized EC2", "Terminated idle EC2", "Alerted anomaly", "Downsized Redshift"],
    "Resource ID": ["i-12345", "i-67890", "db-abcde", "vol-xyz12", "i-54321",
                    "i-09876", "snap-abc", "lambda-01", "i-11223", "snap-xyz",
                    "i-33445", "db-fghij", "i-55667", "i-77889", "rs-001"],
    "Cloud Provider": ["AWS", "AWS", "AWS", "AWS", "AWS",
                       "AWS", "Azure", "AWS", "GCP", "Azure",
                       "AWS", "AWS", "AWS", "GCP", "AWS"],
    "Cost Saved ($)": [45.20, 0.00, 120.50, 8.00, 0.00,
                       32.10, 0.00, 65.30, 0.00, 2.50,
                       0.00, 78.40, 23.60, 0.00, 94.00],
    "Status": ["Success", "Alerted", "Success", "Success", "Alerted",
               "Success", "Alerted", "Success", "Alerted", "Success",
               "Alerted", "Success", "Success", "Alerted", "Success"]
})

# Apply filters (simple simulation)
if action_type != "All":
    log_data = log_data[log_data["Action Performed"].str.contains(action_type, case=False)]
if cloud_provider != "All":
    log_data = log_data[log_data["Cloud Provider"] == cloud_provider]

# Display table with custom status badges using HTML
st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Audit Logs</h2>', unsafe_allow_html=True)

# Function to generate badge HTML
def status_badge(status):
    if status == "Success":
        return '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200">Success</span>'
    else:
        return '<span class="px-2 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200">Alerted</span>'

# Create a new column with badge HTML
log_data["Status Badge"] = log_data["Status"].apply(status_badge)

# Display as DataFrame with HTML column
st.markdown(
    log_data.to_html(escape=False, index=False, columns=["Timestamp", "AI Agent ID", "Action Performed", "Resource ID", "Cloud Provider", "Cost Saved ($)", "Status Badge"]),
    unsafe_allow_html=True
)

# Optional: add a download button
if st.button("Export Logs as CSV", type="secondary"):
    csv = log_data.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="audit_logs.csv", mime="text/csv")
