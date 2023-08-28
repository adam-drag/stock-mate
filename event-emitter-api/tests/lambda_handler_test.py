import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import boto3
import pytz
from moto import mock_sns

from api_responses import INVALID_JSON_PAYLOAD_RESPONSE, INVALID_ENDPOINT_RESPONSE, \
    INVALID_REQUEST_METHOD_RESPONSE, SUCCESS_RESPONSE, response_with_custom_message
from lambda_handler import lambda_handler


@mock_sns
class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        self.sns = boto3.client('sns', region_name='us-east-1')
        response = self.sns.create_topic(Name='TestTopic')
        self.topic_arn = response['TopicArn']
        patch.dict('os.environ', {'TOPIC_ARN': self.topic_arn}).start()

        self.sample_event = {
            'httpMethod': 'POST',
            'path': '/purchase-orders',
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

    def test_valid_request_create_purchase_order(self):
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
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, SUCCESS_RESPONSE)

    def test_valid_request_create_sales_order(self):
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
        event = {
            'httpMethod': 'POST',
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, SUCCESS_RESPONSE)

    def test_valid_request_create_product(self):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "test_product",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, SUCCESS_RESPONSE)

    def test_invalid_http_method(self):
        event = {
            'httpMethod': 'GET',
            'path': '/purchase-orders',
            'body': '{"key": "value"}'
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, INVALID_REQUEST_METHOD_RESPONSE)

    def test_invalid_endpoint(self):
        event = {
            'httpMethod': 'POST',
            'path': '/not-supported-path',
            'body': '{"key": "value"}'
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, INVALID_ENDPOINT_RESPONSE)

    def test_invalid_json_payload(self):
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-orders',
            'body': 'invalid_json'
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, INVALID_JSON_PAYLOAD_RESPONSE)

    def test_should_return_400_when_sales_order_position_date_is_not_in_future(self):
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
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_purchase_order_position_date_is_not_in_future(self):
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
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    # here

    def test_should_return_400_when_customer_id_doesnt_start_from_cus(self):
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
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field customer_id is invalid"))

    def test_valid_request_create_sales_order(self):
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
        event = {
            'httpMethod': 'POST',
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, SUCCESS_RESPONSE)

    def test_should_return_400_when_supplier_id_doesnt_start_from_sup(self):
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
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field supplier_id is invalid"))

    def test_should_return_400_when_product_id_doesnt_start_from_prod(self):
        product_request_payload = {
            "product_id": "cus_123",
            "name": "test_product",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field product_id is invalid"))

    def test_should_return_400_when_product_id_is_not_string(self):
        product_request_payload = {
            "product_id": 123,
            "name": "test_product",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field product_id is invalid"))

    def test_should_return_400_when_product_id_is_empty(self):
        product_request_payload = {
            "product_id": "",
            "name": "test_product",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field product_id is invalid"))

    def test_should_return_400_when_product_name_is_empty(self):
        product_request_payload = {
            "product_id": "prod_123",
            "name": "",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field name is invalid"))

    def test_should_return_400_when_product_name_is_not_string(self):
        product_request_payload = {
            "product_id": "prod_123",
            "name": 123,
        }
        event = {
            'httpMethod': 'POST',
            'path': '/product',
            'body': json.dumps(product_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field name is invalid"))

    def test_should_return_400_when_sales_price_is_negative(self):
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
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_sales_quantity_ordered_is_negative(self):
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
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_sales_delivery_date_is_no_parsable_date(self):
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
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_sales_order_positions_is_empty(self):
        sales_order_request_payload = {
            "customer_id": "cus_123",
            "order_positions": []
        }
        event = {
            'httpMethod': 'POST',
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_return_400_when_sales_order_positions_is_none(self):
        sales_order_request_payload = {
            "customer_id": "cus_123",
            "order_positions": None
        }
        event = {
            'httpMethod': 'POST',
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_sales_orders_is_without_order_positions(self):
        sales_order_request_payload = {
            "customer_id": "cus_123",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/sales-orders',
            'body': json.dumps(sales_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is required"))

    def test_should_return_400_when_purchase_price_is_negative(self):
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
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_purchase_quantity_ordered_is_negative(self):
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
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_purchase_delivery_date_is_no_parsable_date(self):
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
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_purchase_order_positions_is_empty(self):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": []
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_return_400_when_purchase_order_positions_is_none(self):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
            "order_positions": None
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is invalid"))

    def test_should_return_400_when_purchase_orders_is_without_order_positions(self):
        purchase_order_request_payload = {
            "supplier_id": "sup_123",
        }
        event = {
            'httpMethod': 'POST',
            'path': '/purchase-orders',
            'body': json.dumps(purchase_order_request_payload)
        }
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field order_positions is required"))

    def test_should_return_400_when_product_minimum_stock_level_is_negative(self):
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
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field minimumStockLevel is invalid"))

    def test_should_return_400_when_product_maximum_stock_level_is_negative(self):
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
        response = lambda_handler(event, None)
        self.assertEqual(response, response_with_custom_message("Field maximumStockLevel is invalid"))
