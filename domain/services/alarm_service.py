from domain.entities.alarm import Alarm

class AlarmService:
    @staticmethod
    def trigger_alarm(alarm: Alarm):
        # Logic to interface with actual alarm hardware
        alarm.activate()

    @staticmethod
    def reset_alarm(alarm: Alarm):
        # Logic to interface with actual alarm hardware
        alarm.deactivate()
