import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class GPIOInterface:
    def __init__(self):
        # Use GPIO numbering
        GPIO.setmode(GPIO.BCM)
        # Initialize the RFID reader
        self.rfid_reader = SimpleMFRC522()

    def setup_pir_sensor(self, pin):
        # Set up the specified pin as an input pin
        GPIO.setup(pin, GPIO.IN)

    def read_pir_sensor(self, pin):
        # Read and return the value from the PIR sensor pin
        return GPIO.input(pin)

    def read_rfid_sensor(self):
        # This function will block until a RFID tag is present
        try:
            id, text = self.rfid_reader.read()
            return id, text
        except Exception as e:
            print("Error reading RFID sensor:", e)
            return None, None

    def cleanup(self):
        # Cleanup the GPIO pins
        GPIO.cleanup()
        # Close RFID reader
        self.rfid_reader.Close_MFRC522()