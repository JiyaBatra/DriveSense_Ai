# DriveSense AI

**DriveSense AI** is an AI-powered driver-assistance project that makes driving safer by combining computer vision and machine learning in a single system. It monitors the driver, the road, and the vehicle itself, combines everything into one risk score, and sits behind a secure login/signup system.

## Features

| # | Feature | Technique | Status |
|---|---------|-----------|--------|
| 1 | Drowsiness Detection | CNN + Haar Cascade | Completed |
| 2 | Road & Lane Detection | Classical computer vision (Canny + Hough) | Completed |
| 3 | Vehicle Health Prediction | Random Forest on engine sensor data | Completed |
| 4 | Accident Risk Alert | Combined risk score from all modules | Completed |
| 5 | Login / Signup | User authentication | Completed |

## System Overview

```mermaid
flowchart LR
    U[User] --> L[Login / Signup]
    L --> A[Webcam<br/>driver face]
    L --> C[Road camera<br/>frames]
    L --> E[Engine sensors<br/>RPM, pressure, temperature]
    A --> B[Drowsiness<br/>Detection]
    C --> D[Lane<br/>Detection]
    E --> F[Vehicle Health<br/>Prediction]
    B --> G[Accident Risk Alert]
    D --> G
    F --> G
    G --> H[Driver warning]
```

## App Screenshots

The whole system runs as a Streamlit web app with a sidebar to switch between modules.

| Login / Sign Up | Dashboard |
|:---:|:---:|
| ![Login](assets/DriveSense_AI__localhost_8501__-_Drivesense_ai_-_Visual_Studio_Code_07-10-2026_11_54_12.png) | ![Dashboard](assets/DriveSense_AI__localhost_8501__-_Drivesense_ai_-_Visual_Studio_Code_07-10-2026_11_54_31.png) |

![Dashboard modules](assets/DriveSense_AI__localhost_8501__-_Drivesense_ai_-_Visual_Studio_Code_07-10-2026_11_54_37.png)

---

## Feature 1: Drowsiness Detection

Detects in real time whether the driver is **awake** or **sleepy** using a webcam. If the driver stays sleepy for more than **2 seconds**, a **DROWSINESS ALERT** is shown on screen.

### Demo

![Drowsiness Detection Demo](assets/drowsiness_demo.png)

*Live webcam feed: the face is detected (blue box) and classified as Awake/Sleepy with a confidence score.*

![Drowsiness Detection in the app](assets/DriveSense_AI__localhost_8501__-_Drivesense_ai_-_Visual_Studio_Code_07-10-2026_11_55_08.png)

*Drowsiness Detection page inside the app: the driver is detected and labelled Awake (100%).*

### How It Works (Flow Chart)

```mermaid
flowchart TD
    A([Start]) --> B[Load trained CNN model<br/>drowsiness_model.keras]
    B --> C[Load Haar Cascade<br/>face detector]
    C --> D[Open webcam]
    D --> E[Read frame and mirror it]
    E --> F[Convert frame to grayscale]
    F --> G{Face detected?}
    G -- No --> H[Reset sleepy timer] --> N
    G -- Yes --> I[Draw box and crop face]
    I --> J[Resize to 64x64<br/>BGR to RGB]
    J --> K[CNN predicts probability]
    K --> L{Probability >= 0.5?}
    L -- No --> M[Label: Awake<br/>Reset sleepy timer] --> N
    L -- Yes --> O[Label: Sleepy<br/>Start / continue timer]
    O --> P{Sleepy for >= 2 sec?}
    P -- Yes --> Q[Show DROWSINESS ALERT]
    P -- No --> N
    Q --> N[Display frame with label and confidence]
    N --> R{Q key pressed?}
    R -- No --> E
    R -- Yes --> S[Release camera and close windows]
    S --> T([End])
```

### Model Training Pipeline

