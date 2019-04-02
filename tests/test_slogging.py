import os
import inspect
import sys
import re
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/firebreakq1faas')
from firebreakq1faas.slogging import (
    add_timestamp,
    log
)  # noqa


def test_addtimestamp_adds_key():
    """We should add a 'timestamp' key to the logging messages."""
    event_dict = add_timestamp(None, None, {})
    assert("timestamp" in event_dict)


def test_addtimestamp_in_iso8601():
    """The timestamp should be iso8601 formatted."""
    event_dict = add_timestamp(None, None, {})
    iso8601 = r"^[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}\.[\d]{6}"
    match = re.match(iso8601, event_dict["timestamp"])
    assert(match)
