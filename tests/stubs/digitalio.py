class Direction:
    OUTPUT = 0


class DigitalInOut:
    def __init__(self, pin):
        self.pin = pin
        self.value = False

    def switch_to_output(self, value):
        self.value = value
