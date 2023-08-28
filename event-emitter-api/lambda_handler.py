import json
import logging
import os
from typing import Callable, NamedTuple

import boto3

from api_responses import FAILED_TO_PUBLISH_TO_SNS_RESPONSE, SUCCESS_RESPONSE, INVALID_ENDPOINT_RESPONSE
from validator import validate_request, validate_create_purchase_order_payload, validate_create_sales_order_payload, \
    ValidationResult, validate_create_product_payload


class EventConfig(NamedTuple):
    subject: str
    validator: Callable[[str], ValidationResult]


PATH_CONFIG_MAP = {
    '/purchase-orders': EventConfig('NEW_PURCHASE_ORDER_SCHEDULED', validate_create_purchase_order_payload),
    '/sales-orders': EventConfig('NEW_SALES_ORDER_SCHEDULED', validate_create_sales_order_payload),
    '/product': EventConfig('NEW_PRODUCT_SCHEDULED', validate_create_product_payload)
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Starting lambda_handler")
    logger.info(f"Event: {event}")
    sns = boto3.client('sns')
    topic_arn = os.environ.get('TOPIC_ARN')
    if not topic_arn:
        raise ValueError("TOPIC_ARN environment variable not set")

    logger.info(f"Received event: {event}")
    validation_result = validate_request(event)
    if not validation_result:
        return validation_result.response

    path = event.get('path')
    event_config = PATH_CONFIG_MAP.get(path)

    if not event_config:
        return INVALID_ENDPOINT_RESPONSE
    is_event_valid_result = event_config.validator(event['body'])
    if not is_event_valid_result:
        return is_event_valid_result.response
    logger.info(f"Event is valid: {is_event_valid_result}")
    request_data = json.loads(event['body'])
    logger.info(f"Publishing to SNS:{event_config}: {request_data}")
    try:
        sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(request_data),
            Subject=event_config.subject
        )
    except Exception as e:
        logger.error(f"Error publishing to SNS: {e}")
        return FAILED_TO_PUBLISH_TO_SNS_RESPONSE
    logger.info(f"Published to SNS:{event_config}: {request_data}")
    return SUCCESS_RESPONSE
