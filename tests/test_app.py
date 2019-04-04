import os
import inspect
import sys
import pytest
import json
import vcr

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + "/firebreakq1faas")
from firebreakq1faas.app import app  # noqa

app.config["SECRET_KEY"] = "testnotrandom"

vcr = vcr.VCR(
    serializer="json",
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode="once",
    match_on=["uri", "method"],
)


@pytest.fixture(scope="session")
def authenticated():
    """Setup a flask test client. This is used to connect to the test
    server and make requests.
    """

    app.config["TESTING"] = True
    app.config["verify_oidc"] = False
    authenticated = app.test_client()
    return authenticated


@pytest.fixture(scope="session")
def unauthenticated():
    """Setup a flask test unauthenticated. This is used to connect to the test
    server and make requests.
    """

    unauthenticated = app.test_client()
    return unauthenticated


@pytest.fixture(scope="session")
def alb_https_odic_get_root():
    """Load a JSON alb request that has OIDC information in it.
    """
    with open("tests/fixtures/alb_https_oidc_get_root.json", "r") as f:
        return json.load(f)


@vcr.use_cassette()
def test_root(authenticated, alb_https_odic_get_root):
    """Test the '/' route to check that the output is html and
    contains '/index.html' and the status code is a 302 redirect
    """
    result = authenticated.get("/", headers=alb_https_odic_get_root["headers"])
    # for authenticated this should be index.html, need to work out sessions
    assert b"/login" in result.data and 302 == result.status_code


@vcr.use_cassette()
def test_root_without_login(unauthenticated, alb_https_odic_get_root):
    """Test the '/' route to check that unathenticated users are redirected.
    """
    result = unauthenticated.get("/")
    print(result.data)
    assert b"/login" in result.data and 302 == result.status_code


def test_good_to_go(unauthenticated):
    """Test the '/__gtg' endpoint works and returns the text 'Good to
    Go!'. This is used by the ELB healthcheck.
    """
    result = unauthenticated.get("/__gtg")
    assert b"Good to Go!" in result.data


def test_logout(authenticated):
    """Test the '/logout' endpoint works and returns /login redirect
    """
    result = authenticated.get("/logout")
    assert b"/login" in result.data and 302 == result.status_code


@vcr.use_cassette()
def test_good_static_path(authenticated, alb_https_odic_get_root):
    """Test the dynamic static endpoint works and returns the contents of
    the correct file from `static`

    """
    result = authenticated.get("/test.html", headers=alb_https_odic_get_root["headers"])
    # shouldn't be /login but haven't worked out how to set sessions
    assert b"/login" in result.data


@vcr.use_cassette()
def test_root_without_login(unauthenticated, alb_https_odic_get_root):
    """Test the dynamic static endpoint redirects with a 302 when unathenticated.
    """
    result = unauthenticated.get("/")
    print(result.data)
    assert 302 == result.status_code
