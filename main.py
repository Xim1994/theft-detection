from application.handlers.detection_handler import DetectionHandler
from infrastructure.raspberry_pi.gpio_interface import GPIOInterface
from infrastructure.email_service import EmailService

if __name__ == '__main__':
    gpio_interface = GPIOInterface()
    email_service = EmailService()

    detection_handler = DetectionHandler(gpio_interface, email_service)

    # Main loop
    while True:
        detection_handler.handle_detection()
