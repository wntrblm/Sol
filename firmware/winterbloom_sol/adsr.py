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

import micropython
from winterbloom_sol import _utils

# Use nanaseconds for absolute time throughout to avoid losing precision for float
# time over long program duration.
_NS_TO_S = 1000000000


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
        # Envelope state: 0 - idle, 1 - attack, 2 - decay, 3 - sustain, 4 - release.
        self._state = 0
        self._state_time = 0
        self._accum = 0.0
        self._last_update = 0
        self._release_start_level = 0

    def start(self):
        self._state = 1
        self._state_time = 0
        self._last_update = time.monotonic_ns()

    def stop(self):
        if self._state == 4 or self._state == 0:
            return
        self._state = 4
        self._state_time = 0
        self._release_start_level = self._accum
        self._last_update = time.monotonic_ns()

    @property
    def output(self):
        now = time.monotonic_ns()
        dt = (now - self._last_update) / _NS_TO_S
        self._state_time += dt

        # Idle
        if self._state == 0:
            self._accum = 0

        # Attack
        if self._state == 1:
            if self.attack == 0:
                self._accum = 1.0
                self._state = 2
            else:
                self._accum += 1.0 / self.attack * dt
                if self._accum > 1.0 or self._state_time > self.attack:
                    # Special case for attack- since the ADSR can be
                    # re-triggered, the attack phase can take less
                    # time than expected. Figure out how much extra time
                    # there is an carry it over to the decay state.
                    expected_val = 1.0 / self.attack * self._state_time
                    self._accum = 1.0
                    self._state = 2
                    # Leave remaining state time so that if an update
                    # covers some time in attack and some time in decay
                    # the value can be correctly calculated
                    self._state_time = dt = self._state_time - min(self.attack * expected_val, self.attack)
        
        # Decay
        if self._state == 2:
            if self.decay == 0:
                self._accum = self.sustain
                self._state = 3
            else:
                self._accum -= (1.0 - self.sustain) / self.decay * dt
                if self._accum < self.sustain or self._state_time > self.decay:
                    self._accum = self.sustain
                    self._state_time = 0
                    self._state = 3
        
        # Sustain
        elif self._state == 3:
            self._accum = self.sustain

        # Release
        elif self._state == 4:
            if self.release == 0:
                self._accum = 0.0
                self._state = 0
            else:
                self._accum -= self._release_start_level / self.release * dt
                if self._accum < 0.0 or self._state_time > self.release:
                    self._accum = 0.0
                    self._state_time = 0
                    self._state = 0
        
        self._last_update = now
        return self._accum


class DisjointADSR:

    def __init__(self, attack, decay, sustain, release):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self._trigger_time = None
        self._release_time = None

    def start(self):
        self._trigger_time = time.monotonic_ns()
        self._release_time = None

    def stop(self):
        if self._trigger_time is not None and self._release_time is None:
            self._release_time = time.monotonic_ns()

    @micropython.native
    def _calculate_start_phase_level(self, now):
        attack_s = self.attack * _NS_TO_S
        attack_end = self._trigger_time + attack_s

        if attack_s == 0:
            attack_percent = 1.1  # No attack phase
        else:
            attack_percent = (now - self._trigger_time) / attack_s

        decay_s = self.decay * _NS_TO_S
        if decay_s == 0:
            decay_percent = 1.0
        else:
            decay_percent = (now - attack_end) / decay_s

        if attack_percent <= 1.0:
            return _utils.lerp(0, 1.0, attack_percent)
        elif decay_percent >= 0.0:
            return _utils.lerp(1.0, self.sustain, min(decay_percent, 1.0))

    @micropython.native
    def _calculate_stop_phase_level(self, start_phase_level, now):
        release_s = self.release * _NS_TO_S
        if release_s == 0:
            release_percent = 1.0
        else:
            release_percent = (now - self._release_time) / release_s

        return _utils.lerp(start_phase_level, 0, min(release_percent, 1.0))

    @property
    def output(self):
        if self._trigger_time is None:
            return 0

        now = time.monotonic_ns()

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
