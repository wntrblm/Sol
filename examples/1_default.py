"""This is the default program that ships with Winterbloom Sol.

Output mapping:

- CV A: Note CV (v/oct), including pitch bend.
- CV B: Modulation wheel CV from 0-10v.
- Gate 1: Note Gate/Retrigger.
- Gate 2: Note Trigger.
- Gate 3: Midi Clock: triggers on 1/16th notes.
- Gate 4: MIDI Transport gate: on when playing, off when stopped.

"""

import winterbloom_sol as sol


def loop(last, current, outputs):
    # Was the note triggered/retriggered? This happens whenever
    # a new MIDI Note On message comes through.
    if sol.should_trigger_note(current):
        # Set CV A to the V/oct value for the current note.
        outputs.cv_a = sol.note_voct(current)
        # Turn on Gate 1. If it's already on, re-trigger it.
        outputs.retrigger_gate_1()
        # Trigger Gate 2.
        outputs.trigger_gate_2()

    # If no note is being played, turn Gate 1 off.
    if not current.note:
        outputs.gate_1 = False

    # Set CV B to the Modulation Wheel. The value is
    # from 0-1.0 so scale it to 0-10v.
    # If you want the range to be lower, change "10.0"
    # here to something else.
    outputs.cv_b = 10.0 * current.cc(1)

    # Output the MIDI clock on Gate 3.
    # TODO: if midi_clock: outputs.trigger_gate_3()

    # Set Gate 4 to the state of the MIDI transport.
    outputs.gate_4 = current.playing


sol.run(loop)
