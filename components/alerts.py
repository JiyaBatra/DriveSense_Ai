import streamlit as st
import pandas as pd

def display_alerts(alerts_df):
    """Display alerts in a formatted table"""
    if alerts_df.empty:
        st.info("No alerts to display")
        return
    
    # Color code severity
    def severity_color(severity):
        colors = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }
        return colors.get(severity, '⚪')
    
    # Color code status
    def status_badge(status):
        badges = {
            'New': '🆕',
            'Acknowledged': '👁️',
            'Resolved': '✅'
        }
        return badges.get(status, '❓')
    
    for idx, row in alerts_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        
        with col1:
            st.write(severity_color(row['Severity']))
        
        with col2:
            st.write(f"**{row['Alert_Type']}**")
            st.caption(f"{row['Vehicle_ID']}")
        
        with col3:
            st.write(row['Severity'])
        
        with col4:
            st.write(status_badge(row['Status']))
        
        with col5:
            st.write(row['Timestamp'].strftime('%H:%M'))
        
        st.divider()

def alert_summary(stats):
    """Display alert summary statistics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 Critical", stats.get('critical', 0))
    
    with col2:
        st.metric("🟠 High", stats.get('high', 0))
    
    with col3:
        st.metric("🟡 Medium", stats.get('medium', 0))
    
    with col4:
        st.metric("🟢 Low", stats.get('low', 0))

def filter_alerts(alerts_df):
    """Display alert filters"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        alert_type = st.multiselect(
            "Alert Type",
            alerts_df['Alert_Type'].unique(),
            default=alerts_df['Alert_Type'].unique()
        )
    
    with col2:
        severity = st.multiselect(
            "Severity",
            ['Critical', 'High', 'Medium', 'Low'],
            default=['Critical', 'High', 'Medium', 'Low']
        )
    
    with col3:
        status = st.multiselect(
            "Status",
            alerts_df['Status'].unique(),
            default=alerts_df['Status'].unique()
        )
    
    # Filter dataframe
    filtered_df = alerts_df[
        (alerts_df['Alert_Type'].isin(alert_type)) &
        (alerts_df['Severity'].isin(severity)) &
        (alerts_df['Status'].isin(status))
    ]
    
    return filtered_df
