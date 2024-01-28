import RPi.GPIO as GPIO
from domain.entities.alarm import Alarm
from infrastructure.raspberry_pi.gpio_interface import GPIOInterface

class AlarmService:
    def __init__(self, gpio_interface: GPIOInterface):
        self.gpio_interface = gpio_interface

    def trigger_alarm(self, alarm: Alarm):
        # Logic to interface with actual alarm hardware
        self.gpio_interface.set_led_state(alarm.pin, GPIO.HIGH)
        alarm.activate()

    def reset_alarm(self, alarm: Alarm):
        # Logic to interface with actual alarm hardware
        self.gpio_interface.set_led_state(alarm.pin, GPIO.LOW)
        alarm.deactivate()
