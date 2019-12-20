class SPI:
    def __init__(self, SCK, MOSI=None):
        self.sck = SCK
        self.mosi = MOSI
        self.data = []

    def try_lock(self):
        return True

    def unlock(self):
        pass

    def configure(self, *args, **kwargs):
        pass

    def write(self, data):
        self.data.append(data)
