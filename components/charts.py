import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def vehicle_health_chart(data):
    """Create vehicle health doughnut chart"""
    labels = ['Good', 'Warning', 'Critical']
    values = [45, 35, 20]
    colors = ['#00cc96', '#ffa500', '#ff6692']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=colors),
        textposition='inside',
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title="Vehicle Health Status",
        showlegend=True,
        height=400
    )
    
    return fig

def maintenance_trend_chart(data):
    """Create maintenance prediction trend chart"""
    fig = go.Figure()
    
    # Sample data
    dates = pd.date_range('2024-01-01', periods=30)
    risk_scores = pd.Series([i/30 + (i%3)*0.1 for i in range(30)], index=dates)
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=risk_scores,
        mode='lines+markers',
        name='Risk Score',
        line=dict(color='#ff6692', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Maintenance Risk Trend (30 Days)",
        xaxis_title="Date",
        yaxis_title="Risk Score",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def driver_status_chart(data):
    """Create driver status doughnut chart"""
    labels = ['Alert', 'Normal', 'Drowsy', 'Very Drowsy']
    values = [2, 2, 0, 1]
    colors = ['#00cc96', '#636EFA', '#ffa500', '#ff6692']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=colors),
        textposition='inside',
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title="Driver Alertness Status",
        showlegend=True,
        height=400
    )
    
    return fig

def alerts_trend_chart(data):
    """Create weekly alerts trend chart"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    alerts = [12, 18, 15, 22, 19, 16, 10]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=days,
        y=alerts,
        marker=dict(color='#636EFA'),
        text=alerts,
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Weekly Alerts Trend",
        xaxis_title="Day",
        yaxis_title="Alert Count",
        height=400,
        showlegend=False
    )
    
    return fig

def traffic_violations_chart(data):
    """Create traffic violations pie chart"""
    labels = ['Speed Limit', 'Stop Sign', 'Red Light', 'No Entry', 'Warning']
    values = [45, 12, 8, 3, 15]
    colors = ['#ff6692', '#ffa500', '#ffaa00', '#ff7f0e', '#d62728']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textposition='inside',
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title="Traffic Violations Distribution",
        height=400
    )
    
    return fig

def engine_temperature_chart():
    """Create engine temperature chart"""
    hours = list(range(24))
    temps = [70 + i*0.5 + (i%3)*2 for i in range(24)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=temps,
        mode='lines+markers',
        name='Temperature (°C)',
        line=dict(color='#ff6692', width=2),
        fill='tozeroy'
    ))
    
    fig.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Max Threshold")
    
    fig.update_layout(
        title="Engine Temperature (Last 24 Hours)",
        xaxis_title="Hour",
        yaxis_title="Temperature (°C)",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def battery_health_chart():
    """Create battery health chart"""
    vehicles = ['VEH-001', 'VEH-002', 'VEH-003', 'VEH-004', 'VEH-005']
    health = [95, 78, 88, 72, 92]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=vehicles,
        y=health,
        marker=dict(color=health, colorscale='RdYlGn', showscale=True),
        text=[f"{h}%" for h in health],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Battery Health by Vehicle",
        xaxis_title="Vehicle ID",
        yaxis_title="Health (%)",
        height=400
    )
    
    return fig
