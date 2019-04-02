from slogging import log


def lambda_handler(event, context):
    """Lambda handler entry point

    :param event: An event from an ALB
    :param context: An AWS context object
    :returns: HTML
    :rtype: str

    """
    log.msg('Test log event')
    return "Hello, world!"
