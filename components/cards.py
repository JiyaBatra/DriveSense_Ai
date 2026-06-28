import streamlit as st

def metric_card(title, value, label, icon="📊"):
    """Render a metric card"""
    col = st.container()
    with col:
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="margin: 0; color: #666;">{icon} {title}</h3>
            <h1 style="margin: 10px 0; color: #1f77b4;">{value}</h1>
            <p style="margin: 0; color: #999;">{label}</p>
        </div>
        """, unsafe_allow_html=True)

def status_card(title, status, percentage, icon="🚗"):
    """Render a status card with progress"""
    color = "#00cc96" if status == "Good" else "#ff6692" if status == "Warning" else "#636EFA"
    
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #333;">{icon} {title}</h4>
                <p style="margin: 5px 0; color: {color}; font-weight: bold;">{status}</p>
            </div>
            <div style="font-size: 24px; font-weight: bold; color: {color};">{percentage}%</div>
        </div>
        <div style="background-color: #ddd; height: 8px; border-radius: 4px; margin-top: 10px; overflow: hidden;">
            <div style="background-color: {color}; height: 100%; width: {percentage}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def alert_card(alert_type, severity, message, timestamp):
    """Render an alert card"""
    color_map = {
        "Critical": "#ff6692",
        "High": "#ff9e64",
        "Medium": "#ffc107",
        "Low": "#00cc96"
    }
    color = color_map.get(severity, "#636EFA")
    
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin: 10px 0; 
                border-left: 5px solid {color};">
        <div style="display: flex; justify-content: space-between;">
            <div>
                <h4 style="margin: 0; color: {color};">{alert_type}</h4>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">{message}</p>
            </div>
            <div style="text-align: right; color: #999; font-size: 12px;">
                <div>{severity}</div>
                <div>{timestamp}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
