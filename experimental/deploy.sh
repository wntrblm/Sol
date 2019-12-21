#!/bin/bash
cd "$(dirname "$0")"/..
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
rm -rf deploy-bundle
mkdir -p deploy-bundle deploy-bundle/lib deploy-bundle/examples
cp -r /mnt/c/Users/jjram/Desktop/neopixel.mpy deploy-bundle/lib
cp -r firmware/winterbloom_sol deploy-bundle/lib
cp -r firmware/lib/adafruit_circuitpython_busdevice/adafruit_bus_device deploy-bundle/lib/
cp -r firmware/lib/winterbloom_ad5689/winterbloom_ad5689.py deploy-bundle/lib/
cp -r firmware/lib/winterbloom_voltageio/winterbloom_voltageio.py deploy-bundle/lib
cp -r firmware/lib/winterbloom_smolmidi/winterbloom_smolmidi.py deploy-bundle/lib
cp -r examples/*.py deploy-bundle/examples
cp -r examples/1_default.py deploy-bundle/code.py