# DriveSense AI - Development Guide

## 📋 Project Overview

DriveSense_AI is a comprehensive AI-powered smart vehicle monitoring system built with Streamlit, designed to enhance road safety, improve vehicle reliability, and enable intelligent transportation.

### Key Objectives
- **Predictive Maintenance**: ML-based vehicle failure prediction
- **Driver Safety**: Real-time drowsiness and distraction detection
- **Traffic Sign Recognition**: YOLOv8-based computer vision
- **Fleet Management**: Centralized monitoring and analytics
- **Intelligent Alerts**: Real-time safety notifications

---

## 🏗️ Project Architecture

```
DriveSense_AI/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
│
├── pages/                          # Multi-page Streamlit apps
│   ├── 1_Advanced_Analytics.py      # Predictive analysis dashboard
│   ├── 2_Real_Time_Monitoring.py    # Fleet monitoring dashboard
│   └── 3_Driver_Analysis.py         # Driver behavior analysis
│
├── components/                     # UI components
│   ├── sidebar.py                  # Navigation sidebar
│   ├── cards.py                    # Metric and status cards
│   ├── charts.py                   # Plotly visualizations
│   ├── alerts.py                   # Alert display components
│   └── camera.py                   # Camera feed components
│
├── utils/                          # Core business logic
│   ├── data.py                     # Sample data generation
│   ├── prediction.py               # Maintenance prediction model
│   ├── traffic_detection.py        # Traffic sign & lane detection
│   ├── driver_monitoring.py        # Driver behavior & drowsiness detection
│   └── vehicle_health.py           # Vehicle sensor monitoring
│
└── .streamlit/                     # Streamlit configuration
    └── config.toml                 # Theme and server settings
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip or conda
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/JiyaBatra/DriveSense_Ai.git
cd DriveSense_Ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web framework |
| opencv-python | 4.8.1.78 | Computer vision |
| numpy | 1.24.3 | Numerical operations |
| pandas | 2.1.1 | Data processing |
| plotly | 5.17.0 | Interactive charts |
| scikit-learn | 1.3.2 | ML algorithms |
| pillow | 10.0.1 | Image processing |
| scipy | 1.11.3 | Scientific computing |
| torch | 2.0.1 | Deep learning |
| torchvision | 0.15.2 | Computer vision models |
| ultralytics | 8.0.200 | YOLOv8 |

---

## 🎯 Core Features & Modules

### 1. **Main Dashboard** (`app.py`)

**Purpose**: Central hub displaying vehicle health, maintenance status, and alerts

**Key Components**:
- Top metrics: Vehicles online, maintenance due, drowsy drivers, violations, alerts
- Vehicle health doughnut chart
- Maintenance trend line chart
- Driver status distribution
- Weekly alerts trend
- Traffic violations pie chart
- Recent alerts display

**Navigation Menu**:
- 🏠 Dashboard
- 🚗 Vehicle Health
- 🛠 Maintenance
- 👤 Driver Monitoring
- 🚦 Traffic Signs
- 📷 Live Cameras
- 🔔 Alerts
- 📄 Reports
- ⚙️ Settings

---

### 2. **Predictive Maintenance** (`utils/vehicle_health.py`)

**Class**: `MaintenancePredictionModel`

**Features**:
- Component risk calculation
- Remaining Useful Life (RUL) estimation
- Maintenance schedule prediction
- Critical component identification

**Components Monitored**:
- Engine
- Battery
- Brakes
- Transmission
- Suspension

**Risk Factors**:
- Mileage
- Age/Time in service
- Operating temperature
- Usage patterns

**Example Usage**:
```python
from utils.vehicle_health import MaintenancePredictionModel

model = MaintenancePredictionModel()

vehicle_data = {
    'mileage': 85000,
    'age_days': 1200,
    'engine_temp': 85
}

