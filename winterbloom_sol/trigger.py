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


class Trigger:
    """A trigger/retrigger helper.

    This handles "triggering" an output for a short duration. This is
    similar to gate, but gate is a continous on/off, whereas trigger
    is a short pulse of on or off. For example::

        Trigger: ____-____
        Gate:    ____-----

    Example usage::

        trigger = Trigger(DigitalInOut(board.D3))
        trigger()

        while True:
            trigger.step()
    """

    def __init__(self, output, duration=15):
        self._output = output
        self._duration = duration
        self._start_time = None

    def trigger(self, value=True, duration=None):
        # TODO: Figure out what to do if the trigger
        # is still on-going.
        if self._start_time is not None:
            return False

        if duration:
            self._duration = duration
        self._output.value = value
        self._start_time = time.monotonic()

        return True

    __call__ = trigger

    def step(self):
        if self._start_time is None:
            return

        now = time.monotonic()
        elapsed_ms = (now - self._start_time) * 1000
        if elapsed_ms > self._duration:
            self._output.value = not self._output.value
            self._start_time = None
