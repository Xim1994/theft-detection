import unittest
from unittest.mock import Mock, patch
from detection_handler import DetectionHandler  # Replace 'your_module' with the actual module name

class TestDetectionHandler(unittest.TestCase):
    def setUp(self):
        self.handler = DetectionHandler()
        self.handler.cabin_sensor = Mock()
        self.handler.gpio_interface = Mock()
        self.handler.api_client = Mock()

    @patch('your_module.time')  # Mock time.sleep to speed up tests
    def test_read_rfid_on_entry(self, mock_time):
        self.handler.gpio_interface.read_uhf_tag.return_value = 'test_rfid_tag'
        entry_tag = self.handler.read_rfid_on_entry()
        self.assertEqual(entry_tag, 'test_rfid_tag')

    def test_no_rfid_on_entry(self):
        self.handler.gpio_interface.read_uhf_tag.return_value = None
        entry_tag = self.handler.read_rfid_on_entry()
        self.assertIsNone(entry_tag)

    def test_theft_detection_triggers_alarm(self):
        self.handler.current_rfid_tag = 'test_rfid_tag'
        self.handler.gpio_interface.read_uhf_tag.return_value = 'test_rfid_tag'
        self.handler.alarm_service = Mock()
        self.handler.check_rfid_on_exit('test_rfid_tag')
        self.handler.alarm_service.trigger_alarm.assert_called_once()

    def test_no_theft_no_alarm(self):
        self.handler.current_rfid_tag = 'test_rfid_tag'
        self.handler.gpio_interface.read_uhf_tag.return_value = None
        self.handler.alarm_service = Mock()
        self.handler.check_rfid_on_exit('test_rfid_tag')
        self.handler.alarm_service.trigger_alarm.assert_not_called()

if __name__ == '__main__':
    unittest.main()
