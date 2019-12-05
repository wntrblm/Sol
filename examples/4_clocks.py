"""This program shows how to send information from the MIDI clock
and transport to the various gate outputs.

You'll need to use a program or sequencer that can send MIDI clock,
for example, Ableton Live.

With Ableton Live, the transport and clock data will be sent when
you press "play" in Live. The clock should match the BPM
in Live.

Output mapping:

- CV A: None
- CV B: None
- Gate 1: Transport play/stop. High when the MIDI transport is playing,
    low otherwise.
- Gate 2: Triggers every quarter note.
- Gate 3: Triggers every eighth note.
- Gate 4: Triggers every sixteenth note.
"""

import winterbloom_sol as sol


def loop(last, state, outputs):
    # Set Gate 1 to the state of the MIDI transport.
    # If the transport is "playing" then the gate will
    # be on, otherwise, it'll be off.
    outputs.gate_1 = state.playing

    # Trigger Gate 2, 3, and 4 based on the MIDI clock.
    # Trigger Gate 2 every quarter note.
    if sol.should_trigger_clock(state, 4):
        outputs.trigger_gate_2()
    # Trigger Gate 3 every eighth note.
    if sol.should_trigger_clock(state, 8):
        outputs.trigger_gate_3()
    # Trigger Gate 4 every sixteenth note.
    if sol.should_trigger_clock(state, 16):
        outputs.trigger_gate_4()


sol.run(loop)
