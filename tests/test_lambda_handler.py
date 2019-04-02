import os
import inspect
import sys
import pytest
import json
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/firebreakq1faas')
from firebreakq1faas.lambda_handler import lambda_handler  # noqa


@pytest.fixture
def alb_http_get():
    with open("tests/fixtures/alb_http_get.json", "r") as f:
        return json.load(f)


@pytest.fixture
def get_root(alb_http_get):
    return lambda_handler(alb_http_get, None)


def test_lambda_handler_returns_dict(get_root):
    assert(isinstance(get_root, dict))


def test_lambda_handler_dict_has_body(get_root):
    assert("body" in get_root)


def test_lambda_handler_dict_has_statusCode(get_root):
    assert("statusCode" in get_root)


def test_lambda_handler_dict_has_headers(get_root):
    assert("headers" in get_root)


def test_lambda_handler_dict_has_content_type(get_root):
    assert("Content-Type" in get_root['headers'])
