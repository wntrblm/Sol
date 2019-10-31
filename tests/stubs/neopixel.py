class NeoPixel:
    def __init__(self, pin, number):
        self.pin = pin
        self.number = number
        self._leds = [0] * number

    def __setitem__(self, key, value):
        self._leds[key] = value
    
    def __getitem__(self, key):
        return self._leds[key]
