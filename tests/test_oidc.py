import os
import inspect
import sys
import pytest
import json
import vcr
from jwt.exceptions import ExpiredSignatureError

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + "/firebreakq1faas")

from firebreakq1faas.oidc import get_kid, get_public_key, login  # noqa

# Record requests to external services
vcr = vcr.VCR(
    serializer="json",
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode="once",
    match_on=["uri", "method"],
)


@pytest.fixture(scope="session")
def encoded_jwt():
    """This is an encoded_jwt token used for testing
    """
    with open("tests/fixtures/alb_https_oidc_get_root.json", "r") as f:
        return json.load(f)["headers"]["x-amzn-oidc-data"]


@pytest.fixture(scope="session")
def elb_public_key():
    """A public key from an ALB. These rotate so we have it for data
    consistency.
    """
    with open("tests/fixtures/alb_public_key.txt", "r") as f:
        return f.read()


@pytest.fixture(scope="session")
def kid():
    "The Key ID we expect for the above public key"
    return "307a30c3-8280-4ff5-a78d-6bc5263ffbe8"


def test_get_kid(encoded_jwt, kid):
    """Check the Key ID from the encoded_jwt token is what we expect"""
    result = get_kid(encoded_jwt)
    assert kid == result


@vcr.use_cassette()
def test_get_public_key(kid, elb_public_key):
    """Check the public key we get is expected"""
    public_key = get_public_key(kid)
    assert elb_public_key == public_key


@vcr.use_cassette()
def test_login_no_exception(encoded_jwt):
    """When presented with a valid encoded_jwt token the login function
    should not raise an exception"""
    login(encoded_jwt, verify=False)


@vcr.use_cassette()
def test_login_exception(encoded_jwt):
    """If a JWT token has expired the an Exception should be raised."""
    try:
        login(encoded_jwt),
    except ExpiredSignatureError:
        pass
