# Winterbloom VoltageIO

This is a [CircuitPython](https://circuitpython.org) helper library for setting a digital-to-analog Converter (DAC) to a direct voltage value. That is, instead of setting a 16-bit integer value you can set the DAC to a floating-point voltage value. It also provides similar helpers for reading voltage values from analog-to-digital converters (ADCs).

For example you can replace this code:

```python
import board
from analogio import AnalogOut
 
analog_out = AnalogOut(board.A0)

# 0-3.3v range, so this should be ~0.25 volts.
analog_out.value = round(65535 * 0.25 / 3.3)
```

with this code:

```python
import board
from winterbloom_voltageio import VoltageOut
 
voltage_out = VoltageOut.from_pin(board.A0)

# 3.3v range.
voltage_out.linear_calibration(3.3)

# And 0.25v out.
voltage_out.voltage = 0.25
```

While this is a useful convenience for when you want to skip doing the math to set the DAC to a specific voltage, it's also incredibly useful for working around any non-linearity in your DAC. Real-world DACs have some degree of imperfection. You can measure the DAC's output voltage at various output values and then use `VoltageIO.direct_calibration` to get more accurate voltage output:

```python
voltage_out.direct_calibration({
    # Voltage: DAC value
    0: 0,
    0.825: 16000,
    1.65: 32723,
    2.475: 49230,
    3.3, 65535,
})
```

This library is also extremely useful if your DAC's output is scaled. For example, if you have an op amp after your DAC that's scaling its output to 0v-10v. You can use `VoltageIO` to set the output based on the final, scaled voltage:


```python
# While the DAC itself only ouputs up to 3.3v,
# it's scaled up to 10v by an op amp.
voltage_out.linear_calibration(10)

# 5.5v output.
voltage_out.voltage = 5.5
```

Very similarly and for similar reasons, you can use `VoltageIn` to read voltage values from ADCs. For example, you might replace this code:

```python
import board
from analogio import AnalogIn
 
analog_in = AnalogIn(board.A1)

# 3.3v range
voltage = analog_in.value * 3.3 / 65536

print(voltage)
```

with:

```python

import board
from winterbloom_voltageio import VoltageIn
 
voltage_in = VoltageIn.from_pin(board.A0)

# 3.3v range.
voltage_in.linear_calibration(3.3)

print(voltage_in)
```

Just like with `VoltageOut`, you can directly specify the calibration values. This allows you to counteract any non-linearity:

```python
voltage_in.direct_calibration({
    # ADC value: voltage
    0: 0,
    16000: 0.825,
    32723: 1.65,
    49230: 2.475,
    65535: 3.3,
})
```

And again, just like with `VoltageOut`, this class is useful for dealing with cases where your input voltage is scaled up or down for your ADC.

## Installation

Install this library by copying [winterbloom_voltageio.py](winterbloom_voltageio.py) to your device's `lib` folder.

## License and contributing

This is available under the [MIT License](LICENSE). I welcome contributors, please read the [Code of Conduct](CODE_OF_CONDUCT.md) first. :)
