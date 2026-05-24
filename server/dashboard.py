import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="AIOps Control Plane", layout="wide")
st.title("🤖 AIOps Fleet Management Dashboard")

st.sidebar.markdown("### Dashboard Engine Settings")
st_refresh = st.sidebar.slider("Refresh Frame Interval (s)", 1, 10, 3)
st.fragment(run_every=st_refresh)

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "aiops_logs.json"))

def load_local_logs():
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame()
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
            rows = []
            for item in data:
                rows.append({
                    "trace_id": item.get("trace_id"),
                    "agent_name": item.get("agent_name"),
                    "status": item.get("status"),
                    "timestamp": datetime.fromtimestamp(item.get("timestamp", datetime.now().timestamp())),
                    "latency": item.get("latency_seconds", 0.0),
                    "total_tokens": item.get("metrics", {}).get("total_tokens", 0),
                    "error_type": item.get("error", {}).get("type", "None") if item.get("error") else "None"
                })
            return pd.DataFrame(rows)
    except Exception:
        return pd.DataFrame()

df = load_local_logs()

if df.empty:
    st.info("🔄 Ingestion streams idling. Awaiting trace telemetry packets from active agent nodes...")
else:
    # Topline Metric Ribbon
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Executed Tasks", len(df))
    failed = len(df[df["status"] == "FAILED"])
    c2.metric("System Outage Rate", f"{(failed/len(df))*100:.1f}%", f"{failed} errors", delta_color="inverse")
    c3.metric("Aggregated Fleet Token Volume", f"{df['total_tokens'].sum():,}")

    st.markdown("---")
    
    # Graphs
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(px.bar(df, x="agent_name", y="total_tokens", color="status", title="Resource Allocation metrics"), use_container_width=True)
    with g2:
        st.plotly_chart(px.line(df.sort_values("timestamp"), x="timestamp", y="latency", title="Latency Curves"), use_container_width=True)

    st.subheader("Historical Log Feed")
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)