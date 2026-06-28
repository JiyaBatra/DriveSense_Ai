import numpy as np
from typing import Dict, List

class VehicleSensorMonitor:
    """Monitor vehicle sensor data and health metrics"""
    
    def __init__(self):
        self.sensor_history = {}
        self.alert_thresholds = {
            'engine_temp': {'warning': 90, 'critical': 100},
            'battery_health': {'warning': 30, 'critical': 10},
            'fuel_level': {'warning': 15, 'critical': 5},
            'engine_rpm': {'warning': 5500, 'critical': 6500},
            'vibration': {'warning': 3, 'critical': 4}
        }
    
    def read_sensors(self, vehicle_id):
        """Read current sensor values"""
        return {
            'engine_temp': np.random.randint(60, 100),
            'battery_health': np.random.randint(70, 100),
            'fuel_level': np.random.randint(10, 100),
            'engine_rpm': np.random.randint(800, 5000),
            'vibration': np.random.uniform(0, 5),
            'oil_pressure': np.random.randint(40, 60),
            'coolant_level': np.random.uniform(0.7, 1.0)
        }
    
    def check_sensor_health(self, sensor_name, value):
        """Check if sensor value is within healthy range"""
        if sensor_name not in self.alert_thresholds:
            return 'Normal'
        
        thresholds = self.alert_thresholds[sensor_name]
        
        if value >= thresholds['critical']:
            return 'Critical'
        elif value >= thresholds['warning']:
            return 'Warning'
        else:
            return 'Normal'
    
    def generate_sensor_report(self, sensors):
        """Generate health report for all sensors"""
        report = {}
        
        for sensor_name, value in sensors.items():
            status = self.check_sensor_health(sensor_name, value)
            report[sensor_name] = {
                'value': value,
                'status': status,
                'threshold': self.alert_thresholds.get(sensor_name, {})
            }
        
        return report

class MaintenancePredictionModel:
    """Advanced predictive maintenance model"""
    
    # Component failure risk factors
    COMPONENT_FACTORS = {
        'Engine': {'mileage_factor': 0.0005, 'time_factor': 0.0001},
        'Battery': {'cycles_factor': 0.01, 'age_factor': 0.05},
        'Brakes': {'usage_factor': 0.0008, 'wear_factor': 0.02},
        'Transmission': {'mileage_factor': 0.0003, 'temperature_factor': 0.001},
        'Suspension': {'mileage_factor': 0.0002, 'road_factor': 0.001}
    }
    
    def __init__(self):
        self.maintenance_history = {}
    
    def calculate_component_risk(self, component, mileage, age_days, temp=70):
        """Calculate failure risk for specific component"""
        if component not in self.COMPONENT_FACTORS:
            return 0.0
        
        factors = self.COMPONENT_FACTORS[component]
        
        base_risk = (mileage * factors.get('mileage_factor', 0) +
                    age_days * factors.get('time_factor', 0))
        
        # Temperature factor for engine
        if component == 'Engine' and temp > 95:
            base_risk *= (1 + (temp - 95) * 0.01)
        
        return min(base_risk, 1.0)  # Cap at 1.0 (100%)
    
    def predict_maintenance_schedule(self, vehicle_data):
        """Predict maintenance schedule based on vehicle data"""
        mileage = vehicle_data.get('mileage', 0)
        age_days = vehicle_data.get('age_days', 0)
        engine_temp = vehicle_data.get('engine_temp', 70)
        
        maintenance_schedule = {}
        critical_components = []
        
        for component in self.COMPONENT_FACTORS.keys():
            risk = self.calculate_component_risk(component, mileage, age_days, engine_temp)
            
            maintenance_schedule[component] = {
                'risk_score': risk,
                'status': self._get_maintenance_status(risk),
                'days_until_maintenance': self._estimate_days(risk)
            }
            
            if risk > 0.7:
                critical_components.append(component)
        
        return {
            'schedule': maintenance_schedule,
            'critical_components': critical_components,
            'overall_risk': np.mean([c['risk_score'] for c in maintenance_schedule.values()])
        }
    
    def _get_maintenance_status(self, risk_score):
        """Get maintenance status based on risk score"""
        if risk_score > 0.8:
            return 'Critical - Immediate Service Required'
        elif risk_score > 0.6:
            return 'High - Service Recommended Soon'
        elif risk_score > 0.4:
            return 'Medium - Schedule Service'
        else:
            return 'Low - Continue Regular Checks'
    
    def _estimate_days(self, risk_score):
        """Estimate days until maintenance is needed"""
        if risk_score < 0.3:
            return 180
        elif risk_score < 0.6:
            return 60
        elif risk_score < 0.8:
            return 7
        else:
            return 0  # Immediate
    
    def calculate_remaining_useful_life(self, component, current_health):
        """Calculate remaining useful life of component"""
        # Health score: 0-100, where 100 is brand new
        if current_health > 80:
            return 'Excellent'
        elif current_health > 60:
            return 'Good'
        elif current_health > 40:
            return 'Fair'
        elif current_health > 20:
            return 'Poor'
        else:
            return 'Critical - Replace Soon'

class FuelEfficiencyAnalyzer:
    """Analyze and predict fuel efficiency"""
    
    def __init__(self):
        self.fuel_history = []
        self.trip_data = []
    
    def calculate_fuel_consumption(self, distance_km, fuel_consumed_liters):
        """Calculate fuel consumption in km/l"""
        if fuel_consumed_liters == 0:
            return 0
        return distance_km / fuel_consumed_liters
    
    def analyze_driving_efficiency(self, speed_profile, acceleration_profile, temperature):
        """Analyze driving efficiency based on driving patterns"""
        efficiency_score = 100
        
        # High speed penalty
        avg_speed = np.mean(speed_profile)
        if avg_speed > 100:
            efficiency_score -= 20
        elif avg_speed > 80:
            efficiency_score -= 10
        
        # Aggressive acceleration penalty
        avg_acceleration = np.mean([abs(a) for a in acceleration_profile])
        if avg_acceleration > 2:
            efficiency_score -= 30
        elif avg_acceleration > 1:
            efficiency_score -= 15
        
        # Cold engine penalty
        if temperature < 50:
            efficiency_score -= 10
        
        return max(0, efficiency_score)
    
    def predict_fuel_needed(self, planned_distance_km, avg_efficiency_kml, reserve_fuel_liters=5):
        """Predict fuel needed for planned trip"""
        fuel_needed = planned_distance_km / avg_efficiency_kml
        total_fuel_with_reserve = fuel_needed + reserve_fuel_liters
        
        return {
            'fuel_needed': fuel_needed,
            'total_with_reserve': total_fuel_with_reserve,
            'distance_possible': avg_efficiency_kml * (100 - reserve_fuel_liters),
            'recommendation': 'Adequate' if planned_distance_km < avg_efficiency_kml * 80 else 'Refuel Recommended'
        }
    
    def generate_efficiency_report(self, trip_data):
        """Generate fuel efficiency report"""
        return {
            'trip_distance': trip_data.get('distance', 0),
            'fuel_consumed': trip_data.get('fuel', 0),
            'avg_efficiency': self.calculate_fuel_consumption(trip_data.get('distance', 1), trip_data.get('fuel', 1)),
            'efficiency_score': self.analyze_driving_efficiency(
                trip_data.get('speeds', []),
                trip_data.get('accelerations', []),
                trip_data.get('temperature', 70)
            ),
            'cost_estimate': trip_data.get('fuel', 0) * 100  # Assuming $100 per liter for demo
        }
