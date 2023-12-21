from enum import Enum

class SensorType(Enum):
    PIR = 1

class Sensor:
    def __init__(self, id: str, sensor_type: SensorType, pin: int):
        self.id = id
        self.sensor_type = sensor_type
        self.status = False
        self.pin = pin

    def is_triggered(self):
        return self.status

    def set_status(self, status):
        self.status = status
