import unittest
from domain.entities.alarm import Alarm

class TestAlarm(unittest.TestCase):
    def test_alarm_activation(self):
        alarm = Alarm(id="general")
        alarm.activate()
        self.assertTrue(alarm.is_active())

    def test_alarm_deactivation(self):
        alarm = Alarm(id="general")
        alarm.deactivate()
        self.assertFalse(alarm.is_active())
