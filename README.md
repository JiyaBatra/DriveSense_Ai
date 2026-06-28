**DriveSense_AI** is an AI-powered smart vehicle monitoring system built from a TCS mobility solutions perspective. It combines predictive maintenance, driver drowsiness detection, traffic sign recognition, and a Streamlit dashboard to improve road safety, reduce vehicle failures, and enable intelligent transportation.


DriveSense-AI/
│
├── app.py
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Vehicle_Health.py
│   ├── 3_Driver_Monitoring.py
│   ├── 4_Traffic_Signs.py
│   ├── 5_Live_Camera.py
│   └── 6_Reports.py
│
├── components/
│   ├── sidebar.py
│   ├── cards.py
│   ├── charts.py
│   ├── alerts.py
│   └── camera.py
│
├── assets/
│   ├── truck.png
│   ├── driver.jpg
│   └── road.jpg
│
├── utils/
│   ├── data.py
│   └── prediction.py
│
└── requirements.txt

Dashboard Layout

---------------------------------------------------------
 Sidebar | Vehicles | Maintenance | Driver | Traffic | Alert
---------------------------------------------------------
 Vehicle Health      Maintenance Prediction   Driver Status
---------------------------------------------------------
 Live Cameras        Traffic Sign Detection   Recent Alerts
---------------------------------------------------------
 Alerts Trend        Violations Chart         System Insights
---------------------------------------------------------

Technologies

Streamlit

Plotly

OpenCV

YOLOv8

Pandas

NumPy


Features

✅ Vehicle Health Monitoring

Engine Temperature

Battery

Fuel

RPM

Vibration



---

✅ Predictive Maintenance

Risk Score

Maintenance Due

Remaining Useful Life



---

✅ Driver Monitoring

Driver Camera

Eye Detection

EAR

Drowsiness Status

Alert



---

✅ Traffic Sign Detection

Road Camera

YOLO Detection

Speed Limit

Stop Sign

Confidence Score



---

✅ Live Camera Feed

Front Camera

Driver Camera

Rear Camera

Road Camera



---

✅ Alerts

Driver Sleeping

Maintenance Warning

Speed Limit Exceeded

Emergency Alerts



---

Charts

Vehicle Health Doughnut Chart

Maintenance Prediction Line Chart

Driver Status Doughnut Chart

Weekly Alerts Graph

Traffic Violations Pie Chart



---

Sidebar

🚛 DriveSense AI

🏠 Dashboard

🚗 Vehicle Health

🛠 Maintenance

👤 Driver Monitoring

🚦 Traffic Signs

📷 Live Cameras

🔔 Alerts

📄 Reports

⚙ Settings

Top Cards

Vehicles Online

Maintenance Due

Driver Drowsy

Traffic Violations

Total Alerts

Project Size

The complete Streamlit prototype (frontend + dummy backend + charts + navigation + responsive UI) will be around 2,000–3,000 lines of Python code.

It will closely match the reference dashboard while implementing your project flow:

Vehicle sensor analytics

Predictive maintenance

Driver drowsiness detection

Traffic sign recognition

Centralized decision & alert system

Real-time monitoring dashboard


This would be a polished prototype suitable for a final-year project or presentation.