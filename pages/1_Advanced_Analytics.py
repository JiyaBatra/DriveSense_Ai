import streamlit as st
import pandas as pd
import numpy as np
from utils.vehicle_health import MaintenancePredictionModel, FuelEfficiencyAnalyzer
from components.charts import engine_temperature_chart, battery_health_chart

st.set_page_config(page_title="Advanced Analytics", page_icon="📊")

st.title("📊 Advanced Analytics")
st.markdown("Comprehensive vehicle and driver analytics")

# Tabs for different analytics
tab1, tab2, tab3, tab4 = st.tabs(["Predictive Analysis", "Fuel Efficiency", "Performance Metrics", "Trend Analysis"])

with tab1:
    st.subheader("🔮 Predictive Maintenance Analysis")
    
    maintenance_model = MaintenancePredictionModel()
    
    # Sample vehicle data
    vehicle_data = {
        'mileage': 85000,
        'age_days': 1200,
        'engine_temp': 85
    }
    
    prediction = maintenance_model.predict_maintenance_schedule(vehicle_data)
    
    # Display predictions
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Risk", f"{prediction['overall_risk']:.2%}", "Alert" if prediction['overall_risk'] > 0.5 else "Normal")
    with col2:
        st.metric("Critical Components", len(prediction['critical_components']))
    with col3:
        st.metric("Next Service", "7 days" if prediction['critical_components'] else "60 days")
    
    st.divider()
    
    # Component breakdown
    st.subheader("Component Health Breakdown")
    
    components_data = []
    for component, data in prediction['schedule'].items():
        components_data.append({
            'Component': component,
            'Risk Score': data['risk_score'],
            'Status': data['status'],
            'Days Until Service': data['days_until_maintenance']
        })
    
    df_components = pd.DataFrame(components_data)
    
    # Style risk scores
    def color_code_risk(val):
        if val > 0.8:
            return 'background-color: #ff6692'
        elif val > 0.6:
            return 'background-color: #ffa500'
        elif val > 0.4:
            return 'background-color: #ffc107'
        else:
            return 'background-color: #00cc96'
    
    st.dataframe(
        df_components.style.applymap(color_code_risk, subset=['Risk Score']),
        use_container_width=True
    )

with tab2:
    st.subheader("⛽ Fuel Efficiency Analysis")
    
    efficiency_analyzer = FuelEfficiencyAnalyzer()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Current Efficiency", "12.5 km/l", "+0.5 km/l")
        st.metric("Efficiency Score", "85/100", "Good")
    
    with col2:
        st.metric("Fuel Consumed (Today)", "15.3 L", "+2.1 L")
        st.metric("Cost Estimate", "$1,530", "+$210")
    
    st.divider()
    
    # Trip planning
    st.subheader("🛣️ Trip Fuel Planning")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        planned_distance = st.number_input("Planned Distance (km)", 100, 1000, 250)
    with col2:
        current_fuel = st.number_input("Current Fuel (L)", 0, 100, 50)
    with col3:
        avg_efficiency = st.number_input("Avg Efficiency (km/L)", 8.0, 20.0, 12.5)
    
    # Calculate fuel needs
    fuel_needed = planned_distance / avg_efficiency
    fuel_remaining = current_fuel - fuel_needed
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fuel Needed", f"{fuel_needed:.1f} L")
    with col2:
        status_color = "🟢" if fuel_remaining > 5 else "🟡" if fuel_remaining > 0 else "🔴"
        st.metric("Fuel Remaining", f"{fuel_remaining:.1f} L", status_color)

with tab3:
    st.subheader("📈 Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(engine_temperature_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(battery_health_chart(), use_container_width=True)
    
    # Performance table
    st.subheader("Performance Summary")
    
    performance_data = {
        'Metric': ['Acceleration (0-100 km/h)', 'Max Speed', 'Braking Distance', 'Turning Radius'],
        'Current': ['8.5 sec', '185 km/h', '42 m', '5.2 m'],
        'Optimal': ['8.2 sec', '195 km/h', '40 m', '5.0 m'],
        'Status': ['Good', 'Good', 'Good', 'Good']
    }
    
    st.dataframe(pd.DataFrame(performance_data), use_container_width=True)

with tab4:
    st.subheader("📊 Trend Analysis")
    
    # Time range selector
    time_range = st.selectbox("Time Range", ["7 Days", "30 Days", "90 Days", "1 Year"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📈 Efficiency Trend")
        st.metric("Average", "12.2 km/l", "+1.2%")
    
    with col2:
        st.info("⚙️ Engine Health Trend")
        st.metric("Temperature", "82°C", "-3°C")
    
    # Trend visualization
    import plotly.graph_objects as go
    
    dates = pd.date_range('2024-06-01', periods=30)
    efficiency = np.cumsum(np.random.randn(30) * 0.5) + 12
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=efficiency, mode='lines+markers', name='Efficiency'))
    fig.update_layout(title="30-Day Efficiency Trend", xaxis_title="Date", yaxis_title="km/l", height=400)
    
    st.plotly_chart(fig, use_container_width=True)
