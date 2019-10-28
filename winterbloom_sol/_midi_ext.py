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

import winterbloom_smolmidi as smolmidi

_DEBUG = False
_DEDUPLICATE_MESSAGES = set(
    [
        smolmidi.CHANNEL_PRESSURE,
        smolmidi.AFTERTOUCH,
        smolmidi.CC,
        smolmidi.PITCH_BEND,
        smolmidi.SONG_POSITION,
    ]
)


class DeduplicatingMidiIn:
    """Like MidiIn, but can de-duplicate messages.

    For example, if the buffer is filled with a lot of Channel Pressure
    messages and we only care about the most recent one, this can ignore
    all but the latest automatically.
    """

    def __init__(self, midi_in):
        self._midi_in = midi_in
        self._peeked = None

    # TODO: Mark this with @micropython.native
    def receive(self):
        if self._peeked is not None:
            message = self._peeked
            self._peeked = None
        else:
            message = self._midi_in.receive()

        if message is None:
            return None

        if message.type not in _DEDUPLICATE_MESSAGES:
            return message

        # Peek ahead and see if there's another message of the same type.
        count = 0
        while True:
            self._peeked = self._midi_in.receive()

            # If not, break.
            if self._peeked is None:
                break

            if self._peeked.type != message.type:
                break

            message = self._peeked
            count += 1

        if _DEBUG and count:  # pragma: no cover
            print(
                "Skipped {} messages, error count: {}".format(
                    count, self._midi_in.error_count
                )
            )

        return message

    def receive_sysex(self, *args, **kwargs):
        return self._midi_in.receive_sysex(*args, **kwargs)
