import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import boto3
import pytz
from moto import mock_sns

from common.api_responses import SUCCESS_RESPONSE, INVALID_REQUEST_METHOD_RESPONSE, INVALID_ENDPOINT_RESPONSE, \
    INVALID_JSON_PAYLOAD_RESPONSE, response_with_custom_message
from common.events.events import EventType
from lambda_handler import lambda_handler, EMITTER_NAME


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
@patch('lambda_handler.EventManager')
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
            "supplier_id": "sup_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantityOrdered": 123,
                    "deliveryDate": self.tomorrow_iso
                }
            ]
        }
        json_payload = json.dumps(purchase_order_request_payload)
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json_payload
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, SUCCESS_RESPONSE)
        event_manager_mock.send_event.assert_called_with(
            'mock_arn_value_for_purchase_order', EventType.NewPurchaseOrderScheduled, EMITTER_NAME, json_payload)

    def test_valid_request_create_sales_order(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantityOrdered": 123,
                    "deliveryDate": self.tomorrow_iso
                }
            ]
        }
        json_payload = json.dumps(sales_order_request_payload)
        event = {
            'httpMethod': 'POST',
            'path': '/sales-order',
            'body': json_payload
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, SUCCESS_RESPONSE)
        event_manager_mock.send_event.assert_called_with(
            'mock_arn_value_for_sales_order', EventType.NewSalesOrderScheduled, EMITTER_NAME, json_payload)

    def test_valid_request_create_product(self, event_manager_mock):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "test_product",
        }
        json_payload = json.dumps(product_request_payload)
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json_payload
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, SUCCESS_RESPONSE)
        event_manager_mock.send_event.assert_called_with(
            'mock_arn_value_for_product', EventType.NewProductScheduled, EMITTER_NAME, json_payload)

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

    def test_should_return_400_when_sales_order_position_date_is_not_in_future(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantityOrdered": 123,
                    "deliveryDate": self.yesterday_iso
                }
            ]
        }
        event = {
            'httpMethod': 'POST',
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_purchase_order_position_date_is_not_in_future(self, event_manager_mock):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": [
                {
                    "product_id": "prod_123",
                    "price": 123,
                    "quantityOrdered": 123,
                    "deliveryDate": self.yesterday_iso
                }
            ]
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-order',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
        event_manager_mock.send_event.assert_not_called()

    # here

    def test_should_return_400_when_customer_id_doesnt_start_from_cus(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "sup_123",
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
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field customer_id is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field supplier_id is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field name is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field name is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_sales_price_is_negative(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
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
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_sales_quantity_ordered_is_negative(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
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
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_sales_delivery_date_is_no_parsable_date(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
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
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_sales_order_positions_is_empty(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
            "order_positions": []
        }
        event = {
            'httpMethod': 'POST',
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_return_400_when_sales_order_positions_is_none(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
            "order_positions": None
        }
        event = {
            'httpMethod': 'POST',
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_sales_orders_is_without_order_positions(self, event_manager_mock):
        sales_order_request_payload = {
            "customer_id": "cus_123",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/sales-order',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field order_positions is required"))
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
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))
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
        self.assertEqual(response, response_with_custom_message("Field order_positions is required"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_product_minimum_stock_level_is_negative(self, event_manager_mock):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "test_product",
            "minimumStockLevel": -123,
            "maximumStockLevel": 123,
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field minimumStockLevel is invalid"))
        event_manager_mock.send_event.assert_not_called()

    def test_should_return_400_when_product_maximum_stock_level_is_negative(self, event_manager_mock):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "test_product",
            "minimumStockLevel": 123,
            "maximumStockLevel": -123,
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None, event_manager=event_manager_mock)
        self.assertEqual(response, response_with_custom_message("Field maximumStockLevel is invalid"))
        event_manager_mock.send_event.assert_not_called()
