from flask import Flask, request, send_from_directory
from oidc import login_required
from slogging import log
import traceback

app = Flask(__name__)


@app.route("/")
@login_required(app)
def hello_world(login_details):
    """ A page to say hello to the world
    """
    log.msg("hello_world")
    response = f"""<html>
    <head>
    <title>Hello World!</title>
    <style>
    html, body {{
    margin: 0; padding: 0;
    font-family: arial; font-weight: 700; font-size: 3em;
    text-align: center;
    }}
    </style>
    </head>
    <body>
    <p>Hello World!</p>
    <img src="{login_details['picture']}">
    </body>
    </html>"""
    return response


@app.route("/__gtg")
def good_to_go():
    """An unauthenticated route for health checks
    """
    log.msg("gtg")
    response = """<html>
    <head>
    <title>Good to Go!</title>
    <style>
    html, body {
    margin: 0; padding: 0;
    font-family: arial; font-weight: 700; font-size: 3em;
    text-align: center;
    }
    </style>
    </head>
    <body>
    <p>Good to Go!</p>
    </body>
    </html>"""
    return response


@app.route("/<path:path>")
@login_required(app)
def send_static(login_details, path):
    print(path)
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(port=5000)
