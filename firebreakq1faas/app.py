import os
from flask import (
    Flask,
    session,
    request,
    send_from_directory,
    render_template,
    redirect,
)
from oidc import login_required, is_logged_in
from slogging import log
import traceback

app = Flask(__name__)
sk = os.getenv("SECRET_KEY", "FALSE")
if sk is not "FALSE":
    app.server_key = sk

mastertitle = "GOV.UK - Cyber Security Team Manual"


@app.route("/var_test")
def var_test():
    return os.getenv("TEST_VAR", "NOT SET")


@app.route("/")
def index():
    return redirect("/index.html", code=302)


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


@app.route("/auth")
def handle_auth():
    if is_logged_in(app):
        return redirect("/index.html", code=302)
    else:
        return redirect("/login", code=302)


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
            "error.html",
            title=f"{mastertitle} - Error",
            error=e,
            govukfrontendver="2.9.0",
        ),
        500,
    )


@app.route("/login")
def send_login():
    return (
        render_template("login.html", title=f"{mastertitle}", govukfrontendver="2.9.0"),
        200,
    )


@app.route("/logout")
def send_logout():
    session.clear()
    return redirect("/login", code=302)


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("static/assets", path)


@app.route("/<path:path>")
@login_required(app)
def send_static(login_details, path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    app.secret_key = "notrandomkey"
    app.config["ENV"] = "development"
    app.config["TESTING"] = True
    app.config["DEBUG"] = True
    app.config["verify_oidc"] = False
    app.run(port=5000)
