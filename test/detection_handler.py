import unittest
from unittest.mock import Mock
from detection_handler import DetectionHandler

class TestDetectionHandler(unittest.TestCase):

    def setUp(self):
        # Crear mocks para las dependencias
        self.gpio_interface_mock = Mock()
        self.email_service_mock = Mock()
        self.api_client_mock = Mock()

        # Instanciar el objeto DetectionHandler con mocks
        self.detection_handler = DetectionHandler(
            gpio_interface=self.gpio_interface_mock,
            email_service=self.email_service_mock,
            api_client=self.api_client_mock
        )

    def test_attempt_rfid_read(self):
        # Configurar el comportamiento del mock
        self.gpio_interface_mock.read_rfid_sensor.return_value = ('tag', 'tag_text')

        # Llamar al método que se está probando
        result = self.detection_handler.attempt_rfid_read()

        # Verificar el resultado
        self.assertEqual(result, 'tag')

    def test_reset_system(self):
        # Llamar al método que se está probando
        self.detection_handler.reset_system()

        # Verificar si los estados se han restablecido
        self.assertIsNone(self.detection_handler.current_rfid_tag)
        self.assertIsNone(self.detection_handler.product_info)
        # Verificar si se llamó al método reset_alarm
        self.email_service_mock.reset_alarm.assert_called_once_with(self.detection_handler.alarm)

    # Agregar más pruebas para otros métodos...

if __name__ == '__main__':
    unittest.main()
