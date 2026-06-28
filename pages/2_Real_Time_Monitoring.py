import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Real-Time Monitoring", page_icon="📡")

st.title("📡 Real-Time Vehicle Monitoring")
st.markdown("Live monitoring of all connected vehicles")

# Auto-refresh
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

# Vehicle selector
vehicles = ['VEH-001', 'VEH-002', 'VEH-003', 'VEH-004', 'VEH-005']
selected_vehicles = st.multiselect("Select Vehicles to Monitor", vehicles, default=vehicles)

st.divider()

# Real-time metrics dashboard
st.subheader("🚗 Live Vehicle Status")

for vehicle in selected_vehicles:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric(f"{vehicle} - Speed", f"{np.random.randint(40, 120)} km/h", f"Avg: 75")
    with col2:
        st.metric("Engine Temp", f"{np.random.randint(70, 95)}°C", "Normal")
    with col3:
        st.metric("RPM", f"{np.random.randint(1000, 4000)}", "Normal")
    with col4:
        st.metric("Fuel Level", f"{np.random.randint(20, 95)}%", "Good")
    with col5:
        st.metric("Battery", f"{np.random.randint(85, 100)}%", "Excellent")
    with col6:
        status = np.random.choice(['🟢 Active', '🟡 Idle', '🔴 Alert'])
        st.metric("Status", status.split()[0], status.split()[1])
    
    st.divider()

# Real-time alerts
st.subheader("🔔 Real-Time Alerts")

alert_data = {
    'Vehicle': ['VEH-002', 'VEH-004', 'VEH-001'],
    'Alert Type': ['High Speed', 'Engine Warning', 'Maintenance Due'],
    'Severity': ['🟡 Medium', '🔴 Critical', '🟠 High'],
    'Time': ['2 min ago', '5 min ago', '15 min ago'],
    'Status': ['⏳ Ongoing', '✅ Resolved', '🔵 New']
}

df_alerts = pd.DataFrame(alert_data)
st.dataframe(df_alerts, use_container_width=True)

# Live chart
st.subheader("📊 Fleet Speed Distribution")

# Generate mock speed data
speeds = np.random.normal(75, 15, 100)
speeds = np.clip(speeds, 0, 140)

fig = go.Figure()
fig.add_trace(go.Histogram(x=speeds, nbinsx=20, name='Speed Distribution'))
fig.update_layout(
    title="Real-Time Fleet Speed Distribution",
    xaxis_title="Speed (km/h)",
    yaxis_title="Number of Vehicles",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# GPS Map placeholder
st.subheader("🗺️ Vehicle Locations")

st.info("📍 GPS Map View - Shows real-time vehicle locations on map (Integration with mapping library required)")

# Location table
location_data = {
    'Vehicle': vehicles,
    'Latitude': np.random.uniform(28.5, 28.7, 5),
    'Longitude': np.random.uniform(77.1, 77.3, 5),
    'Speed': np.random.randint(30, 100, 5),
    'Direction': ['North', 'East', 'South', 'West', 'North-East']
}

st.dataframe(pd.DataFrame(location_data), use_container_width=True)

# Communication stats
st.subheader("📡 Network Status")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Connected Vehicles", "5", "100%")
with col2:
    st.metric("Avg Latency", "45ms", "-5ms")
with col3:
    st.metric("Data Rate", "2.5 MB/s", "Optimal")
with col4:
    st.metric("Signal Quality", "95%", "Excellent")
