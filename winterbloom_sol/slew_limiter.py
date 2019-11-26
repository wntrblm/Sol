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

from winterbloom_sol import _utils

# Use nanaseconds for absolute time throughout to avoid losing precision for float
# time over long program duration.
_NS_TO_S = 1000000000


class SlewLimiter:
    """A Slew Limiter.

    The slew limiter's rate are set at creation time and can be modified at any
    time::

        slew = sol.SlewLimiter(
            rate=0.1,  # seconds
        )

        slew.rate = 1.0  # seconds


    After that, you can set the target value for the limiter::

        slew.target = state.cc[1] * 10.0

    The slew's output will then available to be used as a CV output::

        outputs.cv_b = slew.output

    """

    def __init__(self, rate):
        self.rate = rate
        self._last = None
        self._target = None
        self._set_time = 0

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        # Don't limit for the initial value.
        if self._last is None:
            self._last = value
        else:
            self._last = self.output

        # Ignore duplicate target values to avoid
        # re-starting the slew.
        if self._target is not None and _utils.isclose(
            value, self._target, rel_tol=1e-05
        ):
            return

        print(value)
        self._target = value
        self._set_time = time.monotonic_ns()

    @property
    def output(self):
        if self._target is None:
            return 0

        now = time.monotonic_ns()
        rate_s = self.rate * _NS_TO_S
        delta = min(1.0, (now - self._set_time) / rate_s)

        return _utils.lerp(self._last, self._target, delta)
