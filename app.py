import streamlit as st
from components.sidebar import render_sidebar
from components.cards import metric_card, status_card, alert_card
from components.charts import (
    vehicle_health_chart, maintenance_trend_chart, driver_status_chart,
    alerts_trend_chart, traffic_violations_chart, engine_temperature_chart,
    battery_health_chart
)
from components.alerts import display_alerts, alert_summary, filter_alerts
from components.camera import display_camera_feed, camera_selector
from utils.data import (
    generate_vehicle_data, generate_maintenance_data, generate_driver_data,
    generate_traffic_violation_data, generate_alert_data, get_vehicle_stats
)

# Page config
st.set_page_config(
    page_title="DriveSense AI - Smart Vehicle Monitoring",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
page = render_sidebar()

# Main content routing
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.markdown("Welcome to DriveSense AI - Smart Vehicle Monitoring System")
    
    # Get statistics
    stats = get_vehicle_stats()
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🚛 Vehicles Online", stats['Vehicles_Online'], f"of {stats['Total_Vehicles']}")
    with col2:
        st.metric("🛠 Maintenance Due", stats['Maintenance_Due'], "vehicles")
    with col3:
        st.metric("😴 Drowsy Drivers", stats['Drowsy_Drivers'], "drivers")
    with col4:
        st.metric("🚦 Violations", stats['Traffic_Violations'], "today")
    with col5:
        st.metric("🔔 Total Alerts", stats['Total_Alerts'], "+3 today")
    
    st.divider()
    
    # Charts section
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(vehicle_health_chart(None), use_container_width=True)
    with col2:
        st.plotly_chart(driver_status_chart(None), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(maintenance_trend_chart(None), use_container_width=True)
    with col2:
        st.plotly_chart(alerts_trend_chart(None), use_container_width=True)
    
    st.plotly_chart(traffic_violations_chart(None), use_container_width=True)
    
    # Recent alerts
    st.subheader("🔔 Recent Alerts")
    alerts_df = generate_alert_data()
    display_alerts(alerts_df.head(5))

elif page == "🚗 Vehicle Health":
    st.title("🚗 Vehicle Health")
    
    # Vehicle data
    vehicle_data = generate_vehicle_data()
    vehicles = vehicle_data['Vehicle_ID'].unique()
    
    selected_vehicle = st.selectbox("Select Vehicle", vehicles)
    vehicle_info = vehicle_data[vehicle_data['Vehicle_ID'] == selected_vehicle].iloc[0]
    
    # Health metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🌡️ Engine Temp", f"{vehicle_info['Engine_Temp']}°C", "Normal")
    with col2:
        st.metric("🔋 Battery", f"{vehicle_info['Battery_Health']}%", "Good")
    with col3:
        st.metric("⛽ Fuel Level", f"{vehicle_info['Fuel_Level']}%", "Normal")
    with col4:
        st.metric("⚙️ RPM", f"{vehicle_info['Engine_RPM']} rpm", "Normal")
    with col5:
        st.metric("📊 Vibration", f"{vehicle_info['Vibration']:.2f} G", "Normal")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(engine_temperature_chart(), use_container_width=True)
    with col2:
        st.plotly_chart(battery_health_chart(), use_container_width=True)
    
    # Data table
    st.subheader("📊 Vehicle Data")
    st.dataframe(vehicle_data, use_container_width=True)

elif page == "🛠 Maintenance":
    st.title("🛠 Predictive Maintenance")
    
    maintenance_data = generate_maintenance_data()
    
    # Maintenance status cards
    for idx, row in maintenance_data.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 1.5, 1.5, 1.5, 1.5])
        
        with col1:
            st.write(f"**{row['Vehicle_ID']}**")
        with col2:
            risk_color = "🔴" if row['Risk_Score'] > 0.7 else "🟠" if row['Risk_Score'] > 0.4 else "🟢"
            st.write(f"{risk_color} Risk: {row['Risk_Score']:.2f}")
        with col3:
            st.write(f"📅 {row['Maintenance_Due']}")
        with col4:
            st.write(f"⏱️ {row['RUL']}")
        with col5:
            st.write(f"⚠️ {row['Failure_Prob']}")
        
        st.caption(f"Recommendation: {row['Recommendation']}")
        st.divider()
    
    # Maintenance trend
    st.plotly_chart(maintenance_trend_chart(None), use_container_width=True)
    
    # Data table
    st.subheader("📊 Detailed Maintenance Data")
    st.dataframe(maintenance_data, use_container_width=True)

elif page == "👤 Driver Monitoring":
    st.title("👤 Driver Monitoring")
    
    driver_data = generate_driver_data()
    
    # Driver status cards
    for idx, row in driver_data.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1, 1, 1])
        
        with col1:
            st.write(f"**{row['Driver_Name']}**")
            st.caption(row['Vehicle_ID'])
        with col2:
            score_color = "🔴" if row['Drowsiness_Score'] > 60 else "🟠" if row['Drowsiness_Score'] > 30 else "🟢"
            st.write(f"{score_color} Drowsiness: {row['Drowsiness_Score']}")
        with col3:
            st.write(f"🔔 {row['Alert_Count']}")
        with col4:
            st.write(row['Status'])
        with col5:
            st.write(row['Last_Alert'])
        
        st.divider()
    
    # Driver status chart
    st.plotly_chart(driver_status_chart(None), use_container_width=True)
    
    # Data table
    st.subheader("📊 Driver Data")
    st.dataframe(driver_data, use_container_width=True)

