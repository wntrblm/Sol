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


class ADSR:
    """An ADSR envelope generator.

    The ADSR's parameters are set at creation time and can be modified at any
    time::

        adsr = sol.ADSR(
            attack=0.1,  # seconds
            decay=0.01,  # seconds
            sustain=0.8,  # percent
            release=1.0,  # seconds
        )

        adsr.release = 0.5

    Once set, the ADSR must to told when start its cycle, typically when a note
    is triggered::

        if sol.should_trigger_note(...):
            adsr.start()

    And it must be told when to move from the sustain to the release period::

        if not state.note:
            adsr.stop()

    The ADSR's output is then available to be used as a CV output. It is a normalized
    (0-1.0) value so it must be scaled::

        outputs.cv_b = adsr.output * 10.0

    """

    def __init__(self, attack, decay, sustain, release):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self._trigger_time = None
        self._release_time = None

    def start(self):
        self._trigger_time = time.monotonic()
        self._release_time = None

    def stop(self):
        if self._trigger_time is not None and self._release_time is None:
            self._release_time = time.monotonic()

    def _calculate_start_phase_level(self, now):
        attack_end = self._trigger_time + self.attack

        if self.attack == 0:
            attack_percent = 1.1  # No attack phase
        else:
            attack_percent = (now - self._trigger_time) / self.attack

        if self.decay == 0:
            decay_percent = 1.0
        else:
            decay_percent = (now - attack_end) / self.decay

        if attack_percent <= 1.0:
            return _utils.lerp(0, 1.0, attack_percent)
        elif decay_percent >= 0.0:
            return _utils.lerp(1.0, self.sustain, min(decay_percent, 1.0))

    def _calculate_stop_phase_level(self, start_phase_level, now):
        if self.release == 0:
            release_percent = 1.0
        else:
            release_percent = (now - self._release_time) / self.release

        return _utils.lerp(start_phase_level, 0, min(release_percent, 1.0))

    @property
    def output(self):
        if self._trigger_time is None:
            return 0

        now = time.monotonic()

        # We calculate the values for the start phase even when
        # we're in the stop phase so that the stop phase knows
        # what level to start its interpolation from.
        # In order to "freeze" the last level output from the
        # start phase, use self._release_time instead of now
        # if it's set.
        start_phase_level = self._calculate_start_phase_level(self._release_time or now)

        if not self._release_time:
            return start_phase_level

        return self._calculate_stop_phase_level(start_phase_level, now)
