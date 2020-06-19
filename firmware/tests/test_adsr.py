# Copyright (c) 2019 Alethea Flowers for Winterbloom
# Licensed under the MIT License

from unittest import mock

from winterbloom_sol import adsr

_NS_TO_S = 1000000000


class TestADSR:
    def test_default_state(self):
        env = adsr.ADSR(0, 0, 0, 0)
        assert env.output == 0.0


    @mock.patch("time.monotonic_ns", autospec=True)
    def test_cycle(self, monotonic_ns):
        monotonic_ns.return_value = 0
        env = adsr.ADSR(1.0, 1.0, 0.5, 1.0)

        assert env.output == 0

        env.start()
        assert env.output == 0

        # Halfway point of attack phase
        monotonic_ns.return_value = 0.5 * _NS_TO_S
        assert env.output == 0.5

        # End of attack phase
        monotonic_ns.return_value = 1.0 * _NS_TO_S
        assert env.output == 1.0

        # Halfway point of decay phase
        monotonic_ns.return_value = 1.5 * _NS_TO_S
        assert env.output == 0.75

        # End of decay phase
        monotonic_ns.return_value = 2.0 * _NS_TO_S
        assert env.output == 0.5

        # Should sustain indefinitely.
        monotonic_ns.return_value = 10.0 * _NS_TO_S
        assert env.output == 0.5

        env.stop()

        # Start of release phase
        assert env.output == 0.5

        # Halfway point of release phase
        monotonic_ns.return_value = 10.5 * _NS_TO_S
        assert env.output == 0.25

        # End of release phase
        monotonic_ns.return_value = 11.0 * _NS_TO_S
        assert env.output == 0.0


    @mock.patch("time.monotonic_ns", autospec=True)
    def test_no_attack(self, monotonic_ns):
        monotonic_ns.return_value = 0
        env = adsr.ADSR(0, 1.0, 0.5, 1.0)

        assert env.output == 0

        # Since there's no attack, starting should
        # put the env at 1.0 and start the decay phase.
        env.start()
        assert env.output == 1.0

        # Halfway point of decay phase.
        monotonic_ns.return_value = 0.5 * _NS_TO_S
        assert env.output == 0.75

        # End of decay / start of sustain.
        monotonic_ns.return_value = 1.0 * _NS_TO_S
        assert env.output == 0.5


    @mock.patch("time.monotonic_ns", autospec=True)
    def test_no_decay(self, monotonic_ns):
        monotonic_ns.return_value = 0
        env = adsr.ADSR(1.0, 0, 0.5, 1.0)

        assert env.output == 0

        env.start()
        assert env.output == 0

        # End of attack. Should be max output.
        monotonic_ns.return_value = 1.0 * _NS_TO_S
        assert env.output == 1.0

        # Since there's no decay, it should immediately
        # snap to the sustain level.
        monotonic_ns.return_value = 1.1 * _NS_TO_S
        assert env.output == 0.5


    @mock.patch("time.monotonic_ns", autospec=True)
    def test_no_release(self, monotonic_ns):
        monotonic_ns.return_value = 0
        env = adsr.ADSR(1.0, 1.0, 0.5, 0.0)

        assert env.output == 0

        env.start()
        # Should be in the sustain phase now.
        monotonic_ns.return_value = 2.0 * _NS_TO_S
        assert env.output == 0.5

        # Since there's no release, it should immediately
        # drop to zero.
        env.stop()
        assert env.output == 0
