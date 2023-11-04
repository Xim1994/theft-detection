from domain.entities.sensor import Sensor
from domain.entities.alarm import Alarm
from domain.services.sensor_service import SensorService
from domain.services.alarm_service import AlarmService
from infrastructure.raspberry_pi.gpio_interface import GPIOInterface
from infrastructure.email_service import EmailService
from infrastructure.api_client import APIClient
from domain.value_objects.rfid_tag import RfidTag
import time
import logging

class DetectionHandler:
    def __init__(self, gpio_interface, email_service, api_client):
        self.gpio_interface = gpio_interface
        self.email_service = email_service
        self.api_client = api_client
        self.entry_sensor = Sensor(id='entry', sensor_type='PIR')
        self.cabin_sensor = Sensor(id='cabin', sensor_type='PIR')
        self.alarm = Alarm()
        self.current_rfid_tag = None
        self.product_info = None

    def attempt_rfid_read(self, timeout=5):
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            rfid_tag = self.gpio_interface.read_rfid_sensor()
            if rfid_tag:
                return rfid_tag
            time.sleep(0.1)  # Short delay to prevent spamming the RFID reader
        return None

    def reset_system(self):
        # Reset all relevant system states
        self.current_rfid_tag = None
        self.product_info = None
        AlarmService.reset_alarm(self.alarm)
        logging.info("System has been reset to idle state.")

    def handle_detection(self):
        try:
            # Detect entry sensor activation
            if SensorService.detect_sensor_activation(self.entry_sensor):
                self.current_rfid_tag = self.attempt_rfid_read()
                if self.current_rfid_tag:
                    self.product_info = self.api_client.get_product_info(self.current_rfid_tag)
                else:
                    # No RFID tag detected within the time frame, reset system
                    logging.warning("No RFID tag detected after entry movement.")
                    self.reset_system()
                    return
                
                # Wait for cabin sensor activation
                while not SensorService.detect_sensor_activation(self.cabin_sensor):
                    time.sleep(0.5)  # Avoid busy waiting
                
                # Wait for exit detection
                while not SensorService.detect_sensor_deactivation(self.entry_sensor):
                    time.sleep(0.5)  # Avoid busy waiting

                if not SensorService.is_active(self.cabin_sensor):
                    new_rfid_tag = self.gpio_interface.read_rfid_sensor()
                    if not new_rfid_tag or new_rfid_tag != self.current_rfid_tag:
                        AlarmService.trigger_alarm(self.alarm)
                        self.email_service.send_alert('Suspicious activity detected', 'Product info: ' + str(self.product_info))
                else:
                    # Person is still in the cabin
                    logging.info("Person is still in the cabin, waiting for exit.")
            else:
                # No entry detected, reset the alarm state if it was triggered
                if AlarmService.is_triggered(self.alarm):
                    AlarmService.reset_alarm(self.alarm)

        except Exception as e:
            logging.error(f"Error during detection handling: {e}")
            # Depending on the error you might want to send an email to the admin or log the incident.

        finally:
            # A delay before the next detection cycle begins, to avoid immediate re-triggering
            time.sleep(2)
