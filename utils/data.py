import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_vehicle_data():
    """Generate sample vehicle sensor data"""
    vehicles = ['VEH-001', 'VEH-002', 'VEH-003', 'VEH-004', 'VEH-005']
    
    data = {
        'Vehicle_ID': vehicles * 12,
        'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(60)] * 1,
        'Engine_Temp': np.random.randint(60, 100, 60),
        'Battery_Health': np.random.randint(70, 100, 60),
        'Fuel_Level': np.random.randint(10, 100, 60),
        'Engine_RPM': np.random.randint(800, 5000, 60),
        'Vibration': np.random.uniform(0, 5, 60),
        'Status': np.random.choice(['Normal', 'Warning', 'Critical'], 60)
    }
    
    return pd.DataFrame(data)

def generate_maintenance_data():
    """Generate predictive maintenance data"""
    data = {
        'Vehicle_ID': ['VEH-001', 'VEH-002', 'VEH-003', 'VEH-004', 'VEH-005'],
        'Risk_Score': [0.25, 0.65, 0.15, 0.85, 0.45],
        'Maintenance_Due': ['120 days', '7 days', '200 days', 'Urgent', '60 days'],
        'RUL': ['Good', 'Critical', 'Excellent', 'Failed', 'Good'],
        'Failure_Prob': ['5%', '92%', '2%', '99%', '18%'],
        'Recommendation': ['Routine Check', 'Immediate Service', 'Oil Change', 'Emergency Repair', 'Brake Inspection']
    }
    
    return pd.DataFrame(data)

def generate_driver_data():
    """Generate driver monitoring data"""
    data = {
        'Vehicle_ID': ['VEH-001', 'VEH-002', 'VEH-003', 'VEH-004', 'VEH-005'],
        'Driver_Name': ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Emma Wilson', 'David Brown'],
        'Drowsiness_Score': [15, 42, 8, 78, 25],
        'Alert_Count': [2, 15, 1, 31, 5],
        'Status': ['Alert', 'Drowsy', 'Alert', 'Very Drowsy', 'Alert'],
        'Last_Alert': ['2 min ago', '30 sec ago', '15 min ago', '5 sec ago', '8 min ago']
    }
    
    return pd.DataFrame(data)

def generate_traffic_violation_data():
    """Generate traffic violation data"""
    violations = ['Speed Limit', 'Stop Sign', 'Red Light', 'No Entry', 'Warning Sign']
    data = {
        'Violation_Type': violations,
        'Count': [45, 12, 8, 3, 15],
        'Severity': ['Medium', 'High', 'High', 'Critical', 'Medium']
    }
    
    return pd.DataFrame(data)

def generate_alert_data():
    """Generate alert history data"""
    alert_types = ['Driver Drowsiness', 'Maintenance Warning', 'Speed Exceeded', 
                   'Engine Overheat', 'Battery Warning', 'Emergency']
    data = {
        'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(24)],
        'Alert_Type': np.random.choice(alert_types, 24),
        'Vehicle_ID': np.random.choice(['VEH-001', 'VEH-002', 'VEH-003', 'VEH-004', 'VEH-005'], 24),
        'Severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 24),
        'Status': np.random.choice(['New', 'Acknowledged', 'Resolved'], 24)
    }
    
    return pd.DataFrame(data)

def get_vehicle_stats():
    """Get overall vehicle statistics"""
    return {
        'Total_Vehicles': 5,
        'Vehicles_Online': 5,
        'Maintenance_Due': 2,
        'Drowsy_Drivers': 2,
        'Traffic_Violations': 83,
        'Total_Alerts': 24
    }
