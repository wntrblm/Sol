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

# Use nanoseconds for absolute time throughout to avoid losing precision for float
# time over long program duration.
_NS_TO_S = 1000000000


class Trigger:
    """A trigger/retrigger helper.

    This handles "triggering" an output for a short duration. This is
    similar to gate, but gate is a continuous on/off, whereas trigger
    is a short pulse of on or off. For example::

        Trigger: ____-____
        Gate:    ____-----

    Example usage::

        trigger = Trigger(DigitalInOut(board.D3))
        trigger()

        while True:
            trigger.step()
    """

    def __init__(self, output, duration_ms=15):
        self._output = output
        self._duration = duration_ms
        self._start_time = None

    def trigger(self, duration_ms=None):
        # TODO: Figure out what to do if the trigger
        # phase is still on-going.
        if self._start_time is not None:
            return False

        if duration_ms:
            self._duration = duration_ms

        self._output.value = True
        self._start_time = time.monotonic_ns()

        return True

    __call__ = trigger

    def step(self):
        if self._start_time is None:
            return

        now = time.monotonic_ns()
        elapsed_ms = (now - self._start_time) / _NS_TO_S * 1000
        if elapsed_ms > self._duration:
            self._output.value = False
            self._start_time = None


class Retrigger:
    """A retrigger helper.

    This handles "re-triggering" an output. This is
    similar to gate, but gate is a continuous on/off, whereas re-trigger
    will hold the line low for a short duration to "re-trigger" the note.
    For example::

        Gate:       __-------
        Re-trigger: __--_----

    Example usage::

        retrigger = Retrigger(DigitalInOut(board.D3))
        retrigger()

        while True:
            retrigger.step()
    """

    def __init__(self, output, duration_ms=15):
        self._output = output
        self._duration = duration_ms
        self._start_time = None

    def retrigger(self, duration_ms=None):
        # TODO: Figure out what to do if the trigger
        # phase is still on-going.
        if self._start_time is not None:
            return False

        # If the value is already low, no need to
        # "retrigger"- just set the output to high
        # and return.
        if self._output.value is False:
            self._output.value = True
            return True

        if duration_ms:
            self._duration = duration_ms

        self._output.value = False
        self._start_time = time.monotonic_ns()

        return True

    __call__ = retrigger

    def step(self):
        if self._start_time is None:
            return

        now = time.monotonic_ns()
        elapsed_ms = (now - self._start_time) / _NS_TO_S * 1000
        if elapsed_ms > self._duration:
            self._output.value = True
            self._start_time = None
