# Copyright (c) 2019 Alethea Flowers for Winterbloom
# Licensed under the MIT License

from unittest import mock

import winterbloom_smolmidi as smolmidi
from winterbloom_sol import helpers, poly, sol

_NS_TO_S = 1000000000


def make_message(type, *data):
    msg = smolmidi.Message()
    msg.type = type
    msg.data = data
    return msg


@mock.patch("time.monotonic_ns", autospec=True)
def test_poly_note_stealing(monotonic_ns):
    state = sol.State()
    outputs = sol.Outputs()

    p = poly.Poly()

    # No notes, all outputs should be default states.
    monotonic_ns.return_value = 0
    p.update(state, outputs)

    assert outputs.cv_a == 0
    assert outputs.cv_b == 0
    assert outputs.cv_c == 0
    assert outputs.cv_d == 0
    assert outputs.gate_1 is False
    assert outputs.gate_2 is False
    assert outputs.gate_3 is False
    assert outputs.gate_4 is False

    # Play one note, assert that it gets assigned.
    state.message = make_message(smolmidi.NOTE_ON, 40, 127)
    p.update(state, outputs)

    assert outputs.cv_a == helpers.note_to_volts_per_octave(40)
    assert outputs.cv_b == 0
    assert outputs.cv_c == 0
    assert outputs.cv_d == 0
    assert outputs.gate_1 is True
    assert outputs.gate_2 is False
    assert outputs.gate_3 is False
    assert outputs.gate_4 is False

    # Release the note, assert that it's gate gets released.
    monotonic_ns.return_value = 1 * _NS_TO_S
    state.message = make_message(smolmidi.NOTE_OFF, 40)
    p.update(state, outputs)

    assert outputs.gate_1 is False

    # Play four notes, assert that they all get assigned.
    monotonic_ns.return_value = 1 * _NS_TO_S
    state.message = make_message(smolmidi.NOTE_ON, 40, 127)
    p.update(state, outputs)
    monotonic_ns.return_value = 2 * _NS_TO_S
    state.message = make_message(smolmidi.NOTE_ON, 41, 127)
    p.update(state, outputs)
    monotonic_ns.return_value = 3 * _NS_TO_S
    state.message = make_message(smolmidi.NOTE_ON, 42, 127)
    p.update(state, outputs)
    monotonic_ns.return_value = 4 * _NS_TO_S
    state.message = make_message(smolmidi.NOTE_ON, 43, 127)
    p.update(state, outputs)

    assert outputs.cv_a == helpers.note_to_volts_per_octave(40)
    assert outputs.cv_b == helpers.note_to_volts_per_octave(41)
    assert outputs.cv_c == helpers.note_to_volts_per_octave(42)
    assert outputs.cv_d == helpers.note_to_volts_per_octave(43)
    assert outputs.gate_1 is True
    assert outputs.gate_2 is True
    assert outputs.gate_3 is True
    assert outputs.gate_4 is True

    # Play one more note, it should replace the oldest (first)
    # note.
    state.message = make_message(smolmidi.NOTE_ON, 44, 127)
    p.update(state, outputs)

    assert outputs.cv_a == helpers.note_to_volts_per_octave(44)

    # This should cause retrigger, so it should go False briefly
    # then go to True. step() must be called to update the gate
    # retrigger logic.
    assert outputs.gate_1 is False
    monotonic_ns.return_value = 5 * _NS_TO_S
    outputs.step()
    assert outputs.gate_1 is True

    # Release one of the notes in the middle. It should create
    # a "hole".
    state.message = make_message(smolmidi.NOTE_OFF, 42)
    p.update(state, outputs)

    assert outputs.gate_3 is False

    # Now, play another note. It should get assigned to the
    # "hole".
    state.message = make_message(smolmidi.NOTE_ON, 45, 127)
    p.update(state, outputs)

    assert outputs.cv_c == helpers.note_to_volts_per_octave(45)
    assert outputs.gate_3 is True