```mermaid
flowchart LR
    A[Dataset<br/>train / val / test] --> B[image_dataset_from_directory<br/>64x64, batch 64]
    B --> C[CNN training<br/>Adam + binary crossentropy]
    C --> D[EarlyStopping +<br/>ModelCheckpoint]
    D --> E[Evaluate on test set<br/>report + confusion matrix]
    E --> F[Save drowsiness_model.keras]
```

### Model Architecture

| Layer | Details |
|-------|---------|
| Input | 64 × 64 × 3 image |
| Rescaling | Pixels normalized to 0–1 |
| Augmentation | RandomFlip (horizontal), RandomRotation (0.03) |
| Conv2D + MaxPooling | 16 filters, 3×3, ReLU |
| Conv2D + MaxPooling | 32 filters, 3×3, ReLU |
| Conv2D + MaxPooling | 64 filters, 3×3, ReLU |
| GlobalAveragePooling2D | Replaces Flatten to keep parameters low |
| Dense | 64 units, ReLU |
| Dropout | 0.4 |
| Output | Dense(1), Sigmoid (0 = Awake, 1 = Sleepy) |

**Training setup:** Adam optimizer, binary cross-entropy loss, up to 8 epochs, EarlyStopping (patience 2, restores best weights), and ModelCheckpoint saving the best model by validation accuracy.

### Results

| Metric | Value |
|--------|-------|
| Test Accuracy | _xx.x%_ |
| Test Loss | _x.xxx_ |

---

## Feature 2: Road & Lane Detection

Detects the left and right lane boundaries on a road image or a live camera feed and overlays them on the frame. The implementation uses classical computer vision (no training required), which keeps it light enough to run on a laptop without a GPU.

**Capabilities**

- Lane detection on single images
- Live webcam lane detection
- Left and right lane overlay (blue / green)
- Lane position output, used by the Accident Risk Alert module

### How It Works (Flow Chart)

```mermaid
flowchart TD
    A([Start]) --> B[Read image or webcam frame]
    B --> C[Resize to 640 px width<br/>for low laptop load]
    C --> D[Convert to grayscale]
    D --> E[Gaussian blur 5x5]
    E --> F[Canny edge detection<br/>thresholds 50 and 150]
    F --> G[Apply region of interest<br/>trapezoid mask on the road area]
    G --> H[Hough transform<br/>HoughLinesP]
    H --> I{Lines found?}
    I -- No --> N
    I -- Yes --> J[Compute slope of each line]
    J --> K{Slope magnitude < 0.5?}
    K -- Yes --> L[Ignore near-horizontal line]
    K -- No --> M{Slope negative?}
    M -- Yes --> M1[Left lane lines]
    M -- No --> M2[Right lane lines]
    L --> J
    M1 --> O[Fit one line per side<br/>np.polyfit]
    M2 --> O
    O --> P[Draw left lane in blue<br/>right lane in green]
    P --> N[Add label and display frame]
    N --> R{Q key pressed?}
    R -- No --> B
    R -- Yes --> S[Release camera and close windows]
    S --> T([End])
```

### Pipeline Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Resize width | 640 px | Reduce compute load |
| Gaussian kernel | 5 × 5 | Remove noise before edge detection |
| Canny thresholds | 50 / 150 | Edge sensitivity |
| Region of interest | Trapezoid (bottom of frame up to 55% height) | Focus on the road ahead |
| Hough threshold / min length / max gap | 40 / 40 / 100 | Line detection sensitivity |
| Slope filter | abs(slope) ≥ 0.5 | Discard horizontal edges |

---

## Feature 3: Vehicle Health Prediction

Predicts whether an engine is **healthy** or has a **fault** from six sensor readings, then produces a readable report: condition, status, health score, model confidence, and maintenance recommendations.

### Demo

![Vehicle Health Demo](assets/vehicle_health.gif)

*Demo recording of the vehicle health prediction running on sample sensor inputs.*

![Vehicle Health page](assets/Captures_-_File_Explorer_07-10-2026_11_57_30.png)

*Vehicle Health page inside the app: enter the six engine sensor values and get the engine condition.*

### Input Sensors

