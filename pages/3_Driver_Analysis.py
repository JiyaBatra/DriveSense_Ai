import streamlit as st
import pandas as pd
import numpy as np
from utils.driver_monitoring import DriverBehaviorAnalyzer
import plotly.graph_objects as go

st.set_page_config(page_title="Driver Analysis", page_icon="👤")

st.title("👤 Driver Analysis & Monitoring")
st.markdown("Comprehensive driver safety and behavior analysis")

# Driver selector
drivers = ['John Smith - VEH-001', 'Sarah Johnson - VEH-002', 'Mike Davis - VEH-003', 
           'Emma Wilson - VEH-004', 'David Brown - VEH-005']
selected_driver = st.selectbox("Select Driver", drivers)

st.divider()

# Driver profile and current status
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👤 Current Status", "Alert", "✅ Normal")
with col2:
    st.metric("⏱️ Drowsiness Score", "25", "Low Risk")
with col3:
    st.metric("🛣️ Distance Driven", "245 km", "Today")

st.divider()

# Tabs for driver analysis
tab1, tab2, tab3, tab4 = st.tabs(["Live Monitoring", "Behavior Analysis", "Safety Report", "Trip History"])

with tab1:
    st.subheader("🔍 Live Driver Monitoring")
    
    # Eye detection visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("📷 Driver Camera Feed")
        st.markdown(
            "<div style='background-color: #222; padding: 40px; border-radius: 10px; text-align: center; color: white;'>"
            "<p style='font-size: 48px;'>👁️</p><p>Live Camera Feed - Connect camera source</p>"
            "</div>",
            unsafe_allow_html=True
        )
    
    with col2:
        st.subheader("📊 Eye Metrics")
        st.metric("Eye Aspect Ratio (EAR)", "0.38", "Normal")
        st.metric("Blink Rate", "18/min", "Normal")
        st.metric("Eye Open Duration", "95%", "Good")

with tab2:
    st.subheader("📈 Behavior Analysis")
    
    analyzer = DriverBehaviorAnalyzer()
    
    # Behavior metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🚗 Avg Speed", "65 km/h", "Safe")
    with col2:
        st.metric("⚡ Harsh Accel.", "2 events", "Fair")
    with col3:
        st.metric("🛑 Harsh Braking", "3 events", "Fair")
    with col4:
        st.metric("📵 Distractions", "1 event", "Good")
    
    st.divider()
    
    # Behavior chart
    behaviors = ['Speeding', 'Harsh Acceleration', 'Harsh Braking', 'Distractions', 'Lane Departure']
    occurrences = [2, 2, 3, 1, 0]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=behaviors, y=occurrences, marker=dict(color='#ff6692')))
    fig.update_layout(title="Unsafe Driving Behaviors (Last Trip)", height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk factors
    st.subheader("⚠️ Risk Factors")
    
    risk_factors = {
        'Risk Factor': ['Fatigue Level', 'Attention Level', 'Road Familiarity', 'Vehicle Condition', 'Weather Conditions'],
        'Status': ['🟢 Low', '🟢 Good', '🟡 Medium', '🟢 Good', '🟡 Fair'],
        'Impact': ['Low', 'Medium', 'Low', 'Low', 'Medium']
    }
    
    st.dataframe(pd.DataFrame(risk_factors), use_container_width=True)

with tab3:
    st.subheader("📋 Safety Report")
    
    # Trip statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Today's Trip")
        st.metric("Duration", "4 hours 30 min")
        st.metric("Distance", "245 km")
        st.metric("Avg Speed", "65 km/h")
        st.metric("Alerts Generated", "8")
    
    with col2:
        st.subheader("Safety Metrics")
        st.metric("Safety Score", "82/100", "Good")
        st.metric("Drowsiness Incidents", "1")
        st.metric("Speed Violations", "2")
        st.metric("Distraction Events", "1")
    
    st.divider()
    
    # Safety recommendations
    st.subheader("💡 Safety Recommendations")
    
    recommendations = [
        "✅ Maintain current alertness level",
        "⚠️ Reduce speed in residential areas",
        "💤 Take a 15-minute break every 2 hours",
        "📱 Minimize phone usage while driving",
        "👁️ Monitor for signs of drowsiness"
    ]
    
    for rec in recommendations:
        st.write(rec)

with tab4:
    st.subheader("📍 Trip History")
    
    # Trip data
    trips = {
        'Date': pd.date_range('2024-06-20', periods=5, freq='D'),
        'Distance': [245, 180, 320, 150, 290],
        'Duration': ['4h 30m', '3h 15m', '5h 45m', '2h 30m', '4h 15m'],
        'Avg Speed': [65, 60, 70, 62, 75],
        'Safety Score': [82, 88, 75, 90, 80],
        'Incidents': [8, 4, 12, 2, 6]
    }
    
    df_trips = pd.DataFrame(trips)
    st.dataframe(df_trips, use_container_width=True)
    
    # Trip timeline
    st.subheader("📊 Monthly Trends")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_trips['Date'], y=df_trips['Safety Score'], 
                            mode='lines+markers', name='Safety Score', line=dict(color='#636EFA')))
    fig.update_layout(title="Safety Score Trend", xaxis_title="Date", yaxis_title="Score", height=400)
    
    st.plotly_chart(fig, use_container_width=True)
