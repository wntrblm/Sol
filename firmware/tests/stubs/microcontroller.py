nvm = bytearray([0xFF] * 8000)


def _load_test_calibration():
    import os
    import struct

    calibration_data = (
        open(os.path.join(os.path.dirname(__file__), "calibration.py"), "r")
        .read()
        .encode("utf-8")
    )
    nvm[0:2] = b"\x69\x69"
    nvm[2:4] = struct.pack("H", len(calibration_data))
    nvm[4 : 4 + len(calibration_data)] = calibration_data


_load_test_calibration()
