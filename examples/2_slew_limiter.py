"""This program shows how to use a SlewLimiter to add lag/legato
to your CV outputs. This shows how to use it with the note CV
output, but it can be used for any CV output.

This patch is a simplified version of the default program.

Output mapping:

- CV A: Note CV (v/oct), including pitch bend, with legato.
- CV B: None
- Gate 1: Note Gate/Retrigger.
- Gate 2: None
- Gate 3: None
- Gate 4: None

"""

import winterbloom_sol as sol


# Create a slew limiter to add legato/lag. Note that you should create
# this outside of the loop function. This is because it keeps track
# of state between calls to loop - if you created it in the loop it
# wouldn't have any idea of what the previous values were. You
# can create more than one and you can modify the rate in the loop
# if you want.
slew_limiter = sol.SlewLimiter(rate=1.5)  # Rate is in seconds.


def loop(last, state, outputs):
    if sol.was_key_pressed(state):
        outputs.retrigger_gate_1()

    if state.note:
        # Instead of setting the output of CV A directly, set
        # the slew limiter's target. The slew limiter will take
        # care of gradually moving its output to the target.
        slew_limiter.target = sol.voct(state)

    # Set the CV A output to the slew limiter's output.
    outputs.cv_a = slew_limiter.output

    if not state.note:
        outputs.gate_1 = False


sol.run(loop)