prediction = model.predict_maintenance_schedule(vehicle_data)
print(prediction['critical_components'])  # ['Engine', 'Battery']
```

---

### 3. **Driver Drowsiness Detection** (`utils/driver_monitoring.py`)

**Classes**:
- `FaceDetector`: Detects driver face in camera feed
- `EyeDetector`: Detects eyes and calculates Eye Aspect Ratio (EAR)
- `HeadPoseEstimator`: Estimates head position and gaze
- `DriverBehaviorAnalyzer`: Comprehensive behavior analysis

**Drowsiness Detection Algorithm**:

Eye Aspect Ratio (EAR) Formula:
```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
```

Where p1-p6 are eye landmark points

**Thresholds**:
- EAR < 0.2: Eyes closed (drowsy)
- 5 consecutive frames below threshold: Drowsiness alert

**Drowsiness Score (0-100)**:
```
score = (0.3 - EAR) * 333
```

**Example Usage**:
```python
from utils.driver_monitoring import EyeDetector, DriverBehaviorAnalyzer

detector = EyeDetector()
analyzer = DriverBehaviorAnalyzer()

# Detect drowsiness
ear = 0.25
state = detector.update_drowsiness_state(ear)
drowsiness_score = analyzer.calculate_drowsiness_score(ear)

if drowsiness_score > 70:
    print("CRITICAL DROWSINESS ALERT!")
```

---

### 4. **Traffic Sign Detection** (`utils/traffic_detection.py`)

**Class**: `TrafficSignDetector`

**Supported Signs**:
- Speed Limit (30, 60, 90)
- Stop Sign
- No Entry
- Traffic Signal (Red/Green)
- Warning Signs (Curve, Pedestrian, Construction)

**Features**:
- YOLOv8-based detection
- Confidence filtering
- Severity classification
- Violation reporting

**Example Usage**:
```python
from utils.traffic_detection import TrafficSignDetector

detector = TrafficSignDetector(confidence_threshold=0.5)

# In production, would use actual camera feed
detections = detector.detect_signs(frame)

for detection in detections:
    print(f"{detection['class_name']}: {detection['confidence']:.2%}")
```

---

### 5. **Vehicle Health Monitoring** (`utils/vehicle_health.py`)

**Class**: `VehicleSensorMonitor`

**Monitored Sensors**:
- Engine Temperature
- Battery Health
- Fuel Level
- Engine RPM
- Vibration Analysis
- Oil Pressure
- Coolant Level

**Alert Thresholds**:
```python
{
    'engine_temp': {'warning': 90, 'critical': 100},
    'battery_health': {'warning': 30, 'critical': 10},
    'fuel_level': {'warning': 15, 'critical': 5},
    'engine_rpm': {'warning': 5500, 'critical': 6500},
    'vibration': {'warning': 3, 'critical': 4}
}
```

**Example Usage**:
```python
from utils.vehicle_health import VehicleSensorMonitor

monitor = VehicleSensorMonitor()
sensors = monitor.read_sensors('VEH-001')
report = monitor.generate_sensor_report(sensors)
```

---

### 6. **Fuel Efficiency Analysis** (`utils/vehicle_health.py`)

**Class**: `FuelEfficiencyAnalyzer`

**Features**:
- Real-time consumption tracking
- Efficiency scoring based on driving patterns
- Fuel prediction for trips
- Cost estimation

**Efficiency Penalties**:
- High speed (>100 km/h): -20 points
- Aggressive acceleration (>2 m/s²): -30 points
- Cold engine (<50°C): -10 points

**Example Usage**:
```python
from utils.vehicle_health import FuelEfficiencyAnalyzer

analyzer = FuelEfficiencyAnalyzer()

# Plan trip
fuel_plan = analyzer.predict_fuel_needed(
    planned_distance_km=250,
    avg_efficiency_kml=12.5,
    reserve_fuel_liters=5
)

