class Alarm:
    def __init__(self, id: str, pin: int):
        self.id = id
        self.active = False
        self.pin = pin

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active
