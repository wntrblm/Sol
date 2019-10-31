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

import gc

import board
import digitalio
import neopixel
import usb_midi
import winterbloom_ad5689 as ad5689
import winterbloom_smolmidi as smolmidi
import winterbloom_voltageio as voltageio
from winterbloom_sol import _midi_ext, _utils, trigger


class State:
    """
    Tracks the state of MIDI input and provides easy access to common midi
    parameters.
    """

    def __init__(self):
        self.message = None
        self.note = None
        self.velocity = 0
        self.pitch_bend = 0
        self.pressure = 0
        self.cc = [0] * 128

    # TODO: Apply micropython.native to this.
    def copy_from(self, other):
        self.message = other.message
        self.note = other.note
        self.velocity = other.velocity
        self.pitch_bend = other.pitch_bend

        for n in range(len(self.cc)):
            self.cc[n] = other.cc[n]


class Outputs:
    """Manages all of the outputs for the Sol board and provides
    easy access to set them."""

    def __init__(self):
        self._dac = ad5689.create_from_pins(cs=board.D6)
        self._dac.soft_reset()
        self._cv_a = voltageio.VoltageOut(self._dac.a)
        self._cv_a.linear_calibration(10.26)
        self._cv_b = voltageio.VoltageOut(self._dac.b)
        self._cv_b.linear_calibration(10.26)
        self._gate_1 = digitalio.DigitalInOut(board.D10)
        self._gate_1.direction = digitalio.Direction.OUTPUT
        self._gate_2 = digitalio.DigitalInOut(board.D11)
        self._gate_2.direction = digitalio.Direction.OUTPUT
        self._gate_3 = digitalio.DigitalInOut(board.D12)
        self._gate_3.direction = digitalio.Direction.OUTPUT
        self._gate_4 = digitalio.DigitalInOut(board.D13)
        self._gate_4.direction = digitalio.Direction.OUTPUT
        self._gate_1_trigger = trigger.Trigger(self._gate_1)
        self._gate_2_trigger = trigger.Trigger(self._gate_2)
        self._gate_3_trigger = trigger.Trigger(self._gate_3)
        self._gate_4_trigger = trigger.Trigger(self._gate_4)

    cv_a = _utils.ValueForwardingProperty("_cv_a", "voltage")
    cv_b = _utils.ValueForwardingProperty("_cv_b", "voltage")
    gate_1 = _utils.ValueForwardingProperty("_gate_1")
    trigger_gate_1 = _utils.ValueForwardingProperty("_gate_1_trigger", "trigger")
    gate_2 = _utils.ValueForwardingProperty("_gate_2")
    trigger_gate_2 = _utils.ValueForwardingProperty("_gate_2_trigger", "trigger")
    gate_3 = _utils.ValueForwardingProperty("_gate_3")
    trigger_gate_3 = _utils.ValueForwardingProperty("_gate_3_trigger", "trigger")
    gate_4 = _utils.ValueForwardingProperty("_gate_4")
    trigger_gate_4 = _utils.ValueForwardingProperty("_gate_4_trigger", "trigger")

    def __str__(self):
        return "<Outputs A:{}, B:{}, 1:{}, 2:{}, 3:{}, 4:{}>".format(
            self.cv_a, self.cv_b, self.gate_1, self.gate_2, self.gate_3, self.gate_4
        )

    def step(self):
        self._gate_1_trigger.step()
        self._gate_2_trigger.step()
        self._gate_3_trigger.step()
        self._gate_4_trigger.step()


class Sol:
    def __init__(self):
        self.outputs = Outputs()
        self._midi_in = _midi_ext.DeduplicatingMidiIn(
            smolmidi.MidiIn(usb_midi.ports[0])
        )
        self._hue = 0
        self._led = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self._led.brightness = 0.05

    def _process_midi(self, state):
        msg = self._midi_in.receive()

        state.message = msg

        if not msg:
            return

        if msg.type == smolmidi.NOTE_ON:
            state.note = msg.data[0]
            state.velocity = msg.data[1] / 127.0

        elif msg.type == smolmidi.NOTE_OFF:
            if state.note == msg.data[0]:
                state.note = None
                state.velocity = msg.data[1] / 127.0

        elif msg.type == smolmidi.CC:
            state.cc[msg.data[0]] = msg.data[1]

        elif msg.type == smolmidi.PITCH_BEND:
            pitch_bend_value = (((msg.data[1] << 7) | msg.data[0]) - 8192) / 8192
            state.pitch_bend = pitch_bend_value

        elif msg.type == smolmidi.CHANNEL_PRESSURE:
            state.pressure = msg.data[0] / 127.0

        self._hue += 0.05
        self._led[0] = tuple(
            map(lambda x: int(x * 255), _utils.hsv_to_rgb(self._hue, 1.0, 1.0))
        )

    def run(self, loop):
        last = State()
        current = State()
        while True:
            self._process_midi(current)
            loop(last, current, self.outputs)
            last.copy_from(current)
            self.outputs.step()
            gc.collect()

    # Sketch for 2 channel API
    def run_two_channel(self, loop_one, loop_two):
        last_one = State()
        current_one = State()
        last_two = State()
        current_two = State()

        while True:
            self._process_midi_two_channel(current_one, current_two)
            loop_one(last_one, current_two, self.outputs)
            loop_two(last_two, current_two, self.outputs)
            self.outputs.step()
            gc.collect()
