# Copyright (c) 2019 Alethea Flowers for Winterbloom
# Licensed under the MIT License

from unittest import mock

from winterbloom_sol import trigger

_NS_TO_S = 1000000000


class DigitalInOutStub:
    def __init__(self):
        self.value = False


@mock.patch("time.monotonic_ns", autospec=True)
def test_trigger_basic(time_monotonic):
    output = DigitalInOutStub()
    trig = trigger.Trigger(output)

    time_monotonic.return_value = 0
    trig()

    assert output.value is True

    time_monotonic.return_value = 0.014 * _NS_TO_S
    trig.step()
    assert output.value is True

    time_monotonic.return_value = 0.016 * _NS_TO_S
    trig.step()
    assert output.value is False


def test_overlapping_trigger():
    output = DigitalInOutStub()
    trig = trigger.Trigger(output)

    assert trig(True)
    assert not trig(True)


@mock.patch("time.monotonic_ns", autospec=True)
def test_trigger_custom_duration(time_monotonic):
    output = DigitalInOutStub()
    trig = trigger.Trigger(output)

    time_monotonic.return_value = 0
    trig(duration_ms=50)

    time_monotonic.return_value = 0.049 * _NS_TO_S
    trig.step()
    assert output.value is True

    time_monotonic.return_value = 0.051 * _NS_TO_S
    trig.step()
    assert output.value is False


def test_empty_step():
    output = DigitalInOutStub()
    trig = trigger.Trigger(output)

    trig.step()

    assert output.value is False
