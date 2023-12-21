import unittest
from unittest.mock import Mock
from domain.services.sensor_service import SensorService
from domain.entities.sensor import Sensor, SensorType

class TestSensorService(unittest.TestCase):
    def setUp(self):
        self.gpio_interface_mock = Mock()
        self.sensor_service = SensorService(self.gpio_interface_mock)
        self.sensor = Sensor(id="1", sensor_type=SensorType.PIR, pin=11)

    def test_detect_sensor_activation(self):
        self.gpio_interface_mock.read_pir_sensor.return_value = True
        result = self.sensor_service.detect_sensor_activation(self.sensor)
        self.assertTrue(result)

    def test_detect_sensor_deactivation(self):
        self.gpio_interface_mock.read_pir_sensor.return_value = False
        result = self.sensor_service.detect_sensor_deactivation(self.sensor)
        self.assertTrue(result)

    def test_sensor_activation_with_debounce(self):
        self.gpio_interface_mock.read_pir_sensor.return_value = True
        # Primera llamada, debe retornar True
        self.assertTrue(self.sensor_service.detect_sensor_activation(self.sensor))
        # Llamadas subsecuentes deben retornar False debido al debounce
        self.assertFalse(self.sensor_service.detect_sensor_activation(self.sensor))
