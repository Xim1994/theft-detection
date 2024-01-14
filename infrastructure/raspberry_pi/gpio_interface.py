import RPi.GPIO as GPIO
from Library import uhf 

class GPIOInterface:
    def __init__(self):
        # Use GPIO numbering
        GPIO.setmode(GPIO.BOARD)

    def setup_pir_sensor(self, pin):
        # Set up the specified pin as an input pin
        GPIO.setup(pin, GPIO.IN)
    
    def setup_uhf_reader(self, port='/dev/ttyS0', baudrate='115200'):
        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7, GPIO.LOW)  # Enable the module
        self.uhf_reader = uhf.UHF(port, baudrate)

    def read_uhf_tag(self):
        try:
            rev = self.uhf_reader.single_read()
            if rev is not None:
                epc = ''.join(rev[8:20])
                # Further processing of EPC to get GTIN, if required
                return epc
            return None
        except Exception as e:
            print("Error reading UHF RFID tag:", e)
            return None

    def read_pir_sensor(self, pin):
        # Read and return the value from the PIR sensor pin
        return GPIO.input(pin)

    def setup_led(self, pin):
        GPIO.setup(pin, GPIO.OUT)

    def set_led_state(self, pin, state):
        GPIO.output(pin, state)

    def cleanup(self):
        # Cleanup the GPIO pins
        GPIO.cleanup()
        # Close RFID reader
        uhf.stop_read()