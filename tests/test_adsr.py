# Copyright (c) 2019 Alethea Flowers for Winterbloom
# Licensed under the MIT License

from unittest import mock

from winterbloom_sol import adsr


def test_default_state():
    env = adsr.ADSR(0, 0, 0, 0)
    assert env.output == 0.0


@mock.patch("time.monotonic", autospec=True)
def test_cycle(monotonic):
    monotonic.return_value = 0
    env = adsr.ADSR(1.0, 1.0, 0.5, 1.0)

    assert env.output == 0

    env.start()
    assert env.output == 0

    # Halfway point of attack phase
    monotonic.return_value = 0.5
    assert env.output == 0.5

    # End of attack phase
    monotonic.return_value = 1.0
    assert env.output == 1.0

    # Halfway point of decay phase
    monotonic.return_value = 1.5
    assert env.output == 0.75

    # End of decay phase
    monotonic.return_value = 2.0
    assert env.output == 0.5

    # Should sustain indefinitely.
    monotonic.return_value = 10.0
    assert env.output == 0.5

    env.stop()

    # Start of release phase
    assert env.output == 0.5

    # Halfway point of release phase
    monotonic.return_value = 10.5
    assert env.output == 0.25

    # End of release phase
    monotonic.return_value = 11.0
    assert env.output == 0.0


@mock.patch("time.monotonic", autospec=True)
def test_no_attack(monotonic):
    monotonic.return_value = 0
    env = adsr.ADSR(0, 1.0, 0.5, 1.0)

    assert env.output == 0

    # Since there's no attack, starting should
    # put the env at 1.0 and start the decay phase.
    env.start()
    assert env.output == 1.0

    # Halfway point of decay phase.
    monotonic.return_value = 0.5
    assert env.output == 0.75

    # End of decay / start of sustain.
    monotonic.return_value = 1.0
    assert env.output == 0.5


@mock.patch("time.monotonic", autospec=True)
def test_no_decay(monotonic):
    monotonic.return_value = 0
    env = adsr.ADSR(1.0, 0, 0.5, 1.0)

    assert env.output == 0

    env.start()
    assert env.output == 0

    # End of attack. Should be max output.
    monotonic.return_value = 1.0
    assert env.output == 1.0

    # Since there's no decay, it should immediately
    # snap to the sustain level.
    monotonic.return_value = 1.1
    assert env.output == 0.5


@mock.patch("time.monotonic", autospec=True)
def test_no_release(monotonic):
    monotonic.return_value = 0
    env = adsr.ADSR(1.0, 1.0, 0.5, 0.0)

    assert env.output == 0

    env.start()
    # Should be in the sustain phase now.
    monotonic.return_value = 2.0
    assert env.output == 0.5

    # Since there's no release, it should immediately
    # drop to zero.
    env.stop()
    assert env.output == 0
