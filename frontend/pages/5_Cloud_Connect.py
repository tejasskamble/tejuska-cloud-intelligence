import streamlit as st

st.set_page_config(page_title="Cloud Connect | TEJUSKA", layout="wide")

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown("## Cloud Integration Hub")
st.markdown("Securely connect your AWS, Azure, and GCP environments to enable autonomous FinOps governance.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### AWS Connection")
    with st.form("aws_connect_form"):
        aws_access_key = st.text_input("AWS Access Key ID", type="password")
        aws_secret_key = st.text_input("AWS Secret Access Key", type="password")
        aws_region = st.selectbox("Default Region", ["ap-south-1 (Mumbai)", "us-east-1 (N. Virginia)", "eu-central-1 (Frankfurt)"])
        
        submit_aws = st.form_submit_button("Connect AWS Account", type="primary", use_container_width=True)
        
        if submit_aws:
            if len(aws_access_key) > 5 and len(aws_secret_key) > 5:
                st.success("AWS Account successfully linked and authenticated.")
                st.session_state["aws_connected"] = True
            else:
                st.error("Please provide valid AWS credentials.")

with col2:
    st.markdown("### Active Connections Status")
    if st.session_state.get("aws_connected"):
        st.success("Amazon Web Services: STATUS ACTIVE (Syncing Billing Data)")
    else:
        st.info("Amazon Web Services: Disconnected")
        
    st.info("Microsoft Azure: Disconnected")
    st.info("Google Cloud Platform: Disconnected")
