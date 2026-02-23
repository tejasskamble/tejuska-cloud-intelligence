import streamlit as st

st.set_page_config(page_title="Cloud Connect | TEJUSKA", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown("## 🔗 Multi-Cloud Integration Hub")
st.markdown("Securely connect your AWS, Azure, and GCP environments to enable autonomous FinOps governance.")
st.divider()

# --- Status Dashboard ---
st.markdown("### Active Connections Status")
col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.session_state.get("aws_connected"):
        st.success("AWS: Active 🟢")
    else:
        st.error("AWS: Disconnected 🔴")
with col_b:
    if st.session_state.get("azure_connected"):
        st.success("Azure: Active 🟢")
    else:
        st.error("Azure: Disconnected 🔴")
with col_c:
    if st.session_state.get("gcp_connected"):
        st.success("GCP: Active 🟢")
    else:
        st.error("GCP: Disconnected 🔴")

st.divider()

# --- Connection Forms ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### AWS Connection")
    with st.form("aws_connect_form"):
        aws_access_key = st.text_input("Access Key ID", type="password")
        aws_secret_key = st.text_input("Secret Access Key", type="password")
        aws_region = st.selectbox("Region", ["ap-south-1 (Mumbai)", "us-east-1 (N. Virginia)"])
        submit_aws = st.form_submit_button("Connect AWS", type="primary", use_container_width=True)
        if submit_aws and aws_access_key:
            st.session_state["aws_connected"] = True
            st.rerun()

with col2:
    st.markdown("#### Azure Connection")
    with st.form("azure_connect_form"):
        tenant_id = st.text_input("Tenant ID", type="password")
        client_id = st.text_input("Client ID", type="password")
        client_secret = st.text_input("Client Secret", type="password")
        submit_azure = st.form_submit_button("Connect Azure", type="primary", use_container_width=True)
        if submit_azure and tenant_id:
            st.session_state["azure_connected"] = True
            st.rerun()

with col3:
    st.markdown("#### GCP Connection")
    with st.form("gcp_connect_form"):
        gcp_project = st.text_input("Project ID")
        gcp_json = st.file_uploader("Upload Service Account JSON", type=["json"])
        submit_gcp = st.form_submit_button("Connect GCP", type="primary", use_container_width=True)
        if submit_gcp and gcp_project:
            st.session_state["gcp_connected"] = True
            st.rerun()
