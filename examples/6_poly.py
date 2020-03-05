"""This program shows how to use Sol with polyphony.

It shows how to create a program with three voices (though you can have up to
four) and how they get assigned to different CV and gate outputs.

Output mapping:
- CV A, Gate 1: Voice one. The CV is the pitch, the gate is the note on/off.
- CV B, Gate 2: Voice two. The CV is the pitch, the gate is the note on/off.
- CV C, Gate 3: Voice three. The CV is the pitch, the gate is the note on/off.
- CV D: The mod wheel mapped to -5v to +5v.
- Gate 4: unused.

"""

import winterbloom_sol as sol

# Creates a polyphonic helper with three voices. You can use up to four,
# but it's limited to three in this example to show how you can still use
# remaining CV outputs for things like CC outputs.
poly = sol.Poly(num_voices=3)


def loop(last, state, outputs):
    # Tell the poly helper to update. It will automatically assign the three
    # voices to CV A, B, C and Gates 1, 2, 3.
    poly.update(state, outputs)

    # Since we have one left over CV and Gate, let's output the mod wheel
    # to the CV.
    outputs.cv_d = -5.0 + state.cc(1) * 10.0


sol.run(loop)
