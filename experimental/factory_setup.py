import io
import time
import os
import subprocess
import utils
import shutil
import zipfile

import requests

import calibrate

JLINK_PATH = "C:\Program Files (x86)\SEGGER\JLink\JLink.exe"
assert os.path.exists("bootloader.bin")
assert os.path.exists("firmware.uf2")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIRMWARE_DIR = os.path.join(ROOT_DIR, "firmware")
LIB_DIR = os.path.join(FIRMWARE_DIR, "lib")
EXAMPLES_DIR = os.path.join(ROOT_DIR, "examples")

FILES_TO_DEPLOY = {
    "https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/releases/download/6.0.0/adafruit-circuitpython-neopixel-5.x-mpy-6.0.0.zip:adafruit-circuitpython-neopixel-5.x-mpy-6.0.0/lib/neopixel.mpy": "lib",
    os.path.join(FIRMWARE_DIR, "winterbloom_sol"): "lib",
    os.path.join(FIRMWARE_DIR, "LICENSE"): ".",
    os.path.join(FIRMWARE_DIR, "README.HTM"): ".",
    os.path.join(LIB_DIR, "adafruit_circuitpython_busdevice/adafruit_bus_device"): "lib",
    os.path.join(LIB_DIR, "winterbloom_ad_dacs/winterbloom_ad_dacs"): "lib",
    os.path.join(LIB_DIR, "winterbloom_voltageio/winterbloom_voltageio.py"): "lib",
    os.path.join(LIB_DIR, "winterbloom_smolmidi/winterbloom_smolmidi.py"): "lib",
    EXAMPLES_DIR: ".",
    os.path.join(EXAMPLES_DIR, "1_default.py"): "code.py",
}


def program_bootloader():
    print("========== PROGRAMMING BOOTLOADER ==========")
    subprocess.check_call(
        [JLINK_PATH, "-device", "ATSAMD51J20", "-autoconnect", "1", "-if", "SWD", "-speed", "4000", "-CommanderScript", "flash-bootloader.jlink"]
    )


def program_circuitpython():
    print("========== PROGRAMMING CIRCUITPYTHON ==========")
    input("Connect usb cable, press enter.")
    bootloader_drive = utils.find_drive_by_name("SOLBOOT")
    utils.copyfile("firmware.uf2", os.path.join(bootloader_drive, "NEW.uf2"))


def deploy_circuitpython_code():
    print("========== DEPLOYING CODE ==========")
    # Wait for the circuitpython drive to show up.
    time.sleep(5)
    cpy_drive = utils.find_drive_by_name("CIRCUITPY")

    utils.clean_pycache(FIRMWARE_DIR)
    utils.clean_pycache(EXAMPLES_DIR)

    os.makedirs(os.path.join(cpy_drive, "lib"), exist_ok=True)

    for src, dst in FILES_TO_DEPLOY.items():
        if src.startswith("https://"):
            http_src, zip_path = src.rsplit(':', 1)

            zip_data = io.BytesIO(requests.get(http_src).content)

            with zipfile.ZipFile(zip_data, "r") as zipfh:
                file_data = zipfh.read(zip_path)
            
            dst = os.path.join(dst, os.path.basename(zip_path))
            with open(os.path.join(cpy_drive, dst), "wb") as fh:
                fh.write(file_data)
                
        else:
            if os.path.isdir(src):
                dst = os.path.join(cpy_drive, dst, os.path.basename(src))
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, os.path.join(cpy_drive, dst))

        print(f"Copied {src} to {dst}")
    
    utils.flush(cpy_drive)
    

def run_calibration():
    print("========== CALIBRATION & TEST ==========")
    calibrate.main()


def main():
    try:
        bootloader_drive = utils.find_drive_by_name("SOLBOOT")
    except:
        bootloader_drive = None
    
    try:
        circuitpython_drive = utils.find_drive_by_name("CIRCUITPY")
    except:
        circuitpython_drive = None

    if not circuitpython_drive and not bootloader_drive:
        program_bootloader()
    
    if not circuitpython_drive:
        program_circuitpython()

    if circuitpython_drive and os.path.exists(os.path.join(circuitpython_drive, "code.py")):
        if input("redeploy code? y/n: ").strip() == "y":
            deploy_circuitpython_code()
    else:
        deploy_circuitpython_code()

    if not circuitpython_drive or not os.path.exists(os.path.join(circuitpython_drive, "calibration.py")):
        run_calibration()


if __name__ == "__main__":
    main()