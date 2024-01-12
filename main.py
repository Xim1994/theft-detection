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