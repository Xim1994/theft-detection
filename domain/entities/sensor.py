class Sensor:
    def __init__(self, id, sensor_type):
        self.id = id
        self.sensor_type = sensor_type
        self.status = False

    def is_triggered(self):
        return self.status

    def set_status(self, status):
        self.status = status
