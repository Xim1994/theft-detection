from domain.entities.sensor import Sensor, SensorType
from domain.entities.alarm import Alarm
from domain.services.sensor_service import SensorService
from domain.services.alarm_service import AlarmService
from infrastructure.raspberry_pi.gpio_interface import GPIOInterface
from infrastructure.email_service import EmailService
from infrastructure.api_client import ApiClient
import time
import logging
from dotenv import load_dotenv
import os

class DetectionHandler:
    def __init__(self, gpio_interface: GPIOInterface, email_service: EmailService, api_client: ApiClient):
        load_dotenv()

        self.gpio_interface = gpio_interface
        self.email_service = email_service
        self.api_client = api_client
        self.entry_sensor = Sensor(id='entry', sensor_type=SensorType.PIR, pin=int(os.getenv('ENTRY_PIR_PIN', '11')))
        self.cabin_sensor = Sensor(id='cabin', sensor_type=SensorType.PIR, pin=int(os.getenv('CABIN_PIR_PIN', '18')))
        self.alarm = Alarm(id='general', pin=int(os.getenv('ALARM_PIN', '13')))
        self.current_rfid_tag = None
        self.product_info = None
        self.sensor_service = SensorService(gpio_interface)
        self.alarm_service = AlarmService(gpio_interface)

        # Setup hardware
        self.setup_hardware()

    def setup_hardware(self):
        # Setup sensors and alarm led
        self.gpio_interface.setup_pir_sensor(self.entry_sensor.pin)
        self.gpio_interface.setup_pir_sensor(self.cabin_sensor.pin)
        self.gpio_interface.setup_led(self.alarm.pin)

    def attempt_rfid_read(self, timeout=5):
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            rfid_tag, rfid_text = self.gpio_interface.read_rfid_sensor()
            if rfid_tag:
                return rfid_tag
            time.sleep(0.1)  # Short delay to prevent spamming the RFID reader
        return None

    def reset_system(self):
        # Reset all relevant system states
        self.current_rfid_tag = None
        self.product_info = None
        self.alarm_service.reset_alarm(self.alarm)
        logging.info("System has been reset to idle state.")

    def handle_detection(self):
        try:
            # Detect entry sensor activation
            if self.sensor_service.detect_sensor_activation(sensor=self.entry_sensor):
                self.current_rfid_tag = self.attempt_rfid_read()
                if self.current_rfid_tag is None:
                    self.product_info = "hab" #self.api_client.get_product_info(self.current_rfid_tag)
                else:
                    # No RFID tag detected within the time frame, reset system
                    logging.warning("No RFID tag detected after entry movement.")
                    self.reset_system()
                    return
                
                # Wait for cabin sensor activation
                start_time = time.time()
                while not self.sensor_service.detect_sensor_activation(self.cabin_sensor):
                    time.sleep(0.5)  # Avoid busy waiting
                    if time.time() - start_time > timeout:
                        # Lógica para manejar el timeout
                        print("Tiempo de espera para la activación del sensor de la cabina excedido.")
                        return  # O maneja el timeout como prefieras
                
                # Wait for exit detection
                while self.sensor_service.detect_sensor_deactivation(self.entry_sensor):
                    time.sleep(0.5)  # Avoid busy waiting

                # wait a time for the rfid reading
                new_rfid_tag = self.gpio_interface.read_rfid_sensor()
                if not new_rfid_tag or new_rfid_tag != self.current_rfid_tag:
                    self.alarm_service.trigger_alarm(self.alarm)
                    self.email_service.send_alert('Suspicious activity detected', 'Product info: ' + str(self.product_info))

            else:
                # No entry detected, reset the alarm state if it was triggered
                if self.alarm_service.is_triggered(self.alarm):
                    self.alarm_service.reset_alarm(self.alarm)

        except Exception as e:
            logging.error(f"Error during detection handling: {e}")
            # Depending on the error you might want to send an email to the admin or log the incident.

        finally:
            # A delay before the next detection cycle begins, to avoid immediate re-triggering
            time.sleep(2)
