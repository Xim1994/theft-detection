from domain.entities.alarm import Alarm
from domain.services.alarm_service import AlarmService
from infrastructure.raspberry_pi.gpio_interface import GPIOInterface
from infrastructure.email_service import EmailService
from infrastructure.api_client import ApiClient
import time
import logging
from dotenv import load_dotenv
import os
from pyepc import decode, SGTIN
from gpiozero import MotionSensor

logging.basicConfig(filename='system_log.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class DetectionHandler:
    def __init__(self):
        load_dotenv()

        self.gpio_interface = GPIOInterface()
        self.email_service = EmailService(os.getenv('EMAIL_SERVER'), int(os.getenv('EMAIL_PORT', '465')), os.getenv('EMAIL_PASSWORD'))
        self.api_client = ApiClient(os.getenv('BROWNIE_API_URL'), os.getenv('BROWNIE_API_TOKEN'))
        self.cabin_sensor = MotionSensor(int(os.getenv('CABIN_PIR_PIN', '23')))
        self.alarm = Alarm(id='general', pin=int(os.getenv('ALARM_PIN', '7')))
        self.current_rfid_tag = None
        self.product_info = None
        self.alarm_service = AlarmService(self.gpio_interface)

        # Setup hardware
        self.setup_hardware()

    def setup_hardware(self):
        # Setup sensors and alarm led
        self.gpio_interface.setup_led(self.alarm.pin)
        self.gpio_interface.setup_uhf_reader()

    def attempt_rfid_read(self, timeout=100):
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            rfid_tag = self.gpio_interface.read_uhf_tag()
            if rfid_tag:
                return rfid_tag
            time.sleep(0.1)  # Short delay to prevent spamming the RFID reader
        return None
    
    def get_gtin_from_epc(self, epc):
        x = decode(epc)
        sgtin = SGTIN(x.company_prefix, '0', x.item_ref, x.serial_number)
        return sgtin.gtin

    def reset_system(self):
        # Reset all relevant system states
        self.current_rfid_tag = None
        self.product_info = None
        self.alarm_service.reset_alarm(self.alarm)
        logging.info("System has been reset to idle state.")

    def detect_entry(self):
        try:
            self.cabin_sensor.wait_for_motion()
            logging.info("Motion detected - person entered")
        except Exception as e:
            logging.error(f"Error during entry detection: {e}")

    def detect_exit(self):
        try:
            self.cabin_sensor.wait_for_no_motion()
            logging.info("No motion detected - person exited")
        except Exception as e:
            logging.error(f"Error during exit detection: {e}")

    def read_rfid_on_entry(self):
        """Reads RFID tag upon entry."""
        rfid_tag = self.attempt_rfid_read()
        if rfid_tag:
            self.product_info = self.api_client.get_product_info(self.get_gtin_from_epc(rfid_tag))
            logging.info(f"RFID tag read on entry: {rfid_tag}")
            return rfid_tag
        else:
            logging.warning("No RFID tag detected on entry.")
            return None

    def check_rfid_on_exit(self, entry_rfid_tag):
        """Compares RFID tag read on exit with the one read on entry."""
        exit_rfid_tag = self.attempt_rfid_read()
        if exit_rfid_tag and exit_rfid_tag == entry_rfid_tag:
            logging.warning("Same RFID tag detected on exit, potential theft.")
            return True
        elif exit_rfid_tag is None:
            logging.info("No RFID tag detected on exit.")
        else:
            logging.info("Different RFID tag detected on exit.")
        return False

    def handle_detection(self):
        try:
            self.detect_entry()
            entry_rfid_tag = self.read_rfid_on_entry()
            if entry_rfid_tag is None:
                self.reset_system()
                return

            self.detect_exit()
            theft_detected = self.check_rfid_on_exit(entry_rfid_tag)
            if theft_detected:
                self.trigger_theft_alarm()
        except Exception as e:
            logging.error(f"Error during detection handling: {e}")
        finally:
            self.reset_system()
            time.sleep(2)  # Delay before next detection cycle

    def trigger_theft_alarm(self):
        """Triggers alarm and sends email notification in case of a theft."""
        self.alarm_service.trigger_alarm(self.alarm)
        body = self.email_service.get_email_body(self.product_info)
        self.email_service.send_email(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_RECEIVER'), os.getenv('EMAIL_SUBJECT'), body)
        logging.info("Theft alarm triggered and email notification sent.")
