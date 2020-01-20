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

import math
import time

import micropython

# Use nanaseconds for absolute time throughout to avoid losing precision for float
# time over long program duration.
_NS_TO_S = 1000000000


class _PhaseAccumulator:
    def __init__(self, frequency):
        self.frequency = frequency
        self._phase = 0
        self._last_time = time.monotonic_ns()

    @micropython.native
    def _accumulate(self):
        current_time = time.monotonic_ns()
        time_delta = (current_time - self._last_time) / _NS_TO_S
        self._last_time = current_time
        phase_accum = time_delta * self.frequency
        self._phase += phase_accum
        while self._phase > 1.0:
            self._phase -= 1.0


class SineLFO(_PhaseAccumulator):
    def __init__(self, frequency):
        super(SineLFO, self).__init__(frequency)

    @property
    def output(self):
        self._accumulate()
        return math.sin(math.pi * 2 * self._phase)


class SawtoothLFO(_PhaseAccumulator):
    def __init__(self, frequency):
        super(SawtoothLFO, self).__init__(frequency)

    @property
    def output(self):
        self._accumulate()
        return (((self._phase * 2) % 1) * 2) - 1.0


class TriangleLFO(_PhaseAccumulator):
    def __init__(self, frequency):
        super(TriangleLFO, self).__init__(frequency)

    @property
    def output(self):
        self._accumulate()
        return (abs(self._phase - 0.5) * 4.0) - 1.0
