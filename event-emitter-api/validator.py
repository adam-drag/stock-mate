import json
from datetime import datetime, timezone

from common.api_responses import INVALID_REQUEST_METHOD_RESPONSE, INVALID_JSON_PAYLOAD_RESPONSE, \
    response_with_custom_message
from common.utils.logger import get_logger

logger = get_logger(__name__)

SUPPLIER_ID_PREFIX = "sup_"
PRODUCT_ID_PREFIX = "prod_"
CUSTOMER_ID_PREFIX = 'cus_'

MAX_ID_LEN = 10
MAX_PRODUCT_ID_LEN = 10


class ValidationResult:

    def __init__(self, is_valid, response):
        self.is_valid = is_valid
        self.response = response
        logger.info(f"Validation result: {self}")

    def __str__(self):
        return str(self.response)

    def __bool__(self):
        return self.is_valid


def supplier_id_validator(supplier_id) -> bool:
    return is_valid_id(supplier_id) and supplier_id.startswith(SUPPLIER_ID_PREFIX)


def customer_id_validator(supplier_id) -> bool:
    return is_valid_id(supplier_id) and supplier_id.startswith(CUSTOMER_ID_PREFIX)


def is_valid_id(entity_id) -> bool:
    return (entity_id is not None and
            isinstance(entity_id, str) and
            0 < len(entity_id) <= MAX_ID_LEN)


def product_id_validator(product_id) -> bool:
    return (product_id is not None and
            isinstance(product_id, str) and
            0 < len(product_id) <= MAX_PRODUCT_ID_LEN and
            product_id.startswith(PRODUCT_ID_PREFIX))


def price_validator(price) -> bool:
    return is_positive_number(price)


def quantity_validator(quantity) -> bool:
    return is_positive_number(quantity)


def date_validator(str_date) -> bool:
    try:
        if str_date is None:
            return False
        date = datetime.fromisoformat(str_date)
        is_future = is_future_datetime(date)
        if not is_future:
            logger.error(f"Date {str_date} is not in the future")
        return is_future
    except Exception as e:
        logger.error(f"Failed to validate date: {str(e)}")
        return False


def is_future_datetime(date):
    if date.tzinfo is None and datetime.now().tzinfo is not None:
        current_time = datetime.now().replace(tzinfo=None)
    elif date.tzinfo is not None and datetime.now().tzinfo is None:
        current_time = datetime.now().replace(tzinfo=timezone.utc)
    else:
        current_time = datetime.now()

    return date > current_time


def is_positive_number(quantity):
    return (quantity is not None and
            isinstance(quantity, (int, float)) and
            quantity > 0)


def order_position_validator(order_position) -> bool:
    if order_position is None:
        return False

    for field, validator in order_position_field_validators.items():
        if not validator(order_position.get(field)):
            return False
    return True


def order_positions_validator(order_positions) -> bool:
    if order_positions is None or len(order_positions) == 0:
        return False

    for order_position in order_positions:
        if not order_position_validator(order_position):
            return False
    return True


create_purchase_order_required_fields = [
    "supplier_id",
    "order_positions"
]

create_sales_order_required_fields = [
    "customer_id",
    "order_positions"
]

create_purchase_order_field_validators = {
    "supplier_id": supplier_id_validator,
    "order_positions": order_positions_validator
}

create_sales_order_field_validators = {
    "customer_id": customer_id_validator,
    "order_positions": order_positions_validator
}

order_position_field_validators = {
    "product_id": product_id_validator,
    "price": price_validator,
    "quantityOrdered": quantity_validator,
    "deliveryDate": date_validator
}


def stock_level_validator(stock_level) -> bool:
    return stock_level is None or stock_level >= 0


def name_field_validator(name) -> bool:
    return name is not None and isinstance(name, str) and len(name) > 0


create_product_field_validators = {
    "name": name_field_validator,
    "minimumStockLevel": stock_level_validator,
    "maximumStockLevel": stock_level_validator,
}

create_product_required_fields = [
    "name"
]

create_customer_required_fields = [
    "name"
]

create_customer_field_validators = {
    "name": name_field_validator,
}

create_supplier_required_fields = [
    "name"
]

create_supplier_field_validators = {
    "name": name_field_validator,
}


def validate_payload(payload_str, required_fields, field_validators):
    if payload_str is None:
        return ValidationResult(False, INVALID_JSON_PAYLOAD_RESPONSE)
    payload = json.loads(payload_str)
    for field in required_fields:
        if field not in payload:
            return ValidationResult(False, response_with_custom_message(f"Field {field} is required"))

    for field, validator in field_validators.items():
        if not validator(payload.get(field)):
            return ValidationResult(False, response_with_custom_message(f"Field {field} is invalid"))

    return ValidationResult(True, None)


def validate_create_purchase_order_payload(payload):
    return validate_payload(payload, create_purchase_order_required_fields, create_purchase_order_field_validators)


def validate_create_sales_order_payload(payload):
    return validate_payload(payload, create_sales_order_required_fields, create_sales_order_field_validators)


def validate_create_product_payload(payload):
    return validate_payload(payload, create_product_required_fields, create_product_field_validators)


def validate_create_customer_payload(payload):
    return validate_payload(payload, create_customer_required_fields, create_customer_field_validators)


def validate_create_supplier_payload(payload):
    return validate_payload(payload, create_supplier_required_fields, create_supplier_field_validators)


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
