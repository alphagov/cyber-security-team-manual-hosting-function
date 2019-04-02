# Tests

Tests are written for [pytest](https://docs.pytest.org/en/latest/)

We use [tox](https://tox.readthedocs.io/en/latest/) as our test runner.
Filenames mirror those from [firebreakq1faas](../firebreakq1faas)


Run the tests whenever a file changes:

``` shell
while inotifywait -r -e modify tests firebreakq1faas ; do clear; tox; done
```
