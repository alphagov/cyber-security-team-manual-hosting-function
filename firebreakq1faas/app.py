from flask import (
    Flask,
    request
)

from slogging import log
app = Flask(__name__)


@app.route("/")
def hello_world():
    """Lambda handler entry point

    :param event: An event from an ALB
    :param context: An AWS context object
    :returns: HTML
    :rtype: str

    """
    log.msg(request.headers)

    response = """<html>
    <head>
    <title>Hello World!</title>
    <style>
    html, body {
    margin: 0; padding: 0;
    font-family: arial; font-weight: 700; font-size: 3em;
    text-align: center;
    }
    </style>
    </head>
    <body>
    <p>Hello World!</p>
    </body>
    </html>"""
    return response
