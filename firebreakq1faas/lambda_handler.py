import os
import app
import serverless_wsgi
from slogging import log


def lambda_handler(event, context):
    """Lambda handler entry point

    :param event: An event from an ALB
    :param context: An AWS context object
    :returns: An AWS ALB event
    :rtype: dict


    """
    print(event)
    print(context)

    sk = os.getenv("SECRET_KEY", "FALSE")
    if sk is not "FALSE":
        app.server_key = sk

    return serverless_wsgi.handle_request(app.app, event, context)