| Sensor | Description |
|--------|-------------|
| Engine rpm | Engine speed |
| Lub oil pressure | Lubrication oil pressure |
| Fuel pressure | Fuel line pressure |
| Coolant pressure | Cooling system pressure |
| lub oil temp | Lubrication oil temperature |
| Coolant temp | Coolant temperature |

### How It Works (Flow Chart)

```mermaid
flowchart TD
    A([Start]) --> B[Load engine_health_model.pkl<br/>and engine_health_scaler.pkl]
    B --> C[Receive 6 sensor values]
    C --> D[Arrange values in training order]
    D --> E[Scale with StandardScaler]
    E --> F[Random Forest predicts<br/>engine condition]
    F --> G[Get prediction probability<br/>as confidence]
    G --> H{Prediction = 1?}
    H -- Yes --> I[Condition: Healthy<br/>Status: Normal]
    H -- No --> J[Condition: Fault Detected<br/>Status: Warning]
    I --> K[Calculate health score]
    J --> K
    K --> L[Generate maintenance<br/>recommendations]
    L --> M[Return report:<br/>condition, status, score,<br/>confidence, recommendations]
    M --> N([End])
```

### Model Training Pipeline

```mermaid
flowchart LR
    A[engine_data.csv] --> B[Data checks<br/>missing values, duplicates,<br/>class balance]
    B --> C[Select 6 sensor features]
    C --> D[Stratified split<br/>80% train / 20% test]
    D --> E[StandardScaler<br/>fit on train only]
    E --> F[Random Forest<br/>200 trees, balanced class weights]
    F --> G[Evaluate<br/>accuracy, report, confusion matrix,<br/>feature importance]
    G --> H[Save model and scaler<br/>with joblib]
```

### Health Score Logic

The health score starts at **100** and rule-based penalties are applied for out-of-range readings. An additional penalty is applied when the model detects a fault. The score is kept between 0 and 100.

| Condition | Penalty |
|-----------|---------|
| Engine RPM above 3500 / above 4000 | −5 / −10 |
| Oil pressure below 2.5 / below 2 | −10 / −20 |
| Coolant temperature above 100 / above 105 | −10 / −20 |
| Oil temperature above 100 / above 110 | −8 / −15 |
| Coolant pressure below 1.5 | −10 |
| Model predicts a fault | −15 |

### Example Output

```python
predict_vehicle_health(
    engine_rpm=750,
    oil_pressure=3.2,
    fuel_pressure=6.5,
    coolant_pressure=2.4,
    oil_temperature=80,
    coolant_temperature=78
)
# {
#   "condition": "Healthy",
#   "status": "Normal",
#   "health_score": 100,
#   "confidence": <model confidence in %>,
#   "recommendation": ["Engine parameters are within the expected range. Continue regular monitoring."]
# }
```

### Results

| Metric | Value |
|--------|-------|
| Test Accuracy | _xx.x%_ |
| Weighted F1-score | _x.xx_ |

---

## Feature 4: Accident Risk Alert

Combines the outputs of all modules into a single risk score and warns the driver in real time.

```mermaid
flowchart LR
    A[Drowsiness state] --> D[Risk scoring<br/>engine]
    B[Lane position] --> D
    C[Vehicle health score] --> D
    D --> E{Risk level}
    E -- Low --> F[Normal driving]
    E -- Medium --> G[Visual warning]
    E -- High --> H[Visual and audio alarm]
```

| Risk level | Driver response |
|------------|-----------------|
| Low | Normal driving, no warning |
| Medium | On-screen visual warning |
| High | Visual warning and audio alarm |

---

## Feature 5: Login / Signup

Users create an account and log in before using the DriveSense AI modules, so each driver gets a secure, personal session.

**Capabilities**

- New user registration (signup)
- Login with registered credentials
- Input validation on both forms
- Passwords stored securely (hashed, never in plain text)
- Access to the detection modules only after a successful login

