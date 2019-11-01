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


def loop(last, state, outputs):
    """The loop is run over and over to process MIDI information
    and translate it to outputs.

    "last" holds the previous state, "state" holds the current state,
    and "outputs" lets you control the output jacks.

    You can read more about the state here: TODO.
    And more about the outputs here: TODO.
    """
    # Whenever a new note message comes in, such as from
    # a key being pressed or a sequencer sending a note,
    # update the gate and trigger outputs.
    if sol.was_key_pressed(state):
        # Turn on Gate 1. If it's already on, re-trigger it
        # so that envelope generators and similar modules
        # notice that it's a distinct note.
        outputs.retrigger_gate_1()

        # For Gate 2, just trigger it every time a key
        # is pressed. No need for re-triggering since
        # this will automatically shut off after a few
        # milliseconds.
        outputs.trigger_gate_2()

    # If there's a note currently playing set CV A to the
    # voltage that corresponds to the note. This also
    # take pitch bend into account. Since pitch bend
    # can change in between keys being pressed we update
    # this every loop instead of just when a new note
    # message comes in.
    if state.note:
        # Set CV A to the V/oct value for the current note.
        # this handles pitch bend as well.
        outputs.cv_a = sol.voct(state)
    # If no note is being played, turn Gate 1 off.
    if not state.note:
        outputs.gate_1 = False

    # Set CV B's value based on the the Modulation Wheel.
    # The modulation wheel is MIDI controller 1 (CC 1).
    # The value from the state is from 0-1.0 so scale it to
    # 0-10v. If you want the range to be lower, change 10.0
    # to something else. For example, if you wanted it to
    # go from 0-8v, change it to 8.0.
    outputs.cv_b = 10.0 * state.cc(1)

    # Trigger Gate 3 on every 16th note.
    # If you want to trigger on a different division,
    # change 16 to your division. For example, to trigger
    # on every quarter note change it to 4.
    if sol.should_trigger_clock(state.clock, 16):
        outputs.trigger_gate_3()

    # Set Gate 4 to the state of the MIDI transport.
    # If the transport is "playing" then the gate will
    # be on, otherwise, it'll be off.
    outputs.gate_4 = state.playing


sol.run(loop)
