class PortIn:
    def __init__(self):
        self.data = None

    def readinto(self, buf, numbytes):
        bytes_read = 0
        for n in range(numbytes):
            try:
                value = next(self.data)
                if isinstance(value, Exception):
                    raise value

                buf[n] = value
                bytes_read += 1
            except StopIteration:
                break

        return bytes_read


ports = [
    PortIn()
]
