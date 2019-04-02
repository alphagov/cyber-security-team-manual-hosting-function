from structlog import get_logger
from structlog.processors import JSONRenderer
from datetime import datetime


def add_timestamp(_, __, event_dict):
    """Add ISO8601 timestamp to logging objects

    :param _: Unused
    :param __: Unused
    :param event_dict: Logging dictionary to add timestamp too.
    :returns: Updated logging dict
    :rtype: dict

    """
    event_dict["timestamp"] = datetime.utcnow().isoformat()
    return event_dict


log = get_logger(
    processors=[
        add_timestamp,
        JSONRenderer(indent=1, sort_keys=True)])
