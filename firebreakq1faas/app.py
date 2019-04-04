from flask import Flask, request, send_from_directory, render_template, redirect
from oidc import login_required
from slogging import log
import traceback

app = Flask(__name__)

mastertitle = "GOV.UK - Cyber Security Team Manual"


@app.route("/")
def index():
    print(request.cookies)
    if "AWSELBAuthSessionCookie" in request.cookies:
        return redirect("/index.html", code=302)
    else:
        return redirect("/login", code=302)


@app.route("/__gtg")
def good_to_go():
    """An unauthenticated route for health checks
    """
    log.msg("gtg")
    response = "Good to Go!"
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
def send_login():
    return (
        render_template("login.html", title=f"{mastertitle}", govukfrontendver="2.9.0"),
        200,
    )


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("static/assets", path)


@app.route("/<path:path>")
@login_required(app)
def send_static(login_details, path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.run(port=5000)
