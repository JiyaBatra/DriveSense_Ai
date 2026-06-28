# 🚀 DriveSense AI - Quick Start Guide

Get up and running with DriveSense AI in 5 minutes!

---

## ⚡ Quick Installation

### 1. **Clone & Setup**
```bash
git clone https://github.com/JiyaBatra/DriveSense_Ai.git
cd DriveSense_Ai
pip install -r requirements.txt
```

### 2. **Run the Application**
```bash
streamlit run app.py
```

### 3. **Open in Browser**
Navigate to: `http://localhost:8501`

---

## 📱 Application Features

### **Main Dashboard** (Default)
- 5 Key Metrics: Vehicles, Maintenance, Drowsy Drivers, Violations, Alerts
- Vehicle Health Status Chart
- Maintenance Trend Analysis
- Driver Alertness Distribution
- Weekly Alerts Trend
- Traffic Violations Breakdown
- Recent Alerts Feed

### **Navigation Menu** (Left Sidebar)
```
🏠 Dashboard                  → Main overview
🚗 Vehicle Health             → Real-time sensor data
🛠 Maintenance               → Predictive maintenance
👤 Driver Monitoring         → Drowsiness detection
🚦 Traffic Signs             → Traffic detection
📷 Live Cameras              → Camera feeds
🔔 Alerts                    → Alert management
📄 Reports                   → Analytics reports
⚙️ Settings                  → Configuration
```

### **Multi-Page Analytics**
1. **Advanced Analytics** - Predictive models & trend analysis
2. **Real-Time Monitoring** - Fleet status dashboard
3. **Driver Analysis** - Driver behavior & safety reports

---

## 🎮 Using the Dashboard

### **Vehicle Health Tab**
1. Select a vehicle from dropdown
2. View real-time sensor metrics
3. Check engine temperature chart
4. Monitor battery health status

### **Maintenance Tab**
1. View risk scores for each vehicle
2. Check maintenance recommendations
3. See remaining useful life (RUL)
4. Review predicted failure probability

### **Driver Monitoring Tab**
1. Select a driver
2. View drowsiness score (0-100)
3. Check alert history
4. See driver status indicators

### **Traffic Signs Tab**
1. View detected signs from camera
2. Check violation statistics
3. Review confidence scores
4. See detection timeline

### **Live Cameras Tab**
1. Select camera source (Front/Driver/Rear/Road)
2. Adjust brightness, contrast, saturation
3. Monitor live feed status
4. Check camera health metrics

### **Alerts Tab**
1. Filter by alert type
2. Filter by severity (Critical/High/Medium/Low)
3. Filter by status (New/Acknowledged/Resolved)
4. View alert timeline

---

## 📊 Sample Data

The application comes with **sample data for 5 vehicles**:
- **VEH-001** to **VEH-005**
- Mock sensor readings
- Simulated driver behavior
- Generated alerts and violations

### **Replace with Real Data**
Edit `utils/data.py`:
```python
def generate_vehicle_data():
    # Replace with actual sensor data source
    # Connect to database, API, or IoT platform
    pass
```

---

## 🔌 Integration Points

### **Database Connection**
```python
# In your data loading function
import sqlite3
conn = sqlite3.connect('vehicle_data.db')
vehicle_df = pd.read_sql('SELECT * FROM vehicles', conn)
```

### **Real Camera Feed**
```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
```

### **Real-Time Alerts**
```python
# Connect to message queue (Redis, RabbitMQ)
# Subscribe to alert topic
for alert in message_queue.listen('vehicle_alerts'):
    st.write(alert)
```

---

## ⚙️ Configuration

### **Streamlit Config** (`.streamlit/config.toml`)

**Theme Colors**:
```toml
primaryColor = "#636EFA"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

**Auto-Refresh Settings**:
```bash
streamlit run app.py --client.showErrorDetails=true
```

---

## 🧬 Core Modules

### **Main App** (`app.py`)
- Central dashboard with all visualizations
- Sidebar navigation
- Multi-tab interface

### **Components** (`components/`)
- `sidebar.py` - Navigation menu
- `cards.py` - Metric displays
- `charts.py` - Plotly visualizations
- `alerts.py` - Alert management
- `camera.py` - Camera utilities

### **Utilities** (`utils/`)
- `data.py` - Sample data generation
- `prediction.py` - ML prediction models
- `vehicle_health.py` - Sensor monitoring
- `driver_monitoring.py` - Drowsiness detection
- `traffic_detection.py` - Traffic sign detection

### **Pages** (`pages/`)
- `1_Advanced_Analytics.py` - Predictive analysis
- `2_Real_Time_Monitoring.py` - Fleet dashboard
- `3_Driver_Analysis.py` - Driver behavior

---

## 🎯 Key Metrics Explained

### **Vehicles Online**
Number of vehicles actively connected to the system

### **Maintenance Due**
Vehicles requiring maintenance based on predictive model

### **Drowsy Drivers**
Current number of drivers showing drowsiness signs

### **Traffic Violations**
Total violations detected (speeding, red light, etc.)

### **Total Alerts**
Count of all active and recent alerts

---

## 🚨 Alert System

### **Alert Types**
- 🔴 **Critical**: Emergency action required
- 🟠 **High**: Immediate attention needed
- 🟡 **Medium**: Monitor and address
- 🟢 **Low**: Informational only

### **Common Alerts**
- Driver Drowsiness
- Maintenance Warning
- Speed Limit Exceeded
- Engine Overheating
- Battery Warning
- Emergency Alerts

---

## 📈 Drowsiness Detection

**Algorithm**: Eye Aspect Ratio (EAR)
- Tracks eye closure over time
- Calculates drowsiness score (0-100)
- Triggers alerts at threshold (70+)

**Score Levels**:
- 0-30: Alert ✅ Normal
- 30-50: 🟡 Moderate Drowsiness
- 50-70: 🟠 High Drowsiness
- 70+: 🔴 Critical Drowsiness

---

## 🚗 Maintenance Prediction

**Components Analyzed**:
- Engine
- Battery
- Brakes
- Transmission
- Suspension

**Factors Considered**:
- Mileage
- Age/Time in service
- Operating temperature
- Usage patterns

---

## 🛑 Troubleshooting

### **App Not Starting**
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Missing Dependencies**
```bash
# Install specific package
pip install streamlit==1.28.1
```

### **Streamlit Cache Issues**
```bash
# Clear Streamlit cache
streamlit cache clear
```

---

## 📚 Next Steps

1. **Connect Real Data**: Update `utils/data.py` with actual data sources
2. **Add Camera Integration**: Implement real camera feed
3. **Enable Alerts**: Set up email/SMS notifications
4. **Deploy Cloud**: Push to Streamlit Cloud or AWS
5. **Customize Thresholds**: Adjust alert thresholds for your fleet

---

## 💡 Tips & Tricks

- **Auto-refresh**: Use F5 to refresh page
- **Filter Data**: Use sidebar filters to narrow down
- **Export Reports**: Use browser's print-to-PDF feature
- **Responsive Design**: Resize browser window for mobile view

---

## 🔗 Useful Links

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Charts**: https://plotly.com/python/
- **OpenCV**: https://opencv.org/
- **YOLOv8**: https://github.com/ultralytics/ultralytics
- **Scikit-learn**: https://scikit-learn.org/

---

## 📧 Support

For issues or questions:
- Check `DEVELOPMENT.md` for detailed documentation
- Review `README.md` for project overview
- Create GitHub issue with error details

---

**Happy Monitoring! 🚗✨**

Version: 1.0.0 | Last Updated: June 28, 2024
