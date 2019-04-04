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

    return {
      "statusCode": 302,
      "headers": {
        "Content-Type": "text/html; charset=utf-8",
        "Location": "https://www.google.com"
      },
      "statusDescription": "302 Found",
      "body": "",
      "isBase64Encoded": false
    }
    #return serverless_wsgi.handle_request(app.app, event, context)
