import os
import inspect
import sys
import pytest
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/firebreakq1faas')
from firebreakq1faas.app import app  # noqa


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client


def test_root(client):
    result = client.get("/")
    assert b"Hello" in result.data
