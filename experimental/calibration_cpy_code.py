import board
import winterbloom_ad5689 as ad5689
import winterbloom_voltageio
import supervisor
import neopixel
import microcontroller

supervisor.disable_autoreload()
pix = neopixel.NeoPixel(board.NEOPIXEL, 1, pixel_order=(0, 1, 2))
pix.brightness = 0.1
pix[0] = (255, 0, 255)

dac = ad5689.create_from_pins(cs=board.DAC_CS)
vio_a = winterbloom_voltageio.VoltageOut(dac.a)
vio_b = winterbloom_voltageio.VoltageOut(dac.b)
vio_c = winterbloom_voltageio.VoltageOut(dac.c)
vio_d = winterbloom_voltageio.VoltageOut(dac.d)


def set_dac(channel, dac_code):
    getattr(dac, channel).value = dac_code


def _vio_for_channel(channel):
    if channel == "a":
        return vio_a
    elif channel == "b":
        return vio_b
    elif channel == "c":
        return vio_c
    else:
        return vio_d

def set_calibration(channel, calibration_values):
    _vio_for_channel(channel).direct_calibration(calibration_values)


def set_voltage(channel, voltage):
    _vio_for_channel(channel).voltage = voltage


def get_cpu_id():
    print(''.join('{:02x}'.format(x) for x in microcontroller.cpu.uid))


print("ready")
while True:
    value = input()
    eval(value)
    print("done")