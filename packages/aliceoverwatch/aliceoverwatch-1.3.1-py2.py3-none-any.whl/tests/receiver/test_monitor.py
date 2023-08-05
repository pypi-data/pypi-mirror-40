#!/usr/bin/env python

""" Tests for the ZMQ receiver monitor.

.. codeauthor:: Raymond Ehlers <raymond.ehlers@yale.edu>, Yale University
"""

import logging
import os
import pendulum
import pytest

logger = logging.getLogger(__name__)

from overwatch.receiver import monitor

@pytest.mark.parametrize("timestamp, expected", [
    ("1541792926", 1541792926),
    ("hello world", -1),
    ("invalidFile", -1),
], ids = ["Standard timestamp", "Invalid timestamp", "Invalid file"])
def testGetHeartbeatFailures(loggingMixin, mocker, timestamp, expected):
    """ Test retrieving a heartbeat from a file. """
    subsystem = "EMC"
    mOpen = mocker.mock_open(read_data = timestamp)
    mocker.patch("overwatch.receiver.monitor.open", mOpen)

    if timestamp == "invalidFile":
        # We don't need to configure the values - they don't really matter. We just want this
        # exception to be raised.
        mOpen.side_effect = IOError()

    result = monitor.getHeartbeat(subsystem = subsystem)

    mOpen.assert_called_once_with(os.path.join(monitor.parameters["receiverData"], "heartbeat.{subsystem}Receiver".format(subsystem = subsystem)), "r")
    assert result == expected

@pytest.mark.parametrize("inputTimestamps, expectedTimestamps, expectedDeadReceivers", [
    ([{"EMC": 1000, "HLT": 1010}, {"EMC": 1020, "HLT": 1030}], 100, (set(), set())),
    ([{"EMC": 1000, "HLT": 1010}, {"EMC": 1020, "HLT": 1030}], 320, (set(["EMC", "HLT"]), set(["EMC", "HLT"]))),
    ([{"EMC": 1000, "HLT": 1010}, {"EMC": 1020, "HLT": 1030}], [{"EMC": 1010, "HLT": 2020}, {"EMC": 1030, "HLT": 2040}], (set(["HLT"]), set(["HLT"]))),
    ([{"EMC": 1000, "HLT": 1010}, {"EMC": 1020, "HLT": 1030}], [{"EMC": 1010, "HLT": 1020}, {"EMC": 1030, "HLT": 2040}], (set(), set(["HLT"]))),
    ([{"EMC": 1000, "HLT": 1010}, {"EMC": 1020, "HLT": 1030}], [{"EMC": 1010, "HLT": 2020}, {"EMC": 1030, "HLT": 1040}], (set(["HLT"]), set())),
], ids = ["All alive", "All dead", "Only HLT receiver died", "HLT died after one check", "HLT receiver recovered"])
def testCheckHeartbeat(loggingMixin, mocker, inputTimestamps, expectedTimestamps, expectedDeadReceivers):
    """ Test checking the heartbeat of given subsystems. """
    # Setup subsystems
    # Normally, we could just get the subsystems by calling `el.keys() for el in inputTimestamps`.
    # Hoewver, specifing the ``mockInputTimestamps`` and ``expectedTimestamps`` properly depends on the
    # order in which the values are insert, which in turn depends on the order in which the subsystems
    # are interated over. Py2 dict keys don't preserve order, so these tests will sometimes fail. By
    # specifying the order in the ``subsystems`` list, we don't have to get the keys from the dict.
    subsystems = ["EMC", "HLT"]
    monitor.parameters["subsystemList"] = subsystems
    # Setup input values
    # Converts into [emc1, hlt1, emc2, hlt2] so that the return values are in the appropriate order.
    mockInputTimestamps = [el[subsystem] for el in inputTimestamps for subsystem in subsystems]
    # Spot check the third element.
    assert mockInputTimestamps[2] == inputTimestamps[1]["EMC"]
    # Sanity check to ensure that we haven't missed any subsystems
    assert set(subsystems) == set(inputTimestamps[1].keys())
    # Setup expected values
    if isinstance(expectedTimestamps, int):
        logger.debug("Using fixed offset.")
        offset = expectedTimestamps
        expectedSource = inputTimestamps
    else:
        logger.debug("Using expected timestamps specified in the parametrization.")
        offset = 0
        expectedSource = expectedTimestamps
    expectedTimestamps = [pendulum.from_timestamp(el[subsystem] + offset, tz = "Europe/Zurich") for el in expectedSource for subsystem in subsystems]
    # Setup mocks using expected input and output values.
    mHeartbeat = mocker.MagicMock(side_effect = mockInputTimestamps)
    mocker.patch("overwatch.receiver.monitor.getHeartbeat", mHeartbeat)
    mPendulumNow = mocker.MagicMock(side_effect = expectedTimestamps)
    mocker.patch("overwatch.receiver.monitor.pendulum.now", mPendulumNow)

    deadReceivers = set()
    # Make the check as many times as specified.
    for edr in expectedDeadReceivers:
        deadReceivers = monitor.checkHeartbeat(deadReceivers)
        # The assertion here lets us test each step of checking the heartbeat.
        assert deadReceivers == edr

