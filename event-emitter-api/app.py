import json
import os
import traceback
from typing import Callable

from common.api_responses import FAILED_TO_PUBLISH_TO_SNS_RESPONSE, SUCCESS_RESPONSE, INVALID_ENDPOINT_RESPONSE, \
    NOT_SUPPORTED_YET_RESPONSE
from common.events.event_manager import EventManager
from common.events.events import EventType
from common.utils.logger import get_logger
from validator import validate_request, validate_create_purchase_order_payload, validate_create_sales_order_payload, \
    ValidationResult, validate_create_product_payload, validate_create_customer_payload, \
    validate_create_supplier_payload


class EventConfig():
    event_type: EventType
    validator: Callable[[str], ValidationResult]

    def __init__(self, event_type: EventType, validator: Callable[[str], ValidationResult]):
        self.event_type = event_type
        self.validator = validator
        self.sns_map = {
            EventType.NewProductScheduled: os.environ.get("NEW_PRODUCT_SCHEDULED_SNS_ARN"),
            EventType.NewSalesOrderScheduled: os.environ.get("NEW_SALES_ORDER_SCHEDULED_SNS_ARN"),
            EventType.NewDeliveryScheduled: os.environ.get("NEW_DELIVERY_SCHEDULED_SNS_ARN"),
            EventType.NewDispatchRequested: os.environ.get("DISPATCH_REQUESTED_SNS_ARN"),
            EventType.UsageUpdateScheduled: os.environ.get("USAGE_UPDATE_SNS_ARN"),
            EventType.NewPurchaseOrderScheduled: os.environ.get("NEW_PURCHASE_ORDER_SCHEDULED_SNS_ARN"),
            EventType.NewSupplierScheduled: os.environ.get("NEW_SUPPLIER_SCHEDULED_SNS_ARN"),
            EventType.NewCustomerScheduled: os.environ.get("NEW_CUSTOMER_SCHEDULED_SNS_ARN"),
        }

    def get_arn(self):
        return self.sns_map.get(self.event_type)


EMITTER_NAME = 'EVENT_EMITTER'

logger = get_logger(__name__)


def lambda_handler(event, context, event_manager=None):
    logger.info("Starting lambda_handler")
    logger.info(f"Received event: {event}")

    if event_manager is None:
        event_manager = EventManager(EMITTER_NAME)

    validation_result = validate_request(event)
    if not validation_result:
        logger.error(f"Invalid request, {validation_result.response}")
        return validation_result.response

    path = event.get('path')
    path_to_event_cfg_map = lazy_load_path_to_event_config_map()
    event_config = path_to_event_cfg_map.get(path)

    if not event_config:
        logger.error(f"Endpoint not found: {path}")
        return INVALID_ENDPOINT_RESPONSE
    is_event_valid_result = event_config.validator(event['body'])
    if not is_event_valid_result:
        logger.error(f"Invalid event: {is_event_valid_result.response}")
        return is_event_valid_result.response
    logger.info(f"Event is valid: {is_event_valid_result}")
    request_data = json.loads(event['body'])
    logger.info(f"Publishing to SNS:{event_config}: {request_data}")
    try:
        sns_arn = event_config.get_arn()
        message = {
            "event_type": event_config.event_type.name,
            "payload": request_data
        }
        message_json = json.dumps(message)
        event_manager.send_event(sns_arn, event_config.event_type, EMITTER_NAME, message_json)
    except Exception as e:
        logger.error(f"Error publishing to SNS: {e}")
        traceback.print_exc()
        return FAILED_TO_PUBLISH_TO_SNS_RESPONSE
    logger.info(f"Published to SNS:{event_config}: {request_data}")
    return SUCCESS_RESPONSE


def lazy_load_path_to_event_config_map():
    return {
        '/purchase-order': EventConfig(EventType.NewPurchaseOrderScheduled, validate_create_purchase_order_payload),
        '/sales-order': EventConfig(EventType.NewSalesOrderScheduled, validate_create_sales_order_payload),
        '/product': EventConfig(EventType.NewProductScheduled, validate_create_product_payload),
        '/customer': EventConfig(EventType.NewCustomerScheduled, validate_create_customer_payload),
        '/supplier': EventConfig(EventType.NewSupplierScheduled, validate_create_supplier_payload),
        '/delivery': EventConfig(EventType.NewDeliveryScheduled,
                                 lambda x: ValidationResult(False, NOT_SUPPORTED_YET_RESPONSE)),
        '/dispatch': EventConfig(EventType.NewDispatchRequested,
                                 lambda x: ValidationResult(False, NOT_SUPPORTED_YET_RESPONSE)),
    }