print(f"Fuel needed: {fuel_plan['fuel_needed']} L")
print(f"Recommendation: {fuel_plan['recommendation']}")
```

---

## 📊 Analytics Pages

### Advanced Analytics (`pages/1_Advanced_Analytics.py`)

**Sections**:
1. **Predictive Maintenance Analysis**
   - Overall risk score
   - Component health breakdown
   - Service timeline

2. **Fuel Efficiency Analysis**
   - Current efficiency metrics
   - Trip fuel planning
   - Cost estimation

3. **Performance Metrics**
   - Engine temperature chart
   - Battery health chart
   - Performance summary

4. **Trend Analysis**
   - 30-day efficiency trend
   - Engine health tracking
   - Comparative analysis

---

### Real-Time Monitoring (`pages/2_Real_Time_Monitoring.py`)

**Features**:
- Live vehicle status dashboard
- Real-time alert feed
- Fleet speed distribution
- GPS location mapping
- Network status monitoring

---

### Driver Analysis (`pages/3_Driver_Analysis.py`)

**Sections**:
1. **Live Monitoring**
   - Camera feed
   - Eye detection metrics
   - EAR tracking

2. **Behavior Analysis**
   - Speeding incidents
   - Harsh acceleration/braking
   - Distraction events
   - Risk factor assessment

3. **Safety Report**
   - Trip statistics
   - Safety score calculation
   - Safety recommendations

4. **Trip History**
   - Historical trip data
   - Safety score trends
   - Monthly analysis

---

## 🔧 Customization Guide

### Adding New Sensors

1. Update `utils/vehicle_health.py`:
```python
self.alert_thresholds[new_sensor_name] = {
    'warning': warning_threshold,
    'critical': critical_threshold
}
```

2. Add to `read_sensors()` method

### Adding New Alert Types

1. Update alert types in relevant module
2. Add severity mapping
3. Implement alert generation logic
4. Update alert display in UI

### Integrating Real Camera Feeds

```python
import cv2

def connect_camera():
    cap = cv2.VideoCapture(0)  # 0 for default camera
    
    while True:
        ret, frame = cap.read()
        if ret:
            # Process frame with detection models
            yield frame
        else:
            break
    
    cap.release()
```

### Implementing YOLOv8

```python
from ultralytics import YOLO

model = YOLO('yolov8m.pt')

def detect_traffic_signs(frame):
    results = model(frame)
    return results
```

---

## 🧪 Testing

### Unit Testing Structure

```python
# tests/test_drowsiness_detector.py
import pytest
from utils.driver_monitoring import EyeDetector

def test_ear_calculation():
    detector = EyeDetector()
    # Test implementation
    assert detector.calculate_eye_aspect_ratio(...) > 0

def test_drowsiness_detection():
    detector = EyeDetector()
    state = detector.update_drowsiness_state(0.15)
    assert state['is_drowsy'] == True
```

---

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app.py --server.port 8501
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t drivesense-ai .
docker run -p 8501:8501 drivesense-ai
```

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect repository and select `app.py`

---

## 📈 Performance Optimization

### Image Processing
- Use resolution reduction for real-time processing
- Implement frame skipping for non-critical analysis
- Cache model predictions when possible

### Database Optimization
- Index frequently queried columns
- Implement data archival for old records
- Use connection pooling

### UI Performance
- Lazy load heavy components
- Use session caching for expensive computations
- Implement pagination for large datasets

---

## 🔒 Security Considerations

- Validate all user inputs
- Sanitize data before storage
- Implement authentication for sensitive data
- Use HTTPS for cloud deployment
- Encrypt stored video feeds and sensor data

---

## 📝 Logging & Monitoring

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

---

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Commit changes: `git commit -m "Add new feature"`
3. Push to branch: `git push origin feature/new-feature`
4. Create Pull Request

---

## 📞 Support & Resources

- **Documentation**: `/DEVELOPMENT.md`
- **README**: `/README.md`
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

## 📄 License

This project is part of the TCS Mobility Solutions initiative for smart vehicle monitoring.

---

**Last Updated**: June 28, 2024  
**Version**: 1.0.0  
**Status**: Active Development
