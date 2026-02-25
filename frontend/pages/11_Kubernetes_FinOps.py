import streamlit as st
import pandas as pd
from utils.ui_components import inject_tailwind, get_theme_css, render_profile_menu

st.set_page_config(page_title="Kubernetes FinOps | TEJUSKA", layout="wide")

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

st.markdown('<h1 class="text-3xl font-bold text-slate-900 dark:text-slate-50">Kubernetes Cluster Cost Optimization</h1>', unsafe_allow_html=True)
st.markdown('<p class="opacity-70 text-slate-700 dark:text-slate-300 mb-6">Deep dive into pod‑level and node‑level cost allocations across EKS, AKS, and GKE.</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["Namespace Cost", "Idle Pods", "Node Utilization"])

with tab1:
    st.markdown('<h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Cost by Namespace</h2>', unsafe_allow_html=True)
    namespace_data = pd.DataFrame({
        "Namespace": ["prod-payment-service", "dev-frontend", "prod-backend-api", "staging-cache", "data-ml"],
        "Cluster": ["eks-prod", "aks-dev", "gke-prod", "eks-staging", "gke-ml"],
        "Monthly Cost ($)": [2450, 380, 1760, 220, 890],
        "CPU Usage (cores)": [12, 2, 8, 1, 4],
        "Memory Usage (GB)": [48, 8, 32, 4, 16]
    })
    st.dataframe(namespace_data, use_container_width=True, hide_index=True,
                 column_config={"Monthly Cost ($)": st.column_config.NumberColumn(format="$%.0f")})

with tab2:
    st.markdown('<h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Over‑provisioned / Idle Pods</h2>', unsafe_allow_html=True)
    idle_pods = pd.DataFrame({
        "Pod Name": ["payment-service-7b9f6", "frontend-5c4d8", "cache-redis-2f3a1", "ml-inference-9e7b2"],
        "Namespace": ["prod", "dev", "staging", "data"],
        "Requested CPU": [4, 2, 1, 8],
        "Actual CPU (avg)": [0.3, 0.1, 0.05, 1.2],
        "Wasted Cost ($/mo)": [185, 42, 18, 320]
    })
    st.dataframe(idle_pods, use_container_width=True, hide_index=True,
                 column_config={"Wasted Cost ($/mo)": st.column_config.NumberColumn(format="$%.0f")})

    st.markdown(
        """
        <div class="p-4 mt-4 bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-800 rounded-lg">
            <p class="text-amber-800 dark:text-amber-200 text-sm">⚠️ Idle resources are costing you approximately $565/month.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Scale Down Selected Deployments", type="primary", use_container_width=True):
        st.success("Scaling down requested. Idle pods will be reduced, estimated savings: $450/month.")

with tab3:
    st.markdown('<h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Node Utilization</h2>', unsafe_allow_html=True)
    node_data = pd.DataFrame({
        "Node Name": ["ip-10-0-1-23", "ip-10-0-2-45", "ip-10-0-3-67", "aks-node-123", "gke-node-456"],
        "Instance Type": ["m5.large", "c5.xlarge", "r5.large", "Standard_D4s_v3", "n2-standard-4"],
        "CPU Utilization %": [68, 92, 45, 81, 37],
        "Memory Utilization %": [72, 88, 51, 79, 42],
        "Monthly Cost": [85, 170, 95, 130, 150]
    })
    st.dataframe(node_data, use_container_width=True, hide_index=True,
                 column_config={"Monthly Cost": st.column_config.NumberColumn(format="$%.0f")})

    # Add a recommendation card
    st.markdown(
        """
        <div class="p-4 mt-4 bg-emerald-50 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-800 rounded-lg">
            <p class="text-emerald-800 dark:text-emerald-200 text-sm">💡 Two nodes are underutilized. Consider rightsizing or bin packing to save ~$200/month.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
