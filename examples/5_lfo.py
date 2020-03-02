"""This program shows how to use the LFO classes to output an
LFO on one of the CV outputs.

Output mapping:
- CV A: A constant sine wave LFO at a frequency of 2 Hz.
- CV B: A variable sawtooth LFO at a frequency determined by the
    modulation wheel. 0-10 Hz.
"""

import winterbloom_sol as sol


# The SineLFO, SawtoothLFO, and TriangeLFO objects can generate
# low-frequency oscillators for you. You just have to specify the
# frequency for the LFO, which you can change later.
sine_lfo = sol.SineLFO(2.0)  # 2 Hz
# For the saw LFO, we'll set it to 0 Hz to start withn and we'll
# use the mod wheel to change it.
saw_lfo = sol.SawtoothLFO(0)  


def loop(last, state, outputs):
    # For the first LFO, we'll send its value to CV A.
    # Since the LFO's value will be between -1 and +1,
    # we'll scale it up to -2 to +2 so the LFO will swing
    # from -2v to +2v.
    outputs.cv_a = sine_lfo.output * 2.0
    
    # For the second LFO, we need to update its frequency
    # based on the mod wheel value. Since the mod wheel
    # value is between 0 and 1.0, we'll scale that up
    # so that the LFO frequency is between 0 and 10 Hz.
    saw_lfo.frequency = state.cc(1) * 10.0

    # Now that we've set the frequency, we can output
    # its value to CV B just the same way we did with
    # the first LFO.
    outputs.cv_b = saw_lfo.output * 2.0


sol.run(loop)
