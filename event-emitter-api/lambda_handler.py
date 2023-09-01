import json
import logging
import os
from typing import Callable, NamedTuple

import boto3

from api_responses import FAILED_TO_PUBLISH_TO_SNS_RESPONSE, SUCCESS_RESPONSE, INVALID_ENDPOINT_RESPONSE
from common.events.event_manager import EventManager
from common.events.events import EventType
from validator import validate_request, validate_create_purchase_order_payload, validate_create_sales_order_payload, \
    ValidationResult, validate_create_product_payload


class EventConfig(NamedTuple):
    subject: EventType
    validator: Callable[[str], ValidationResult]


PATH_CONFIG_MAP = {
    '/purchase-orders': EventConfig(EventType.NewPurchaseOrderScheduled, validate_create_purchase_order_payload),
    '/sales-orders': EventConfig(EventType.NewSalesOrderScheduled, validate_create_sales_order_payload),
    '/product': EventConfig(EventType.NewProductScheduled, validate_create_product_payload)
}

EMITTER_NAME = 'EVENT_EMITTER'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context, sns_client=None, event_manager=None):
    logger.info("Starting lambda_handler")
    logger.info(f"Event: {event}")
    if sns_client is None:
        sns_client = boto3.client('sns')

    if event_manager is None:
        event_manager = EventManager()
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
        payload = json.dumps(request_data)
        sns_client.publish(
            TopicArn=topic_arn,
            Message=payload,
            Subject=event_config.subject.name
        )
        event_manager.insert_event(event_config.subject, EMITTER_NAME, payload)
    except Exception as e:
        logger.error(f"Error publishing to SNS: {e}")
        return FAILED_TO_PUBLISH_TO_SNS_RESPONSE
    logger.info(f"Published to SNS:{event_config}: {request_data}")
    return SUCCESS_RESPONSE
