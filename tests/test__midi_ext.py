# Copyright (c) 2019 Alethea Flowers for Winterbloom
# Licensed under the MIT License

import pytest

import winterbloom_smolmidi as smolmidi
from winterbloom_sol import _midi_ext


def make_message(type, *data):
    msg = smolmidi.Message()
    msg.type = type
    msg.data = data
    return msg


class MidiInStub:
    def __init__(self, messages):
        self._messages = iter(messages)
    
    def receive(self):
        return next(self._messages)

    def receive_sysex(self):
        return [0x01, 0x02]


def test_normal_stream():
    midi_in = _midi_ext.DeduplicatingMidiIn(MidiInStub([
        make_message(smolmidi.NOTE_ON, 0x64, 0x65),
        make_message(smolmidi.NOTE_OFF, 0x64, 0x70),
        None
    ]))

    assert midi_in.receive().type == smolmidi.NOTE_ON
    assert midi_in.receive().type == smolmidi.NOTE_OFF
    assert midi_in.receive() is None


def test_stream_with_duplicates():
    midi_in = _midi_ext.DeduplicatingMidiIn(MidiInStub([
        make_message(smolmidi.NOTE_ON, 0x64, 0x65),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x01),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x02),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x03),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x04),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x05),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x06),
        make_message(smolmidi.NOTE_OFF, 0x64, 0x70),
        None
    ]))

    assert midi_in.receive().type == smolmidi.NOTE_ON
    msg = midi_in.receive()
    assert msg.type == smolmidi.CHANNEL_PRESSURE
    assert msg.data[0] == 0x06
    assert midi_in.receive().type == smolmidi.NOTE_OFF
    assert midi_in.receive() is None


def test_stream_with_discontinous_duplicates():
    midi_in = _midi_ext.DeduplicatingMidiIn(MidiInStub([
        make_message(smolmidi.NOTE_ON, 0x64, 0x65),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x01),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x02),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x03),
        None,
        make_message(smolmidi.CHANNEL_PRESSURE, 0x04),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x05),
        make_message(smolmidi.CHANNEL_PRESSURE, 0x06),
        make_message(smolmidi.NOTE_OFF, 0x64, 0x70),
        None
    ]))

    assert midi_in.receive().type == smolmidi.NOTE_ON
    msg = midi_in.receive()
    assert msg.type == smolmidi.CHANNEL_PRESSURE
    assert msg.data[0] == 0x03
    msg = midi_in.receive()
    # It does *not* return the "None" in the middle of the stream,
    # instead, it just returns the next valid message.
    assert msg.type == smolmidi.CHANNEL_PRESSURE
    assert msg.data[0] == 0x06
    assert midi_in.receive().type == smolmidi.NOTE_OFF
    assert midi_in.receive() is None


def test_receive_sysex():
    midi_in = _midi_ext.DeduplicatingMidiIn(MidiInStub([]))

    assert midi_in.receive_sysex() == [0x01, 0x02]
