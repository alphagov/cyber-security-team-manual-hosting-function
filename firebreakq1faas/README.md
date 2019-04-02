# lambda_handler.py
Entry point for lambda function.

# app.py
A basic [flask](http://flask.pocoo.org/) application.

# slogging.py
A file to setup our structured logging.

# oidc.py
A very basic implementation of OIDC. This is used for authentication.
https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html

# Tests

Tests can be found in the [test](../tests) directory.


# Logging

We are using [structlog](https://www.structlog.org/en/stable/index.html) for our logging handler.

We will use JSON to format the logging output.
