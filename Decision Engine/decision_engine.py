from machine import RTC

class Packetisation:
    def __init__(self, sensor_id, sensor_data, data_type, decision_engine, payload, qos):
        # Use the DecisionEngine to classify the sensor data automatically
        urgency, priority = decision_engine.classify_data(sensor_data, data_type)
        importance = decision_engine.calculate_importance(data_type)
        data_size = len(payload)  # Assuming payload is a byte array or string
        
        # Initialize packet with automatically populated parameters
        self.packet = {
            'header': {
                'sensor_id': sensor_id,
                'urgency': urgency,
                'importance': importance,
                'data_type': data_type,
                'data_size': data_size,
                'timestamp': self.get_timestamp(),
                'qos': qos,
                'priority': priority  # Add priority from the decision engine
            },
            'payload': payload
        }

    def get_timestamp(self):
        """Get the current timestamp."""
        rtc = RTC()
        current_time = rtc.datetime()
        time_string = "Time: {:02}:{:02}:{:02}".format(current_time[4], current_time[5], current_time[6])
        return time_string

    def get_packet(self):
        return self.packet

class DecisionEngine:
    def __init__(self):
        # Define urgency thresholds for various sensors
        self.sensor_urgency_rules = {
            'temperature': lambda value: 0.6 if value > 35.0 or value < 0.0 else 0.0,
            'humidity': lambda value: 0.4 if value < 20.0 else 0.0,
            'pressure': lambda value: 0.2 if abs(value - 1015.0) > 10 else 0.0,
            'battery_level': lambda value: 1.0 if value < 5 else 0.8 if value < 10 else 0.5 if value < 15 else 0.2 if value < 20 else 0.0,
            'system_voltage': lambda value: 0.3 if value < 3.0 else 0.0, 
            'latitude': lambda value: 0.2 if value < -90.0 or value > 90.0 else 0.0,
            'longitude': lambda value: 0.2 if value < -180.0 or value > 180.0 else 0.0,
        }

        # Define importance levels for different data types
        self.data_type_importance = {
            'temperature': 0.8,
            'humidity': 0.7,
            'pressure': 0.5,
            'battery_level': 0.9,
            'system_voltage': 0.7,
            'latitude': 0.6,
            'longitude': 0.6,
        }

        # Priority thresholds
        self.high_urgency_threshold = 0.8
        self.medium_urgency_threshold = 0.5
        self.low_urgency_threshold = 0.2

    def calculate_urgency(self, sensor_data):
        """Calculate urgency based on sensor data and defined rules."""
        urgency = 0.0
        for sensor_type, value in sensor_data.items():
            rule = self.sensor_urgency_rules.get(sensor_type)
            if rule:
                urgency += rule(value)  # Apply the rule for this sensor type
        return min(urgency, 1.0)  # Clamp urgency to 1.0 max

    def calculate_importance(self, data_type):
        """Calculate importance based on data type."""
        return self.data_type_importance.get(data_type, 0.5)

    def classify_data(self, sensor_data, data_type):
        """
        Classify any type of sensor data by calculating urgency and importance.
        """
        urgency = self.calculate_urgency(sensor_data)
        importance = self.calculate_importance(data_type)

        priority_score = 0.6 * urgency + 0.4 * importance
        # Classify based on priority score
        if priority_score >= self.high_urgency_threshold:
            return urgency, "High Priority"
        elif self.medium_urgency_threshold <= priority_score < self.high_urgency_threshold:
            return urgency, "Medium Priority"
        elif self.low_urgency_threshold <= priority_score < self.medium_urgency_threshold:
            return urgency, "Low Priority"
        else:
            return urgency, "Background Priority"

    def preempt_message(self, message):
        """
        Preempt lower-priority messages if necessary.
        """
        pass
