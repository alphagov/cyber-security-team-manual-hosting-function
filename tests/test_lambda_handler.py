import os
import inspect
import sys
import pytest
import json
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/firebreak-q1-faas')
from firebreakq1faas.lambda_handler import lambda_handler  # noqa


def test_lambda_handler():
    result = lambda_handler(None, None)
    assert(result == 'Hello, world!')
