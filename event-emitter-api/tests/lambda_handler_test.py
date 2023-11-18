import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import boto3
import pytz
from moto import mock_sns

from app import lambda_handler
from common.api_responses import SUCCESS_RESPONSE, INVALID_REQUEST_METHOD_RESPONSE, INVALID_ENDPOINT_RESPONSE, \
    INVALID_JSON_PAYLOAD_RESPONSE
from common.events.events import EventType


@patch.dict('os.environ', {
    'NEW_PRODUCT_SCHEDULED_SNS_ARN': 'mock_arn_value_for_product',
    'NEW_SALES_ORDER_SCHEDULED_SNS_ARN': 'mock_arn_value_for_sales_order',
    'NEW_DELIVERY_SCHEDULED_SNS_ARN': 'mock_arn_value_for_delivery',
    'DISPATCH_REQUESTED_SNS_ARN': 'mock_arn_value_for_dispatch',
    'USAGE_UPDATE_SNS_ARN': 'mock_arn_value_for_usage_update',
    'NEW_PURCHASE_ORDER_SCHEDULED_SNS_ARN': 'mock_arn_value_for_purchase_order',
    'NEW_SUPPLIER_SCHEDULED_SNS_ARN': 'mock_arn_value_for_supplier',
    'NEW_CUSTOMER_SCHEDULED_SNS_ARN': 'mock_arn_value_for_customer'
})
@patch('common.events.event_manager.EventManager')
@mock_sns
class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        self.sns = boto3.client('sns', region_name='us-east-1')
        response = self.sns.create_topic(Name='TestTopic')
        self.topic_arn = response['TopicArn']
        patch.dict('os.environ', {'TOPIC_ARN': self.topic_arn}).start()

        self.sample_event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': '{"key": "value"}'
        }
        current_time_utc = datetime.now(pytz.utc)
        tomorrow_utc = current_time_utc + timedelta(days=1)
        yesterday_utc = current_time_utc - timedelta(days=1)
        self.tomorrow_iso = tomorrow_utc.isoformat()
        self.yesterday_iso = yesterday_utc.isoformat()

    def tearDown(self):
        patch.stopall()
        self.sns.delete_topic(TopicArn=self.topic_arn)

    def test_valid_request_create_purchase_order(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_c6257bffb766",
            "created_at": "2023-11-18",
            "order_positions": [
                {
                    "product_id": "prod_bf01bf960d43",
                    "quantity_ordered": 10,
                    "quantity_received": 5,
                    "price": 25.99,
                    "delivery_date": self.tomorrow_iso
                }]}
        json_payload = json.dumps(purchase_order_request_payload)
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json_payload
        }
        expected_message = {
            "event_type": EventType.NewPurchaseOrderScheduled.name,
            "payload": purchase_order_request_payload
        }
        expected_message_json = json.dumps(expected_message)
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, SUCCESS_RESPONSE)
        event_manager_mock.send_event.assert_called()

    def test_valid_request_create_product(self, event_manager_mock):
        product_request_payload = {
            "name": "test_product",
        }
        json_payload = json.dumps(product_request_payload)
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json_payload
        }
        expected_message = {
            "event_type": EventType.NewProductScheduled.name,
            "payload": product_request_payload
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, SUCCESS_RESPONSE)
        event_manager_mock.send_event.assert_called()

    def test_invalid_http_method(self, event_manager_mock):
        event = {
            'httpMethod': 'GET',
            'path': '/purchase-order',
            'body': '{"key": "value"}'
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, INVALID_REQUEST_METHOD_RESPONSE)
        event_manager_mock.send_event.assert_not_called()

    def test_invalid_endpoint(self, event_manager_mock):
        event = {
            'httpMethod': 'POST',
            'path': '/not-supported-path',
            'body': '{"key": "value"}'
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, INVALID_ENDPOINT_RESPONSE)
        event_manager_mock.send_event.assert_not_called()

    def test_invalid_json_payload(self, event_manager_mock):
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': 'invalid_json'
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, INVALID_JSON_PAYLOAD_RESPONSE)
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_purchase_order_position_date_is_not_in_future(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "created_at": self.yesterday_iso,
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantity_ordered": 123,
                    "delivery_date": self.yesterday_iso
                }
            ]
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_supplier_id_doesnt_start_from_sup(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "cus_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantityOrdered": 123,
                    "deliveryDate": self.tomorrow_iso
                }
            ]
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_product_name_is_empty(self, event_manager_mock):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_product_name_is_not_string(self, event_manager_mock):
        product_request_payload = {
            "product_id": "prod_123",
            "name": 123,
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_purchase_price_is_negative(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": -123,
                    "quantityOrdered": 123,
                    "deliveryDate": self.tomorrow_iso
                }
            ]
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_purchase_quantity_ordered_is_negative(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantityOrdered": -123,
                    "deliveryDate": self.tomorrow_iso
                }
            ]
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_purchase_delivery_date_is_no_parsable_date(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantityOrdered": 123,
                    "deliveryDate": "not_a_date"
                }
            ]
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_purchase_order_positions_is_empty(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": []
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_return_400_when_purchase_order_positions_is_none(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": None
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_purchase_orders_is_without_order_positions(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_product_minimum_stock_level_is_negative(self, event_manager_mock):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "test_product",
            "safety_stock": -123,
            "max_stock": 123,
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_product_maximum_stock_level_is_negative(self, event_manager_mock):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "test_product",
            "safety_stock": 123,
            "max_stock": -123,
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(400, response['statusCode'])
        event_manager_mock.send_event.assert_not_called()
