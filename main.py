from application.services.provisioning_application_service import ProvisioningApplicationService
from infrastructure.wifi_provisioning_service import WiFiProvisioningService
from application.handlers.detection_handler import DetectionHandler
from infrastructure.raspberry_pi.gpio_interface import GPIOInterface
from infrastructure.email_service import EmailService
from infrastructure.api_client import ApiClient
from gpiozero import MotionSensor

if __name__ == '__main__':
    pir = MotionSensor(4)
    pir.wait_for_motion()
    print("Motion detected!")
    gpio_interface = GPIOInterface()
    email_service = EmailService()
    api_client = ApiClient('https://api.clientdomain.com/')

    # Verificar la conexión WiFi y, si es necesario, iniciar el punto de acceso y el servidor Flask

    ProvisioningApplicationService.check_and_start_ap()

    # Si ya está conectado a WiFi, continuar con el flujo normal de la aplicación
    if WiFiProvisioningService.is_wifi_connected():
        detection_handler = DetectionHandler(gpio_interface, email_service, api_client)

    # Main loop
    while True:
        detection_handler.handle_detection()
    
import time
import sys
sys.path.append("..")
from Library import uhf 
import RPi.GPIO as GPIO
from pyepc import decode, SGTIN

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(7,GPIO.OUT)

GPIO.output(7,GPIO.LOW)# Enable the module

baudrate ='115200'
port     ='/dev/ttyS0'

uhf = uhf.UHF(port,baudrate)

'''
Uncomment corresponding section to increase reading range,
you will have to set the region as per requirment
'''

#uhf.setRegion_EU() 
#uhf.setRegion_US()
# Example usage

rev = uhf.single_read()
if rev is not None:
   print('EPC = ',rev[8:20])
   epc = ''.join(rev[8:20])
   print(epc) 
   print('RSSI(dBm) = ',int(rev[5],base=16))
   print('CRC = ',rev[20],rev[21])

   # Example usage
   x = decode(epc)
   sgtin = SGTIN(x.company_prefix, '0', x.item_ref, x.serial_number)
   gtin = sgtin.gtin

   print(f"GTIN: {gtin}")

time.sleep(1)
uhf.stop_read()

'''
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Hold a tag near the reader")
    while True:
        id, text = reader.read()
        print("ID:", id)
        print("Text:", text)

except Exception as e:
    print(e)
finally:
    GPIO.cleanup()

import RPi.GPIO as GPIO
import time

# pir at BCM port 23
# PIR sensitivity (detect  range) can be tuned by adjusting the
# screw on the right side of the buuzzer
pir_gpio = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pir_gpio, GPIO.IN, GPIO.PUD_DOWN)

def no_motion():
    print("Nothing moves â€¦")

def motion_detected():
    print("Motion detected at "+str(time.ctime()))

try:
  while True:
    if(GPIO.input(pir_gpio) == 0):
        no_motion()
    elif(GPIO.input(pir_gpio) == 1):
        motion_detected()
    time.sleep(0.1)
except KeyboardInterrupt:
  print('interrupted!')7YDchRhUYS
  GPIO.cleanup()'''