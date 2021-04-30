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

import time

import board
import digitalio
import micropython
import neopixel
import usb_midi
import winterbloom_smolmidi as smolmidi
import winterbloom_voltageio as voltageio
from winterbloom_ad_dacs import ad5686, ad5689
from winterbloom_sol import _calibration, _midi_ext, _utils, trigger


class State:
    """
    Tracks the state of MIDI input and provides easy access to common midi
    parameters.
    """

    def __init__(self):
        self.notes = {}
        self.message = None
        self.velocity = 0
        self.pitch_bend = 0
        self.pressure = 0
        self._cc = bytearray(128)
        self.playing = False
        self.clock = 0
        self.clock_frequency = 0

    @property
    @micropython.native
    def note(self):
        return self.latest_note

    @property
    @micropython.native
    def latest_note(self):
        if not self.notes:
            return None

        latest_note = None
        latest_time = 0
        for note, note_time in self.notes.items():
            if latest_time == 0 or note_time > latest_time:
                latest_note = note
                latest_time = note_time

        return latest_note

    @property
    @micropython.native
    def oldest_note(self):
        if not self.notes:
            return None

        oldest_note = None
        oldest_time = 0
        for note, note_time in self.notes.items():
            if oldest_time == 0 or note_time < oldest_time:
                oldest_note = note
                oldest_time = note_time

        return oldest_note

    @property
    @micropython.native
    def highest_note(self):
        if not self.notes:
            return None

        highest_note = 0
        for note in self.notes.keys():
            if highest_note == 0 or note > highest_note:
                highest_note = note

        return highest_note

    @property
    @micropython.native
    def lowest_note(self):
        if not self.notes:
            return None

        lowest_note = 0
        for note in self.notes.keys():
            if lowest_note == 0 or note < lowest_note:
                lowest_note = note

        return lowest_note

    @micropython.native
    def cc(self, number):
        return self._cc[number] / 127.0

    @micropython.native
    def copy_from(self, other):
        self.notes = other.notes.copy()
        self.message = other.message
        self.velocity = other.velocity
        self.pitch_bend = other.pitch_bend
        self.playing = other.playing
        self.clock = other.clock
        self._cc[:] = other._cc[:]


class StatusLED:
    def __init__(self):
        self._led = neopixel.NeoPixel(board.NEOPIXEL, 1, pixel_order=(0, 1, 2))
        self._led.brightness = 0.1
        self._led[0] = (0, 255, 255)
        self._hue = 0
        self._hue_rgb = (0, 255, 255)
        self._pulse_time = None

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, hue):
        self._hue = hue
        self._led[0] = self._hue_rgb = _utils.color_wheel(self._hue)

    def spin(self):
        self.hue += 5

    def pulse(self):
        self._pulse_time = time.monotonic_ns()
        self._led[0] = (255, 255, 255)

    @micropython.native
    def step(self):
        if self._pulse_time is None:
            return

        pulse_dt = min(
            ((time.monotonic_ns() - self._pulse_time) / 1000000000) / 0.2, 1.0
        )
        self._led[0] = (
            int(_utils.lerp(255, self._hue_rgb[0], pulse_dt)),
            int(_utils.lerp(255, self._hue_rgb[1], pulse_dt)),
            int(_utils.lerp(255, self._hue_rgb[2], pulse_dt)),
        )

        if pulse_dt == 1.0:
            self._pulse_time = None


