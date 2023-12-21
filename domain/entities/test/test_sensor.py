import unittest
from domain.entities.sensor import Sensor, SensorType

class TestSensor(unittest.TestCase):
    def test_sensor_initialization(self):
        sensor = Sensor(id="1", sensor_type=SensorType.PIR, pin=11)
        self.assertEqual(sensor.id, "1")
        self.assertFalse(sensor.is_triggered())

    def test_set_status(self):
        sensor = Sensor(id="1", sensor_type=SensorType.PIR, pin=11)
        sensor.set_status(True)
        self.assertTrue(sensor.is_triggered())
