# Copyright (c) 2019 Alethea Flowers for Winterbloom
# Licensed under the MIT License

import math
from unittest import mock

import usb_midi
import winterbloom_smolmidi as smolmidi
from winterbloom_sol import sol

_NS_TO_S = 1000000000


class TestStateNoteStrategies:
    def make_state(self):
        state = sol.State()
        state.notes = {40: 4, 41: 3, 43: 2, 44: 1}
        return state

    def test_latest_note(self):
        assert self.make_state().latest_note == 40

    def test_oldest_note(self):
        assert self.make_state().oldest_note == 44

    def test_highest_note(self):
        assert self.make_state().highest_note == 44

    def test_lowest_note(self):
        assert self.make_state().lowest_note == 40

    def test_empty(self):
        state = sol.State()
        assert state.latest_note is None
        assert state.oldest_note is None
        assert state.highest_note is None
        assert state.lowest_note is None


class TestState:
    def test_default_state(self):
        state = sol.State()

        assert state.message is None
        assert state.note is None
        assert state.velocity == 0
        assert state.pitch_bend == 0
        assert state.pressure == 0
        for n in range(128):
            assert state._cc[n] == 0

    def test_copy_from(self):
        state_a = sol.State()
        state_b = sol.State()

        state_a.notes = {42: 0}
        state_a.message = object()
        state_a.velocity = 43
        state_a.pitch_bend == 45
        state_a.pressure == 46
        for n in range(128):
            state_a._cc[n] = n

        state_b.copy_from(state_a)

        assert state_b.message is state_a.message
        assert state_b.note == state_a.note
        assert state_b.velocity == state_a.velocity
        assert state_b.pitch_bend == state_a.pitch_bend
        assert state_b.pressure == state_a.pressure
        for n in range(128):
            assert state_b.cc(n) == state_a.cc(n)

        # Check for deep copy
        state_a.notes = {43: 0}
        assert state_b.note != state_a.note
        state_a._cc[0] = 100
        assert state_b.cc(0) != state_a.cc(0)


class TestOutputs:
    def test_default_state(self):
        outputs = sol.Outputs()

        assert outputs.cv_a == 0.0
        assert outputs.cv_b == 0.0
        assert outputs.cv_c == 0.0
        assert outputs.cv_d == 0.0
        assert outputs.gate_1 is False
        assert outputs.gate_2 is False
        assert outputs.gate_3 is False
        assert outputs.gate_4 is False

        assert (
            str(outputs)
            == "<Outputs A:0, B:0, C:0, D:0, 1:False, 2:False, 3:False, 4:False>"
        )

    def test_set_gate(self):
        outputs = sol.Outputs()

        outputs.set_gate(1, True)
        outputs.set_gate(2, True)
        outputs.set_gate(3, True)
        outputs.set_gate(4, True)

        assert outputs.gate_1 is True
        assert outputs.gate_2 is True
        assert outputs.gate_3 is True
        assert outputs.gate_4 is True

    def test_drive_cv_outs(self):
        outputs = sol.Outputs()

        outputs.cv_a = 8.0
        outputs.cv_b = 8.0
        outputs.cv_c = 8.0
        outputs.cv_d = 8.0

        assert outputs.cv_a == 8.0
        assert outputs.cv_b == 8.0
        assert outputs.cv_c == 8.0
        assert outputs.cv_d == 8.0

        assert outputs._cv_a._analog_out._driver.spi_device.spi.data

    def test_set_cv(self):
        outputs = sol.Outputs()

        outputs.set_cv("a", 8.0)
        outputs.set_cv("b", 7.0)
        outputs.set_cv("c", 6.0)
        outputs.set_cv("d", 5.0)

        assert outputs.cv_a == 8.0
        assert outputs.cv_b == 7.0
        assert outputs.cv_c == 6.0
        assert outputs.cv_d == 5.0

    @mock.patch("time.monotonic_ns", autospec=True)
    def test_trigger_step(self, time_monotonic):
        outputs = sol.Outputs()

        time_monotonic.return_value = 0
        outputs.trigger_gate_1()
        outputs.retrigger_gate_2()

        time_monotonic.return_value = 0.014 * _NS_TO_S
        outputs.step()
        assert outputs.gate_1 is True
        assert outputs.gate_2 is True

        time_monotonic.return_value = 0.016 * _NS_TO_S
        outputs.step()
        assert outputs.gate_1 is False
        assert outputs.gate_2 is True

        outputs.retrigger_gate_2()
        assert outputs.gate_2 is False
        time_monotonic.return_value = 0.032 * _NS_TO_S
        outputs.step()
        assert outputs.gate_2 is True


def make_message(type, *data):
    msg = smolmidi.Message()
    msg.type = type
    msg.data = data
    return msg


class TestSol:
    def test_default_state(self):
        sol.Sol()

    def test_run_loop_simple(self):
        def loop(previous, current, outputs):
            assert previous.note is None
            assert current.note == 42
            assert math.isclose(current.velocity, 0.5, rel_tol=0.01)

            outputs.gate_1 = True

            raise sol._StopLoop

        # Add data to the midi stub
        usb_midi.ports[0].data = iter([smolmidi.NOTE_ON, 42, 64])

        s = sol.Sol()
        s.run(loop)

        assert s.outputs.gate_1 is True

    def test_run_loop_note_on_note_off(self):
        count = 0

        def loop(previous, current, outputs):
            nonlocal count

            if count == 0:
                assert previous.note is None
                assert current.note == 42
            elif count == 1:
                assert previous.note == 42
                assert current.note is None
            else:
                raise sol._StopLoop

            count += 1

        # Add data to the midi stub
        usb_midi.ports[0].data = iter(
            [smolmidi.NOTE_ON, 42, 64, smolmidi.NOTE_OFF, 42, 0]
        )

        s = sol.Sol()
        s.run(loop)

        assert count == 2

    def test_process_midi_types_note_on_off(self):
        s = sol.Sol()
        state = sol.State()

        msg = make_message(smolmidi.NOTE_ON, 42, 64)
        s._process_midi(msg, state)
        assert state.note == 42
        assert math.isclose(state.velocity, 0.5, rel_tol=0.01)

        msg = make_message(smolmidi.NOTE_OFF, 42, 0)
        s._process_midi(msg, state)
        assert state.note is None
        assert state.velocity == 0

        # Note on with 0 velocity should be treated as Note Off
        msg = make_message(smolmidi.NOTE_ON, 42, 0)
        s._process_midi(msg, state)
        assert state.note is None
        assert state.velocity == 0

    def test_process_midi_types_cc(self):
        s = sol.Sol()
        state = sol.State()

        msg = make_message(smolmidi.CC, 42, 64)
        s._process_midi(msg, state)
        assert math.isclose(state.cc(42), 0.5, rel_tol=0.01)

    def test_process_midi_types_pitch_bend(self):
        s = sol.Sol()
        state = sol.State()

        msg = make_message(smolmidi.PITCH_BEND, 0x00, 0x40)
        s._process_midi(msg, state)
        assert state.pitch_bend == 0

        msg = make_message(smolmidi.PITCH_BEND, 0x00, 0x00)
        s._process_midi(msg, state)
        assert state.pitch_bend == -1

        msg = make_message(smolmidi.PITCH_BEND, 0x00, 0x80)
        s._process_midi(msg, state)
        assert state.pitch_bend == 1

    def test_process_midi_types_pressure(self):
        s = sol.Sol()
        state = sol.State()

        msg = make_message(smolmidi.CHANNEL_PRESSURE, 64)
        s._process_midi(msg, state)
        assert math.isclose(state.pressure, 0.5, rel_tol=0.01)
