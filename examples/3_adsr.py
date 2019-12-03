"""This program shows how to use Sol's built-in ADSR envelope
generation functionality. If you don't need the second CV output
for something else, this allows you to use Sol instead of an
(or in addition to) a dedicated ADSR moduel.

This patch is a simplified version of the default program.

Output mapping:

- CV A: Note CV (v/oct), including pitch bend.
- CV B: ADSR CV from 0 to 8v.
- Gate 1: None
- Gate 2: None
- Gate 3: None
- Gate 4: None

"""

import winterbloom_sol as sol


# The built-in ADSR works just like a standandalone ADSR. It has
# attack, decay, sustain, and release parameters. You can create
# more than one ADSR if you'd like, but keep in mind you only
# have a limited number of CV outputs.
adsr = sol.ADSR(
    attack=0.5,   # Seconds
    decay=0.2,    # Seconds
    sustain=0.7,  # Percentage - 0.0 to 1.0
    release=1.0   # Seconds
)


def loop(last, state, outputs):
    if sol.was_key_pressed(state):
        # Instead of triggering a gate that could in turn start
        # an external ADSR, just start the built-in ADSR
        # directly.
        adsr.start()

    if state.note:
        outputs.cv_a = sol.voct(state)

    if not state.note:
        # Again, instead of changing the gate to low to
        # stop an external ADSR, just stop the built-in ADSR
        # directly.
        adsr.stop()

    # Set the output of CV B to the ADSR's output. Note that
    # the ADSR's output is from 0.0 to 1.0, so we scale it
    # up to 0.0 to 8.0v.
    outputs.cv_b = adsr.output * 8.0


sol.run(loop)
