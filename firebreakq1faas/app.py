from flask import Flask, request, send_from_directory, render_template, redirect
from oidc import login_required
from slogging import log
import traceback

app = Flask(__name__)

mastertitle = "GOV.UK - Cyber Security Team Manual"


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
    font-family: arial; font-weight: 700; font-size: 0.8em;
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
    font-family: arial; font-weight: 700; font-size: 0.8em;
    text-align: center;
    }
    </style>
    </head>
    <body>
    <p>Good to Go!</p>
    </body>
    </html>"""
    return response


@app.route("/error")
def raise_error():
    raise Exception("Bad Error")


@app.errorhandler(404)
def handle_bad_request(e):
    return (
        render_template(
            "error.html",
            title=f"{mastertitle} - Error",
            error=e,
            govukfrontendver="2.9.0",
        ),
        404,
    )


@app.errorhandler(500)
def handle_bad_request(e):
    return (
        render_template(
            "error.html", title=f"{mastertitle} - Error", govukfrontendver="2.9.0"
        ),
        500,
    )


@app.route("/login")
@login_required(app)
def send_login(login_details, path):
    return redirect("/index.html", code=302)


@app.route("/auth")
def send_auth():
    return (
        render_template("auth.html", title=f"{mastertitle}", govukfrontendver="2.9.0"),
        200,
    )


@app.route("/<path:path>")
@login_required(app)
def send_static(login_details, path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(port=5000)
