import os
import inspect
import sys
import pytest
import json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + "/firebreakq1faas")
from firebreakq1faas.lambda_handler import lambda_handler  # noqa


@pytest.fixture(scope="session")
def alb_https_odic_get_root():
    """Load a JSON alb request that has OIDC information in it.
    """
    with open("tests/fixtures/alb_https_oidc_get_root.json", "r") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def get_root(alb_https_odic_get_root):
    """Run a request through the lambda_handler and save the response for
    later testing.
    """
    return lambda_handler(alb_https_odic_get_root, None)


def test_lambda_handler_returns_dict(get_root):
    """lambda handler should return a dict to AWS' calling function"""
    assert isinstance(get_root, dict)


def test_lambda_handler_dict_has_body(get_root):
    """The response has to have a 'body' key"""
    assert "body" in get_root


def test_lambda_handler_dict_has_statusCode(get_root):
    """The response has to have a 'statusCode' key"""
    assert "statusCode" in get_root


def test_lambda_handler_dict_has_headers(get_root):
    """The response has to have a 'headers' key"""
    assert "headers" in get_root


def test_lambda_handler_dict_has_content_type(get_root):
    """The response has to have a 'Content-Type' key as a child of the
    headers key"""
    assert "Content-Type" in get_root["headers"]
