# Tests

Tests are written for [pytest](https://docs.pytest.org/en/latest/)

We use [tox](https://tox.readthedocs.io/en/latest/) as our test runner.
Filenames mirror those from [firebreakq1faas](../firebreakq1faas)


Run the tests whenever a file changes:

``` shell
while inotifywait -r -e modify tests firebreakq1faas ; do clear; tox; done
```

# test_app.py

You can find information for testing flask applications at http://flask.pocoo.org/docs/1.0/testing/

# fixtures
Test data is kept in this directory.

# fixtures/casstets
Are used by the [pyvcr](https://vcrpy.readthedocs.io/en/latest/usage.html) library to store network requests and responses with the test suite.
