import json
from datetime import datetime, timezone

import jsonschema
from dateutil import parser
from jsonschema import ValidationError
from jsonschema.validators import Draft7Validator

from common.api_responses import INVALID_REQUEST_METHOD_RESPONSE, INVALID_JSON_PAYLOAD_RESPONSE, \
    response_with_custom_message
from common.utils.logger import get_logger
from validation.payload_schemas import product_schema, purchase_order_schema, supplier_schema, inventory_schema

logger = get_logger(__name__)


class ValidationResult:

    def __init__(self, is_valid, response):
        self.is_valid = is_valid
        self.response = response
        logger.info(f"Validation result: {self}")

    def __str__(self):
        return str(self.response)

    def __bool__(self):
        return self.is_valid


validator = Draft7Validator(
    schema=purchase_order_schema,
    format_checker=jsonschema.FormatChecker()
)


def is_future_datetime(date):
    if date.tzinfo is None and datetime.now().tzinfo is not None:
        current_time = datetime.now().replace(tzinfo=None)
    elif date.tzinfo is not None and datetime.now().tzinfo is None:
        current_time = datetime.now().replace(tzinfo=timezone.utc)
    else:
        current_time = datetime.now()

    return date > current_time


def validate_payload(payload_json, schema):
    if not payload_json:
        return ValidationResult(False, INVALID_JSON_PAYLOAD_RESPONSE)
    try:
        payload = json.loads(payload_json)
        jsonschema.validate(payload, schema)
        return ValidationResult(True, None)
    except ValidationError as e:
        return ValidationResult(False, response_with_custom_message(str(e)))


def validate_create_sales_order_payload(payload):
    raise Exception('Not supported yet')


def validate_create_product_payload(payload):
    return validate_payload(payload, product_schema)


def validate_create_supplier_payload(payload):
    return validate_payload(payload, supplier_schema)


def validate_purchase_order_positions_delivery_dates(payload_json):
    payload = json.loads(payload_json)
    for order_position in payload['order_positions']:
        date_object = parser.isoparse(order_position["delivery_date"])
        if not is_future_datetime(date_object):
            return ValidationResult(False, response_with_custom_message("Delivery date must be in future"))
    return ValidationResult(True, None)


def validate_create_purchase_order_payload(payload_json):
    purchase_order_validation = validate_payload(payload_json, purchase_order_schema)
    if purchase_order_validation.is_valid:
        return validate_purchase_order_positions_delivery_dates(payload_json)
    return purchase_order_validation


def validate_create_customer_payload(payload):
    raise Exception('Not supported yet')


def validate_inventor(payload):
    return validate_payload(payload, inventory_schema)


def validate_request(event) -> ValidationResult:
    http_method = event.get("httpMethod", "").upper()

    if http_method != "POST":
        return ValidationResult(False, INVALID_REQUEST_METHOD_RESPONSE)

    try:
        json.loads(event.get('body', None))
    except Exception as e:
        logger.error(f"Failed to parse JSON payload: {str(e)}")
        return ValidationResult(False, INVALID_JSON_PAYLOAD_RESPONSE)

    return ValidationResult(True, None)
