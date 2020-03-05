# The MIT License (MIT)
#
# Copyright (c) 2020 Alethea Flowers for Winterbloom
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

import time

import winterbloom_smolmidi as smolmidi
from winterbloom_sol import helpers


class PolyNoteTracker:
    def __init__(self, num_voices=4):
        self.num_voices = num_voices
        self._assignments = []
        self.gates = []
        self.triggers = []
        for _ in range(self.num_voices):
            self._assignments.append([None, 0])
            self.gates.append(False)
            self.triggers.append(False)

    def update(self, state):
        now = time.monotonic_ns()

        # clear all triggers from the last update,
        # so we can properly re-trigger them if
        # new notes have shown up.
        for n in range(self.num_voices):
            self.triggers[n] = False

        if not state.message:
            return

        if state.message.type == smolmidi.NOTE_ON:
            # The idea here is to go through all of the voice assignments
            # and either find an unassigned voice or find the oldest one.
            # That becomes the slot for the new note.
            note = state.message.data[0]
            assignment_index = None
            oldest_time = None
            oldest_index = None

            for n in range(self.num_voices):
                if self._assignments[n][0] is None:
                    assignment_index = n
                    break
                if oldest_time is None or self._assignments[n][1] < oldest_time:
                    oldest_time = self._assignments[n][1]
                    oldest_index = n
            else:
                # No free voice, assign to the oldest one.
                assignment_index = oldest_index

            self._assignments[assignment_index][0] = note
            self._assignments[assignment_index][1] = now
            self.gates[assignment_index] = True
            self.triggers[assignment_index] = True

        elif state.message.type == smolmidi.NOTE_OFF:
            note = state.message.data[0]
            for n in range(self.num_voices):
                if self._assignments[n][0] == note:
                    self._assignments[n][0] = None
                    self.triggers[n] = False
                    self.gates[n] = False

    @property
    def notes(self):
        return [assignment[0] for assignment in self._assignments]


class Poly:
    _CV_NAMES = ("cv_a", "cv_b", "cv_c", "cv_d")
    _GATE_NAMES = ("gate_1", "gate_2", "gate_3", "gate_4")

    def __init__(self, num_voices=4):
        if num_voices > 4:
            raise ValueError(
                "Poly can only be used with up to 4 voices. Use PolyNoteTracker for more advanced polyphony."
            )
        self._tracker = PolyNoteTracker(num_voices=num_voices)

    def process_voice(self, state, outputs, note, trigger, cv_name, gate_name):
        if note:
            setattr(outputs, cv_name, helpers.voct(note, state.pitch_bend))

            if trigger:
                getattr(outputs, "retrigger_" + gate_name)()
        else:
            setattr(outputs, gate_name, False)

    def update(self, state, outputs):
        self._tracker.update(state)

        notes = self._tracker.notes
        triggers = self._tracker.triggers

        for n in range(self._tracker.num_voices):
            self.process_voice(
                state,
                outputs,
                notes[n],
                triggers[n],
                self._CV_NAMES[n],
                self._GATE_NAMES[n],
            )
