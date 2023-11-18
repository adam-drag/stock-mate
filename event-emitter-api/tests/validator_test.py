import unittest

from common.api_responses import INVALID_REQUEST_METHOD_RESPONSE, INVALID_JSON_PAYLOAD_RESPONSE
from validation.validator import validate_request, validate_create_purchase_order_payload, future_date_validator, order_position_validator


class TestValidateRequest(unittest.TestCase):

    def setUp(self):
        self.sample_event = {
            'httpMethod': 'POST',
            'path': '/purchase-orders',
            'body': '{"key": "value"}'
        }

    def test_invalid_http_method(self):
        event = self.sample_event.copy()
        event['httpMethod'] = 'GET'

        result = validate_request(event)
        self.assertFalse(result)
        self.assertEqual(result.response, INVALID_REQUEST_METHOD_RESPONSE)

    def test_invalid_json_payload(self):
        event = self.sample_event.copy()
        event['body'] = 'invalid_json'

        result = validate_request(event)
        self.assertFalse(result)
        self.assertEqual(result.response, INVALID_JSON_PAYLOAD_RESPONSE)

    def test_valid_request(self):
        event = self.sample_event.copy()

        result = validate_request(event)
        self.assertTrue(result)
        self.assertIsNone(result.response)

    def test_missing_body(self):
        event = self.sample_event.copy()
        del event['body']

        result = validate_request(event)
        self.assertFalse(result)
        self.assertEqual(result.response, INVALID_JSON_PAYLOAD_RESPONSE)

    def test_validate_create_purchase_order_payload_fail_when_payload_is_none(self):
        result = validate_create_purchase_order_payload(None)

        self.assertFalse(result)
        self.assertEqual(result.response, INVALID_JSON_PAYLOAD_RESPONSE)

    def test_date_validator_fail_when_date_is_none(self):
        result = future_date_validator(None)

        self.assertFalse(result)

    def test_order_position_validator_when_order_position_is_none(self):
        result = order_position_validator(None)

        self.assertFalse(result)
