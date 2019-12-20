#!/bin/bash
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
cp -r /mnt/c/Users/jjram/Desktop/neopixel.mpy /mnt/e/lib/
cp -r winterbloom_sol /mnt/e/lib
cp -r lib/adafruit_circuitpython_busdevice/adafruit_bus_device /mnt/e/lib/
cp -r lib/winterbloom_ad5689/winterbloom_ad5689.py /mnt/e/lib/
cp -r lib/winterbloom_voltageio/winterbloom_voltageio.py /mnt/e/lib
cp -r lib/winterbloom_smolmidi/winterbloom_smolmidi.py /mnt/e/lib
cp -r examples/00_test.py /mnt/e/code.py