class Outputs:
    """Manages all of the outputs for the Sol board and provides
    easy access to set them."""

    def __init__(self):
        if _utils.is_beta():
            dac_driver = ad5689
            # 5689 is calibrated from nominal values.
            calibration = _calibration.beta_nominal_calibration()
        else:
            dac_driver = ad5686
            # 5686 is externally calibrated.
            calibration = _calibration.load_calibration()

        self._dac = dac_driver.create_from_pins(cs=board.DAC_CS)
        self._dac.soft_reset()

        self._cv_a = voltageio.VoltageOut(self._dac.a)
        self._cv_a.direct_calibration(calibration["a"])
        self._cv_b = voltageio.VoltageOut(self._dac.b)
        self._cv_b.direct_calibration(calibration["b"])

        # 5686 has 4 channels.
        if dac_driver == ad5686:
            self._cv_c = voltageio.VoltageOut(self._dac.c)
            self._cv_c.direct_calibration(calibration["c"])
            self._cv_d = voltageio.VoltageOut(self._dac.d)
            self._cv_d.direct_calibration(calibration["d"])

        self._gate_1 = digitalio.DigitalInOut(board.G1)
        self._gate_1.direction = digitalio.Direction.OUTPUT
        self._gate_2 = digitalio.DigitalInOut(board.G2)
        self._gate_2.direction = digitalio.Direction.OUTPUT
        self._gate_3 = digitalio.DigitalInOut(board.G3)
        self._gate_3.direction = digitalio.Direction.OUTPUT
        self._gate_4 = digitalio.DigitalInOut(board.G4)
        self._gate_4.direction = digitalio.Direction.OUTPUT

        self._gate_1_trigger = trigger.Trigger(self._gate_1)
        self._gate_2_trigger = trigger.Trigger(self._gate_2)
        self._gate_3_trigger = trigger.Trigger(self._gate_3)
        self._gate_4_trigger = trigger.Trigger(self._gate_4)
        self._gate_1_retrigger = trigger.Retrigger(self._gate_1)
        self._gate_2_retrigger = trigger.Retrigger(self._gate_2)
        self._gate_3_retrigger = trigger.Retrigger(self._gate_3)
        self._gate_4_retrigger = trigger.Retrigger(self._gate_4)

        self.led = StatusLED()

    cv_a = _utils.ValueForwardingProperty("_cv_a", "voltage")
    cv_b = _utils.ValueForwardingProperty("_cv_b", "voltage")
    cv_c = _utils.ValueForwardingProperty("_cv_c", "voltage")
    cv_d = _utils.ValueForwardingProperty("_cv_d", "voltage")
    gate_1 = _utils.ValueForwardingProperty("_gate_1")
    trigger_gate_1 = _utils.ValueForwardingProperty("_gate_1_trigger", "trigger")
    retrigger_gate_1 = _utils.ValueForwardingProperty("_gate_1_retrigger", "retrigger")
    gate_2 = _utils.ValueForwardingProperty("_gate_2")
    trigger_gate_2 = _utils.ValueForwardingProperty("_gate_2_trigger", "trigger")
    retrigger_gate_2 = _utils.ValueForwardingProperty("_gate_2_retrigger", "retrigger")
    gate_3 = _utils.ValueForwardingProperty("_gate_3")
    trigger_gate_3 = _utils.ValueForwardingProperty("_gate_3_trigger", "trigger")
    retrigger_gate_3 = _utils.ValueForwardingProperty("_gate_3_retrigger", "retrigger")
    gate_4 = _utils.ValueForwardingProperty("_gate_4")
    trigger_gate_4 = _utils.ValueForwardingProperty("_gate_4_trigger", "trigger")
    retrigger_gate_4 = _utils.ValueForwardingProperty("_gate_4_retrigger", "retrigger")

    def __str__(self):
        return "<Outputs A:{}, B:{}, C:{}, D:{}, 1:{}, 2:{}, 3:{}, 4:{}>".format(
            self.cv_a,
            self.cv_b,
            self.cv_c,
            self.cv_d,
            self.gate_1,
            self.gate_2,
            self.gate_3,
            self.gate_4,
        )

    def set_cv(self, output, value):
        output = output.lower()
        if output not in ["a", "b", "c", "d"]:
            raise ValueError("No such CV channel '{}'".format(output))
        getattr(self, "_cv_" + output).voltage = value

    def set_gate(self, output, value):
        if output not in list(range(1, 5)):
            raise ValueError("No such gate channel '{}'".format(output))
        getattr(self, "_gate_{}".format(output)).value = value

    def trigger_gate(self, output):
        if output not in list(range(1, 5)):
            raise ValueError("No such gate channel '{}'".format(output))
        getattr(self, "_gate_{}_trigger".format(output))()

    def retrigger_gate(self, output):
        if output not in list(range(1, 5)):
            raise ValueError("No such gate channel '{}'".format(output))
        getattr(self, "_gate_{}_retrigger".format(output))()

    @micropython.native
    def step(self):
        self._gate_1_trigger.step()
        self._gate_2_trigger.step()
        self._gate_3_trigger.step()
        self._gate_4_trigger.step()
        self._gate_1_retrigger.step()
        self._gate_2_retrigger.step()
        self._gate_3_retrigger.step()
        self._gate_4_retrigger.step()
        self.led.step()


class _StopLoop(Exception):
    """Hidden exception used just for testing."""

    pass


class Sol:
    def __init__(self):
        self.outputs = Outputs()
        self._midi_in = _midi_ext.DeduplicatingMidiIn(
            smolmidi.MidiIn(usb_midi.ports[0])
        )
        self._clocks = 0
        self._last_clock = time.monotonic_ns()

    @micropython.native
    def _process_midi(self, msg, state):
        state.message = msg

        if not msg:
            return

        if msg.type == smolmidi.NOTE_ON:
            # Some controllers send note on with velocity 0
            # to signal note off.
            if msg.data[1] == 0:
                state.notes.pop(msg.data[0], None)
                state.velocity = 0
                state.message.type = smolmidi.NOTE_OFF
            else:
                state.notes[msg.data[0]] = time.monotonic_ns()
                state.velocity = msg.data[1] / 127.0

        elif msg.type == smolmidi.NOTE_OFF:
            state.notes.pop(msg.data[0], None)
            state.velocity = msg.data[1] / 127.0

        elif msg.type == smolmidi.CC:
            state._cc[msg.data[0]] = msg.data[1]

        elif msg.type == smolmidi.PITCH_BEND:
            pitch_bend_value = (((msg.data[1] << 7) | msg.data[0]) - 8192) / 8192
            state.pitch_bend = pitch_bend_value

        elif msg.type == smolmidi.CHANNEL_PRESSURE:
            state.pressure = msg.data[0] / 127.0

        # Alias polyphonic aftertouch to pressure. While this discards the
        # note information, it does make this easier to get at for most
        # users. It's also always possible to access the raw MIDI message.
        elif msg.type == smolmidi.AFTERTOUCH:
            state.pressure = msg.data[1] / 127.0

        elif msg.type == smolmidi.START or msg.type == smolmidi.CONTINUE:
            state.playing = True

        elif msg.type == smolmidi.STOP:
            state.playing = False
            self._clocks = 0

        elif msg.type == smolmidi.CLOCK:
            self._clocks += 1

            # Every quarter note, re-calculate the current BPM/clock frequency
            if self._clocks % 24 == 0:
                now = time.monotonic_ns()
                period = now - self._last_clock
                state.clock_frequency = 60000000000 / period
                self._last_clock = now

    def run(self, loop):
        last = State()
        current = State()
        while True:
            msg = self._midi_in.receive()
            self._process_midi(msg, current)
            current.clock = self._clocks

            if msg and not msg.type == smolmidi.CLOCK:
                self.outputs.led.spin()
            elif msg and msg.type == smolmidi.CLOCK and self._clocks % (96 / 2) == 0:
                self.outputs.led.pulse()

            try:
                loop(last, current, self.outputs)
            except _StopLoop:
                break

            last.copy_from(current)
            self.outputs.step()
