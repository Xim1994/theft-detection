class Alarm:
    def __init__(self, id):
        self.id = id
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active
