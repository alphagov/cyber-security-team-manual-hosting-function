import os
import inspect
import sys
import re
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/firebreak-q1-faas')
from firebreakq1faas.logging import (
    add_timestamp,
    log
)  # noqa


def test_addtimestamp_adds_key():
    event_dict = add_timestamp(None, None, {})
    assert("timestamp" in event_dict)


def test_addtimestamp_in_iso8601():
    event_dict = add_timestamp(None, None, {})
    iso8601 = r"^[\d]{4}-[\d]{2}-[\d]{2}T[\d]{2}:[\d]{2}:[\d]{2}\.[\d]{6}"
    match = re.match(iso8601, event_dict["timestamp"])
    assert(match)
