import time
from domain.entities.sensor import Sensor
from infrastructure.raspberry_pi.gpio_interface import GPIOInterface

class SensorService:
    DEBOUNCE_DELAY = 0.5  # Tiempo en segundos para el debouncing

    def __init__(self, gpio_interface: GPIOInterface):
        self.gpio_interface = gpio_interface
        self.last_activation_time = {}
        self.sensor_state = {}

    def _is_debounced(self, sensor_id: str) -> bool:
        current_time = time.time()
        last_activation = self.last_activation_time.get(sensor_id, 0)
        return (current_time - last_activation) >= self.DEBOUNCE_DELAY

    def detect_sensor_activation(self, sensor: Sensor) -> bool:
        if self.gpio_interface.read_pir_sensor(sensor.pin) and self._is_debounced(sensor.id):
            self.last_activation_time[sensor.id] = time.time()
            self.sensor_state[sensor.id] = True
            return True
        return False

    def detect_sensor_deactivation(self, sensor: Sensor) -> bool:
        if not self.gpio_interface.read_pir_sensor(sensor.pin) and self._is_debounced(sensor.id):
            self.last_activation_time[sensor.id] = time.time()
            self.sensor_state[sensor.id] = False
            return True
        return False
