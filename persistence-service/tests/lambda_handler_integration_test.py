import json
import os
import unittest
from unittest.mock import patch, ANY

from moto import mock_sns

from common.events.events import EventType
from app import lambda_handler
from models.models import Product, Customer, Supplier
from utils.component_provider import ComponentProvider


@patch.dict(os.environ, {
    'DB_HOST': 'localhost',
    'DB_NAME': 'test_db',
    'DB_USER': 'test_user',
    'DB_PASSWORD': 'test_password'
})
@mock_sns
class LambdaHandlerIntegrationTest(unittest.TestCase):

    def tearDown(self):
        ComponentProvider._persistence_service = None
        ComponentProvider._topic_router = None

    @patch('utils.component_provider.ComponentProvider.get_rds_domain_client')
    @patch('clients.rds_domain_client.RdsDomainClient')
    @patch("boto3.client")
    def test_lambda_handler_integration_new_product(self, boto_mock, mock_rds_client, mock_get_rds_client):
        mock_get_rds_client.return_value = mock_rds_client

        mock_insert_product = mock_rds_client.insert_product
        mock_insert_product.return_value = None

        payload = {
            'name': 'TestProduct',
            'description': 'TestDescription',
            'safety_stock': 10,
            'max_stock': 50,
            'quantity': 30
        }
        message = {
            "payload": payload,
            "event_type": EventType.NewProductScheduled.name
        }
        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps(message),
                    'TopicArn': f"arn:aws:sns:us-east-1:123456789012:{EventType.NewProductScheduled.name}"
                }
            }]
        }
        context = {}

        # Act
        result = lambda_handler(event, context)

        # Assert
        expected_product_to_persist = Product(
            id=ANY,
            name='TestProduct',
            description='TestDescription',
            safety_stock=10,
            max_stock=50,
            quantity=30
        )
        mock_insert_product.assert_called_with(expected_product_to_persist)

    @patch('utils.component_provider.ComponentProvider.get_rds_domain_client')
    @patch('clients.rds_domain_client.RdsDomainClient')
    @patch("boto3.client")
    def test_lambda_handler_integration_new_supplier(self, boto_mock, mock_rds_client, mock_get_rds_client):
        mock_get_rds_client.return_value = mock_rds_client

        mock_insert_supplier = mock_rds_client.insert_supplier
        mock_insert_supplier.return_value = None

        payload = {
            'name': 'TestSupplier',
        }
        message = {
            "payload": payload,
            "event_type": EventType.NewSupplierScheduled.name
        }
        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps(message),
                    'TopicArn': f"arn:aws:sns:us-east-1:123456789012:{EventType.NewSupplierScheduled.name}"
                }
            }]
        }
        context = {}

        result = lambda_handler(event, context)

        expected_supplier_to_persist = Supplier(
            id=ANY,
            name='TestSupplier'
        )
        mock_insert_supplier.assert_called_with(expected_supplier_to_persist)

    @patch('utils.component_provider.ComponentProvider.get_rds_domain_client')
    @patch('clients.rds_domain_client.RdsDomainClient')
    @patch("boto3.client")
    def test_lambda_handler_integration_new_customer(self, boto_mock, mock_rds_client, mock_get_rds_client):
        mock_get_rds_client.return_value = mock_rds_client

        mock_insert_customer = mock_rds_client.insert_customer
        mock_insert_customer.return_value = None

        payload = {
            'name': 'TestCustomer',
        }
        message = {
            "payload": payload,
            "event_type": EventType.NewCustomerScheduled.name
        }
        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps(message),
                    'TopicArn': f"arn:aws:sns:us-east-1:123456789012:{EventType.NewCustomerScheduled.name}"
                }
            }]
        }
        context = {}

        result = lambda_handler(event, context)

        expected_customer_to_persist = Customer(
            id=ANY,
            name='TestCustomer'
        )
        mock_insert_customer.assert_called_with(expected_customer_to_persist)

    @patch('utils.component_provider.ComponentProvider.get_rds_domain_client')
    @patch('clients.rds_domain_client.RdsDomainClient')
    @patch("boto3.client")
    def test_lambda_handler_integration_new_purchase_order(self, boto_mock, mock_rds_client, mock_get_rds_client):
        mock_get_rds_client.return_value = mock_rds_client

        mock_insert_customer = mock_rds_client.insert_customer
        mock_insert_customer.return_value = None

        payload = {
            'name': 'TestCustomer',
        }
        message = {
            "payload": payload,
            "event_type": EventType.NewCustomerScheduled.name
        }
        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps(message),
                    'TopicArn': f"arn:aws:sns:us-east-1:123456789012:{EventType.NewCustomerScheduled.name}"
                }
            }]
        }
        context = {}

        result = lambda_handler(event, context)

        expected_customer_to_persist = Customer(
            id=ANY,
            name='TestCustomer'
        )
        mock_insert_customer.assert_called_with(expected_customer_to_persist)
