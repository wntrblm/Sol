# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import struct
import time

import board
import microcontroller
import neopixel
import supervisor


def get_cpu_id():
    print("".join("{:02x}".format(x) for x in microcontroller.cpu.uid))


def write_calibration_to_nvm(calibration_data):
    calibration_data = calibration_data.encode("utf-8")
    microcontroller.nvm[0:2] = b"\x69\x69"
    microcontroller.nvm[2:4] = struct.pack("H", len(calibration_data))
    microcontroller.nvm[4 : 4 + len(calibration_data)] = calibration_data
    print("okay, wrote", len(calibration_data), "bytes")


def read_calibration_from_nvm():
    magic_number, length = struct.unpack("HH", microcontroller.nvm[0:4])

    if magic_number != 0x6969:
        raise ValueError()

    data_string = bytes(microcontroller.nvm[4 : 4 + length]).decode("utf-8")
    exec_locals = {}

    exec(data_string, exec_locals)

    return exec_locals["calibration"]


def _calibration_panic():
    print(
        "ERROR: Your module can not read its calibration data!\n"
        + "Don't panic- it can be restored. Go to wntr.dev/sol/restore"
        + "for instructions."
    )
    print("Waiting for restore connection...")

    led = neopixel.NeoPixel(board.NEOPIXEL, 1, pixel_order=(0, 1, 2))
    led.brightness = 0.1

    while not supervisor.runtime.serial_bytes_available:
        led[0] = (255, 0, 0)
        time.sleep(0.1)
        led[0] = (255, 255, 0)
        time.sleep(0.1)

    led[0] = (255, 0, 255)

    while True:
        value = input()
        eval(value)
        print("done")


def load_calibration():
    try:
        return read_calibration_from_nvm()
    except Exception:
        _calibration_panic()


def beta_nominal_calibration():
    """Beta boards are not calibrated, so return calibration based on their nominal range."""
    return dict(a={0: 0, 10.23: 65535}, b={0: 0, 10.23: 65535})