![Login and Sign Up](assets/DriveSense_AI__localhost_8501__-_Drivesense_ai_-_Visual_Studio_Code_07-10-2026_11_54_12.png)

```mermaid
flowchart TD
    A([Open app]) --> B{Has account?}
    B -- No --> C[Signup form]
    C --> D[Validate details]
    D --> E[Hash password and save user]
    E --> F[Login form]
    B -- Yes --> F
    F --> G{Credentials valid?}
    G -- No --> H[Show error] --> F
    G -- Yes --> I[Start session]
    I --> J[DriveSense AI dashboard<br/>Drowsiness, Lane, Vehicle Health, Risk Alert]
    J --> K[Logout]
    K --> A
```

---

## Tech Stack

- **Python 3.11**
- **TensorFlow / Keras**: CNN model for drowsiness detection
- **OpenCV**: webcam capture, Haar Cascade face detection, lane detection (Canny, Hough transform)
- **scikit-learn**: Random Forest, preprocessing, evaluation
- **joblib**: saving and loading the vehicle health model and scaler
- **NumPy, Pandas**: data handling
- **Matplotlib, Seaborn**: evaluation and visualization
- **Streamlit**: web app interface (sidebar navigation, dashboard, login/signup)
- **Authentication**: login/signup with hashed passwords

## Project Structure

```
Drivesense_ai/
├── archive (1)/data/             # drowsiness dataset
│   ├── train/                    # awake / sleepy images
│   ├── val/
│   └── test/
├── archive/                      # road lane dataset
│   ├── road_line_images/
│   └── road_line_annotation/
├── archive (2)/engine_data.csv   # engine sensor dataset
├── Drowsiness_Detection.ipynb    # training + real-time detection
├── Lane_Detection.ipynb          # lane detection
├── Vehicle_Health.ipynb          # vehicle health prediction
├── drowsiness_model.keras        # saved drowsiness model
├── engine_health_model.pkl       # saved vehicle health model
├── engine_health_scaler.pkl      # saved feature scaler
├── assets/
│   ├── drowsiness_demo.png
│   ├── vehicle_health.mp4
│   ├── vehicle_health.gif
│   └── (app screenshots, .png)
└── README.md
```

## How to Run

1. **Clone the repo**
```bash
git clone https://github.com/JiyaBatra/DriveSense_Ai.git
cd DriveSense_Ai
```
2. **Install dependencies**
```bash
pip install tensorflow opencv-python==4.10.0.84 numpy pandas matplotlib seaborn scikit-learn pillow joblib
```
3. **Start the app** with `streamlit run app.py`, open http://localhost:8501, then **sign up / log in**.
4. **Drowsiness detection:** train the model (or use the provided `drowsiness_model.keras`) in `Drowsiness_Detection.ipynb`, then run the webcam cells. Press **Q** to quit.
5. **Lane detection:** run `Lane_Detection.ipynb` to test on a sample image, or run the webcam cell for live detection. Press **Q** to quit.
6. **Vehicle health prediction:** run `Vehicle_Health.ipynb` to train and save the model, then call `predict_vehicle_health(...)` with the six sensor values.
7. **Accident risk alert:** run the combined module to get a live risk level from all three detectors.

## Configuration

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `IMG_SIZE` | (64, 64) | Input size for the drowsiness CNN |
| `ALERT_TIME` | 2.0 sec | Sleepy duration before the alert triggers |
| `scaleFactor` / `minNeighbors` | 1.1 / 5 | Haar face detection sensitivity |
| `n_estimators` | 200 | Number of trees in the vehicle health Random Forest |
| `test_size` | 0.20 | Train/test split for vehicle health |

## Future Work

- Add lane-departure warnings backed by evaluation against the road-line annotations
- Add an audio alarm to the drowsiness alert
- Use eye-aspect-ratio or eye-region detection for better drowsiness accuracy
- Add vibration sensing to the vehicle health module for richer fault detection
- Per-user history and trip reports tied to the logged-in account

## Author

**Jiya Batra** – [GitHub](https://github.com/JiyaBatra)
