"""This is my modified default program that attrempts multiple midi channels.

Output mapping:

- CV A: Midi channel 0 Note CV (v/oct).
- CV B: Midi channel 0 note velocity.
- CV C: Midi channel 1 Note CV (v/oct).
- CV D: Midi channel 1 note velocity.
- Gate 1: Midi channel 0 note Gate/Retrigger.
- Gate 2: Midi Clock: triggers on 1/8th notes.
- Gate 3: Midi channel 1 note Gate/Retrigger.
- Gate 4: MIDI Transport gate: on when playing, off when stopped.

"""
import winterbloom_smolmidi as smolmidi

import winterbloom_sol as sol

def loop(last, state, outputs):
    """The loop is run over and over to process MIDI information
    and translate it to outputs.

    "last" holds the previous state, "state" holds the current state,
    and "outputs" lets you control the output jacks.

    You can read more about the state here: TODO.
    And more about the outputs here: TODO.
    """
    if state.message:
        channel = state.message.channel

    # Whenever a new note message comes in, such as from
    # a key being pressed or a sequencer sending a note,
    # update the gate and trigger outputs.
    if sol.was_key_pressed(state):
        print('midi channel ' + str(channel))
       # Turn on Gate 1. If it's already on, re-trigger it
        # so that envelope generators and similar modules
        # notice that it's a distinct note.
        if channel == 0:
            outputs.retrigger_gate_1()
        elif channel == 1:
            outputs.retrigger_gate_3()



    # If there's a note currently playing set CV A to the
    # voltage that corresponds to the note. This also
    # takes pitch bend into account. Since pitch bend
    # can change in between keys being pressed this
    # has to update this every loop instead of just when
    # a new note message comes in.

    # I have not tested pitch bend !!!

    if state.message and state.note:
        if channel == 0:
            outputs.cv_a = sol.voct(state)
        elif channel == 1:
            outputs.cv_c = sol.voct(state)

    # If no note turned off, turn Gate off.
    if state.message and state.message.type == smolmidi.NOTE_OFF:
        print('note off')
        if channel == 0:
            outputs.gate_1 = False
        elif channel == 1:
            outputs.gate_3 = False

    # must check state.note or velocity changes upon NOTE_OFF
    if state.message and state.note:
        if channel == 0:
            outputs.cv_b = 8.0 * state.velocity
        elif channel == 1:
            outputs.cv_d = 8.0 * state.velocity


    # Trigger Gate 2 on every 8th note.
    # If you want to trigger on a different division,
    # change 16 to your division. For example, to trigger
    # on every quarter note change it to 4.
    if sol.should_trigger_clock(state, 8):
        outputs.trigger_gate_2()

    # Set Gate 4 to the state of the MIDI transport.
    # If the transport is "playing" then the gate will
    # be on, otherwise, it'll be off.
    outputs.gate_4 = state.playing


sol.run(loop)
