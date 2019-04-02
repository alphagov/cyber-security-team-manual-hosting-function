import os
import inspect
import sys
import pytest
import json
import vcr
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/firebreakq1faas')
from firebreakq1faas.app import app  # noqa


vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='tests/fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)


@pytest.fixture(scope="session")
def client():
    app.config['TESTING'] = True
    app.config['verify_oidc'] = False
    client = app.test_client()
    return client


@pytest.fixture(scope="session")
def alb_https_odic_get_root():
    with open("tests/fixtures/alb_https_oidc_get_root.json", "r") as f:
        return json.load(f)


@vcr.use_cassette()
def test_root(client, alb_https_odic_get_root):
    result = client.get("/", headers=alb_https_odic_get_root['headers'])
    assert b"Hello" in result.data


def test_good_to_go(client):
    result = client.get("/__gtg")
    assert b"Good to Go!" in result.data
