#
# WARNING! This function is written for exploration and is mahoosively insecure
#
# DO NOT USE FOR ANYTHING OTHER THAN LEARNING!
#

import logging
import os

log_level = os.environ['LOG_LEVEL'] if 'LOG_LEVEL' in os.environ else 'INFO'
logging_levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
logging_level = logging_levels[log_level] if log_level in logging_levels else logging.INFO

logger = logging.getLogger()
logger.setLevel(logging_level)


def lambda_handler(event, context):
    logger.info(f"{context.function_name} ({ context.function_version}) with event: {event}")

    logger.warn("WARNING: This function returns the entire contents of the 'event' object received by the function, straight back to the client!")
    return {"event": event}