elif page == "🚦 Traffic Signs":
    st.title("🚦 Traffic Sign Recognition")
    
    st.info("YOLOv8-based Traffic Sign Detection")
    
    # Traffic violation data
    violation_data = generate_traffic_violation_data()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(traffic_violations_chart(None), use_container_width=True)
    
    with col2:
        st.subheader("Traffic Signs Detected")
        for idx, row in violation_data.iterrows():
            st.write(f"**{row['Violation_Type']}**: {row['Count']} times")
    
    # Sample detection display
    st.subheader("📷 Recent Detections")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Speed Limit 60**")
        st.info("Confidence: 0.92")
    with col2:
        st.markdown("**Stop Sign**")
        st.info("Confidence: 0.88")
    with col3:
        st.markdown("**No Entry**")
        st.info("Confidence: 0.95")

elif page == "📷 Live Cameras":
    st.title("📷 Live Camera Monitoring")
    
    # Camera selector
    camera_type = camera_selector()
    
    camera_names = {
        "front": "🚗 Front Camera",
        "driver": "👤 Driver Camera",
        "rear": "🔙 Rear Camera",
        "road": "🛣️ Road Camera"
    }
    
    st.subheader(camera_names[camera_type])
    
    # Camera feed
    col1, col2 = st.columns([3, 1])
    
    with col1:
        display_camera_feed(camera_names[camera_type])
    
    with col2:
        st.subheader("📊 Feed Stats")
        st.metric("FPS", "30")
        st.metric("Resolution", "1080p")
        st.metric("Status", "🟢 Active")
    
    # Camera settings
    st.subheader("⚙️ Camera Settings")
    col1, col2, col3 = st.columns(3)
    with col1:
        brightness = st.slider("Brightness", 0, 100, 50)
    with col2:
        contrast = st.slider("Contrast", 0, 100, 50)
    with col3:
        saturation = st.slider("Saturation", 0, 100, 50)

elif page == "🔔 Alerts":
    st.title("🔔 Alert Management")
    
    alerts_df = generate_alert_data()
    
    # Alert summary
    alert_summary({
        'critical': len(alerts_df[alerts_df['Severity'] == 'Critical']),
        'high': len(alerts_df[alerts_df['Severity'] == 'High']),
        'medium': len(alerts_df[alerts_df['Severity'] == 'Medium']),
        'low': len(alerts_df[alerts_df['Severity'] == 'Low'])
    })
    
    st.divider()
    
    # Filter alerts
    filtered_alerts = filter_alerts(alerts_df)
    
    st.subheader("📋 Alert History")
    display_alerts(filtered_alerts)

elif page == "📄 Reports":
    st.title("📄 Reports")
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Daily Summary", "Weekly Analysis", "Monthly Report", "Maintenance Report", "Safety Report"]
    )
    
    st.info(f"📊 {report_type} Report")
    
    if report_type == "Daily Summary":
        st.subheader("Today's Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Trips", 15)
        with col2:
            st.metric("Distance", "320 km")
        with col3:
            st.metric("Alerts", 8)
        with col4:
            st.metric("Violations", 2)
    
    elif report_type == "Weekly Analysis":
        st.subheader("This Week's Analysis")
        st.plotly_chart(alerts_trend_chart(None), use_container_width=True)
    
    elif report_type == "Monthly Report":
        st.subheader("Monthly Statistics")
        st.metric("Total Trips", "450")
        st.metric("Total Distance", "8,500 km")
        st.metric("Total Alerts", "180")
    
    elif report_type == "Maintenance Report":
        maintenance_data = generate_maintenance_data()
        st.dataframe(maintenance_data, use_container_width=True)
    
    elif report_type == "Safety Report":
        st.subheader("Safety Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Drowsy Incidents", 5)
        with col2:
            st.metric("Traffic Violations", 12)
        with col3:
            st.metric("Safety Score", "92%")

elif page == "⚙ Settings":
    st.title("⚙ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Display Settings")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        layout = st.selectbox("Layout", ["Wide", "Narrow"])
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 15)
    
    with col2:
        st.subheader("🔔 Notification Settings")
        critical_alerts = st.checkbox("Enable Critical Alerts", value=True)
        email_alerts = st.checkbox("Email Notifications", value=True)
        sms_alerts = st.checkbox("SMS Notifications", value=False)
    
    st.divider()
    
    st.subheader("👤 User Profile")
    username = st.text_input("Username", "admin")
    email = st.text_input("Email", "admin@drivesense.ai")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
    with col2:
        if st.button("🔄 Reset to Default"):
            st.info("Settings reset to default values")
    with col3:
        if st.button("🚀 Export Configuration"):
            st.info("Configuration exported successfully")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 12px; padding: 20px;'>"
    "DriveSense AI © 2024 | Smart Vehicle Monitoring System | Powered by TCS Mobility Solutions"
    "</div>",
    unsafe_allow_html=True
)
