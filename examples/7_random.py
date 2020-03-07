"""This example shows how to use randomness with Sol.

This sample uses the MIDI clock to figure out when it should
trigger a new note. When it does, it randomly selects a note
from the major scale. You'll need to use a MIDI program that
can send MIDI clock - such as Ableton Live with sync enabled.

Output mapping:

CV A: Pitch CV based on a random note.
Gate 1: Gate on/off for the note.
"""

import random

import winterbloom_sol as sol

# This is a list of notes to choose from. For this example we're
# using the major scale.
notes = [
    0,
    2,
    4,
    5,
    7,
    9,
    11,
    12
]

# Pick which octave to play in. Octave "2" is the lowest Sol will output,
# so pick an octave somewhere above that.
octave = 4 * 12


def loop(last, state, outputs):
    # Trigger for every quarter note.
    if sol.should_trigger_clock(state, 4):
        
        # Select a random note.
        note = octave + random.choice(notes)

        # Set the CV A output to the notes v/oct value.
        outputs.cv_a = sol.voct(note)

        # And trigger the gate.
        outputs.retrigger_gate_1()

    # Otherwise, no need to have the gate on.
    else:
        outputs.gate_1 = False

sol.run(loop)