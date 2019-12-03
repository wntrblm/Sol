"""This program is used to test Winterbloom Sol modules.

Output mapping:

- CV A: 0-10v sine wave
- CV B: 0-10v cosine wave
- Gates: on/off toggle

"""

import time
import math

import winterbloom_sol as sol


def loop(last, state, outputs):
    """The loop is run over and over to process MIDI information
    and translate it to outputs.

    "last" holds the previous state, "state" holds the current state,
    and "outputs" lets you control the output jacks.

    You can read more about the state here: TODO.
    And more about the outputs here: TODO.
    """
    outputs.cv_a = 5 + (5 * math.sin(3.14 * 2 * (time.monotonic() / 20.0)))
    outputs.cv_b = 5 + (5 * math.cos(3.14 * 2 * (time.monotonic() / 20.0)))

    outputs.gate_1 = (int(time.monotonic()) % 5 == 0)
    outputs.gate_2 = (int(time.monotonic()) % 5 == 0)
    outputs.gate_3 = (int(time.monotonic()) % 5 == 0)
    outputs.gate_4 = (int(time.monotonic()) % 5 == 0)


sol.run(loop)
