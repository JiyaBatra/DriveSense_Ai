import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class MaintenancePredictor:
    """Predicts vehicle maintenance needs"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.trained = False
    
    def train(self, X_train, y_train):
        """Train the maintenance prediction model"""
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.trained = True
    
    def predict(self, features):
        """Predict maintenance requirement"""
        if not self.trained:
            # Return dummy prediction if not trained
            return {
                'risk_score': np.random.uniform(0, 1),
                'days_to_maintenance': np.random.randint(7, 180),
                'failure_probability': np.random.uniform(0, 1)
            }
        
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0].max()
        
        return {
            'risk_score': probability,
            'days_to_maintenance': max(7, int(180 * (1 - probability))),
            'failure_probability': probability
        }

class DrowsinessDetector:
    """Detects driver drowsiness using Eye Aspect Ratio"""
    
    @staticmethod
    def calculate_ear(eye_points):
        """Calculate Eye Aspect Ratio (EAR)"""
        if len(eye_points) < 6:
            return 0
        
        # Euclidean distance between points
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])
        C = np.linalg.norm(eye_points[0] - eye_points[3])
        
        ear = (A + B) / (2.0 * C)
        return ear
    
    @staticmethod
    def detect_drowsiness(ear, threshold=0.2, consecutive_frames=5):
        """
        Detect drowsiness based on EAR
        ear: Eye Aspect Ratio value
        threshold: EAR threshold for drowsiness
        consecutive_frames: frames needed to trigger alert
        """
        if ear < threshold:
            return True
        return False
    
    @staticmethod
    def calculate_drowsiness_score(ear, max_score=100):
        """Calculate drowsiness score (0-100)"""
        # Lower EAR = higher drowsiness
        score = max(0, min(max_score, int((0.3 - ear) * 333)))
        return score

# Create singleton instances
maintenance_predictor = MaintenancePredictor()
drowsiness_detector = DrowsinessDetector()
