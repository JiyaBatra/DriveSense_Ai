import numpy as np
from typing import Tuple, Dict

class FaceDetector:
    """Detect and track driver face"""
    
    def __init__(self):
        self.face_cascade = None
        self.eye_cascade = None
    
    def detect_face(self, frame):
        """Detect face in frame"""
        # Placeholder for face detection using cascade or YOLO
        return {
            'detected': True,
            'bbox': [50, 100, 250, 350],
            'confidence': 0.95,
            'landmarks': self._mock_landmarks()
        }
    
    def _mock_landmarks(self):
        """Generate mock facial landmarks"""
        return {
            'left_eye': (120, 180),
            'right_eye': (200, 180),
            'nose': (160, 220),
            'mouth': (160, 280)
        }

class EyeDetector:
    """Detect eyes and calculate Eye Aspect Ratio (EAR)"""
    
    EAR_THRESHOLD = 0.2
    CONSECUTIVE_FRAMES_THRESHOLD = 5
    
    def __init__(self):
        self.consecutive_drowsy_frames = 0
        self.eye_history = []
    
    def detect_eyes(self, face_region):
        """Detect eyes in face region"""
        return {
            'left_eye_detected': True,
            'right_eye_detected': True,
            'left_eye_bbox': [70, 160, 120, 200],
            'right_eye_bbox': [180, 160, 230, 200]
        }
    
    def calculate_eye_aspect_ratio(self, eye_landmarks):
        """
        Calculate Eye Aspect Ratio (EAR)
        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
        """
        if len(eye_landmarks) < 6:
            return 0.0
        
        # Calculate distances between eye landmarks
        A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_blink(self, ear_value):
        """Detect eye blink based on EAR"""
        if ear_value < 0.1:
            return True, 'Blink Detected'
        return False, 'Eyes Open'
    
    def update_drowsiness_state(self, ear_value):
        """Update drowsiness detection state"""
        self.eye_history.append(ear_value)
        
        if ear_value < self.EAR_THRESHOLD:
            self.consecutive_drowsy_frames += 1
        else:
            self.consecutive_drowsy_frames = 0
        
        is_drowsy = self.consecutive_drowsy_frames >= self.CONSECUTIVE_FRAMES_THRESHOLD
        
        return {
            'is_drowsy': is_drowsy,
            'consecutive_frames': self.consecutive_drowsy_frames,
            'ear_value': ear_value,
            'threshold_exceeded': ear_value < self.EAR_THRESHOLD
        }

class HeadPoseEstimator:
    """Estimate driver head position and gaze"""
    
    def __init__(self):
        self.head_positions = []
    
    def estimate_head_pose(self, face_landmarks):
        """Estimate head pitch, yaw, roll angles"""
        return {
            'pitch': 5.2,      # Looking down/up
            'yaw': -8.3,       # Looking left/right
            'roll': 2.1,       # Head tilt
            'confidence': 0.92
        }
    
    def detect_distraction(self, head_pose):
        """Detect driver distraction based on head pose"""
        distraction_types = []
        
        if abs(head_pose['yaw']) > 30:
            distraction_types.append('Looking to the side')
        
        if abs(head_pose['pitch']) > 30:
            distraction_types.append('Looking down')
        
        if abs(head_pose['roll']) > 20:
            distraction_types.append('Head tilted')
        
        return {
            'is_distracted': len(distraction_types) > 0,
            'distraction_types': distraction_types,
            'severity': 'High' if len(distraction_types) > 1 else 'Medium' if distraction_types else 'Low'
        }

class DriverBehaviorAnalyzer:
    """Analyze overall driver behavior"""
    
    def __init__(self):
        self.behavior_history = []
        self.total_alerts = 0
        self.total_distractions = 0
    
    def calculate_drowsiness_score(self, ear_value, max_score=100):
        """Calculate drowsiness score (0-100)"""
        # Lower EAR = Higher drowsiness
        score = max(0, min(max_score, int((0.3 - ear_value) * 333)))
        return score
    
    def generate_alert(self, drowsiness_score, distraction_data):
        """Generate driver alert if needed"""
        alert = None
        
        if drowsiness_score > 70:
            alert = {
                'type': 'CRITICAL_DROWSINESS',
                'message': 'Critical drowsiness detected! Emergency alert activated!',
                'severity': 'Critical',
                'action': 'IMMEDIATE_ACTION_REQUIRED'
            }
        elif drowsiness_score > 50:
            alert = {
                'type': 'HIGH_DROWSINESS',
                'message': 'High drowsiness detected. Please take a break.',
                'severity': 'High',
                'action': 'RECOMMENDED_BREAK'
            }
        elif drowsiness_score > 30:
            alert = {
                'type': 'MODERATE_DROWSINESS',
                'message': 'Moderate drowsiness detected.',
                'severity': 'Medium',
                'action': 'MONITOR'
            }
        
        if distraction_data['is_distracted'] and distraction_data['severity'] == 'High':
            alert = {
                'type': 'HIGH_DISTRACTION',
                'message': f'High distraction: {", ".join(distraction_data["distraction_types"])}',
                'severity': 'High',
                'action': 'FOCUS_ON_ROAD'
            }
        
        if alert:
            self.total_alerts += 1
        
        return alert
    
    def get_driver_score(self, drowsiness_score, distraction_count, trip_duration_hours):
        """Calculate overall driver safety score (0-100)"""
        # Start with 100 and deduct points
        score = 100
        
        # Drowsiness deduction
        score -= min(drowsiness_score, 40)
        
        # Distraction deduction
        score -= min(distraction_count * 5, 30)
        
        # Time on road deduction (fatigue accumulation)
        score -= min(trip_duration_hours * 2, 15)
        
        return max(0, score)
    
    def generate_report(self, metrics):
        """Generate driver behavior report"""
        return {
            'trip_duration': metrics.get('duration', 0),
            'distance_covered': metrics.get('distance', 0),
            'total_drowsiness_incidents': self.total_alerts,
            'average_drowsiness_score': metrics.get('avg_drowsiness', 0),
            'distractions_count': metrics.get('distractions', 0),
            'safety_score': metrics.get('safety_score', 0),
            'recommendation': self._get_recommendation(metrics.get('safety_score', 0))
        }
    
    def _get_recommendation(self, safety_score):
        """Get recommendation based on safety score"""
        if safety_score >= 90:
            return "Excellent driving behavior. Keep it up!"
        elif safety_score >= 75:
            return "Good driving. Be aware of minor distractions."
        elif safety_score >= 60:
            return "Fair driving. Work on focus and alertness."
        elif safety_score >= 45:
            return "Poor driving. Take breaks and avoid drowsiness."
        else:
            return "Critical: Immediate action needed. Stop driving immediately."
