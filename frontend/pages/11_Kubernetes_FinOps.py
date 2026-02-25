import streamlit as st
import pandas as pd
from utils.ui_components import inject_tailwind, get_theme_css
from utils.sidebar import render_bottom_profile

st.set_page_config(page_title="Kubernetes FinOps | TEJUSKA", layout="wide")

inject_tailwind()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

with st.sidebar:
    st.markdown("## Appearance")
    dark_mode = st.toggle("Dark mode", value=(st.session_state.theme == "dark"))
    st.session_state.theme = "dark" if dark_mode else "light"
    render_bottom_profile()

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

if not st.session_state.get("authenticated"):
    st.warning("Please sign in from the Home page.")
    st.stop()

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Kubernetes Cluster Cost Optimization</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Deep dive into pod-level and node-level cost allocations across EKS, AKS, and GKE.</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["Namespace Cost", "Idle Pods", "Node Utilization"])

with tab1:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Namespace Cost Breakdown</h2>', unsafe_allow_html=True)
    namespace_data = pd.DataFrame({
        "Namespace": ["prod-payment-service", "dev-frontend", "prod-auth-service", "staging-backend", "monitoring"],
        "Cluster": ["eks-prod", "eks-dev", "aks-prod", "gke-staging", "eks-prod"],
        "CPU Cost ($)": [1240, 320, 890, 210, 150],
        "Memory Cost ($)": [860, 180, 570, 130, 220],
        "Total Cost ($)": [2100, 500, 1460, 340, 370]
    })
    st.dataframe(namespace_data, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Idle / Over‑Provisioned Pods</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="p-4 mb-4 text-sm text-amber-800 bg-amber-100 rounded-lg dark:bg-amber-900 dark:text-amber-200" role="alert">
            <span class="font-medium">Warning:</span> 8 pods have been running with CPU usage below 5% for over 24 hours.
        </div>
        """,
        unsafe_allow_html=True,
    )
    idle_pods = pd.DataFrame({
        "Pod Name": ["frontend-7d8f9c", "redis-cache-2b3k", "sidecar-injector", "logging-agent", "old-worker"],
        "Namespace": ["dev-frontend", "dev-cache", "prod-mesh", "monitoring", "staging"],
        "Requested CPU": ["2 cores", "1 core", "0.5 core", "1 core", "4 cores"],
        "Actual CPU (avg)": ["0.08 cores", "0.02 cores", "0.03 cores", "0.1 cores", "0.2 cores"],
        "Monthly Waste ($)": [85, 42, 18, 38, 210]
    })
    st.dataframe(idle_pods, use_container_width=True, hide_index=True)

    if st.button("Scale Down Deployments", type="primary"):
        st.success("Initiating scale-down for idle pods... (simulated)")

with tab3:
    st.markdown('<h2 class="text-xl font-semibold text-slate-900 dark:text-slate-50 mb-4">Node Utilization</h2>', unsafe_allow_html=True)
    node_data = pd.DataFrame({
        "Node Name": ["ip-10-1-1-1", "ip-10-1-1-2", "ip-10-1-1-3", "aks-np-123", "gke-node-001"],
        "Instance Type": ["m5.large", "m5.xlarge", "c5.2xlarge", "Standard_D4s_v3", "e2-standard-4"],
        "CPU Util %": [78, 92, 45, 33, 67],
        "Memory Util %": [65, 88, 52, 28, 71],
        "Monthly Cost ($)": [185, 370, 520, 290, 410]
    })
    st.dataframe(node_data, use_container_width=True, hide_index=True)
