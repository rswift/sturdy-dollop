#
# WARNING! This function is written for exploration and is of dubious integrity!
#
# DO NOT USE FOR ANYTHING OTHER THAN LEARNING!
#

import logging
import os
from random import choice

#
# tinkerings to explore API Gateway HTTP Lambda Authoriser
#
# https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
#

log_level = os.environ['LOG_LEVEL'] if 'LOG_LEVEL' in os.environ else 'INFO'
logging_levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
logging_level = logging_levels[log_level] if log_level in logging_levels else logging.INFO

logger = logging.getLogger()
logger.setLevel(logging_level)

authorisation_header = "Authorization".lower() # a half hearted search didn't turn up much, but request headers seem to be sent to the function all lower case


def lambda_handler(event, context):
    logger.info(f"{context.function_name} ({context.function_version}) with event: {event}")

    response = { "isAuthorized": False, "context":{}}

    if authorisation_header in event['headers']:
        authorisation_token = event['headers'][authorisation_header]
        logger.debug(f"Received [{authorisation_token}] in header field '{authorisation_header}'")
    else:
        logger.error(f"Authorisation header '{authorisation_header}' not found in request headers, headers received: {[k for k in event['headers'].keys()]}")
        return response # exit here for a tad more clarity...

    if authorisation_token == "random-horse:battery/staple":
        response['isAuthorized'] = choice([True, False])
        response['context']['outcome'] = "Outcome set from a random choice"
    elif authorisation_token == "correct-horse:battery/staple":
        response['isAuthorized'] = True
        response['context']['outcome'] = "Outcome is XKCD"
    else:
        logger.warn(f"Authorisation token [{authorisation_token}] supplied in header field '{authorisation_header}' has not proven itself worthy...")
        response['context']['outcome'] = "Outcome is failed authorisation!"

    logger.debug(f"Authoriser returning: {response=}")
    return response