# The MIT License (MIT)
#
# Copyright (c) 2019 Alethea Flowers for Winterbloom
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import micropython
import winterbloom_smolmidi as smolmidi
from winterbloom_sol import sol

# One semitone in equal temperament, this is also the number of volts between
# notes in v/oct.
SEMITONE = semitone = 1 / 12


@micropython.native
def note_to_volts_per_octave(note):
    # C1 is MIDI Note 24, and A0 is the lowest common MIDI note. So we'll make 0v C1.
    note = note - 24
    if note < 0:
        return 0

    return note * SEMITONE


@micropython.native
def offset_for_pitch_bend(pitch_bend, range=2):
    return (pitch_bend * range) * SEMITONE


def voct(state_or_note, pitch_bend=0):
    """Returns the V/Oct given a state.
    This considers the note and the state of the pitch bend as well.

    """
    if isinstance(state_or_note, sol.State):
        note = state_or_note.note
        pitch_bend = pitch_bend or state_or_note.pitch_bend
    else:
        note = state_or_note

    return note_to_volts_per_octave(note) + offset_for_pitch_bend(pitch_bend)


def was_key_pressed(state):
    if state.message and state.message.type == smolmidi.NOTE_ON:
        return True
    else:
        return False


@micropython.native
def should_trigger_clock(state, division):
    operand = int(96 / division)

    if state.playing and state.clock % operand == 0:
        return True
    else:
        return False
