# Copyright (c) 2019 Alethea Flowers for Winterbloom
# Licensed under the MIT License

from unittest import mock

from winterbloom_sol import slew_limiter

_NS_TO_S = 1000000000


def test_default_state():
    slew = slew_limiter.SlewLimiter(rate=1.0)
    assert slew.target is None
    assert slew.output == 0


@mock.patch("time.monotonic_ns", autospec=True)
def test_basic(monotonic_ns):
    monotonic_ns.return_value = 0
    slew = slew_limiter.SlewLimiter(rate=1.0)

    assert slew.output == 0

    # Initial value should immediately set.
    slew.target = 5.0
    assert slew.output == 5.0

    # Subsequent values should slew.
    slew.target = 10.0
    assert slew.output == 5.0
    monotonic_ns.return_value = 0.5 * _NS_TO_S  # Halfway through the rate.
    assert slew.output == 7.5

    # Switching the value during a slew period should interpolate from
    # the current slew value to the new target. That is to say that
    # in this case it should interpolate from 7.5 (the current slew output)
    # not 10.0.
    slew.target = 2.5
    monotonic_ns.return_value = (
        1.0 * _NS_TO_S
    )  # Halfway through the rate with the new values.
    assert slew.output == 5.0

    # Setting the same target again during the slew period should not
    # restart it.
    slew.target = 2.5
    monotonic_ns.return_value = 1.5 * _NS_TO_S
    assert slew.output == 2.5
