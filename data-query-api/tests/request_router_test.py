import json
import unittest
from unittest.mock import patch

from request_router import RequestRouter


class TestRequestRouter(unittest.TestCase):

    @patch('services.db_service.DbService')
    def setUp(self, mock_db_service):
        self.mock_db_service = mock_db_service
        self.router = RequestRouter(self.mock_db_service)

    def test_handle_request_products(self):
        self.mock_db_service.fetch_products.return_value = {"product": "apple"}

        event = {'path': '/products', 'queryStringParameters': {'id': '1'}}

        result = self.router.handle_request(event)

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body']), {"product": "apple"})

    def test_handle_request_sales_orders(self):
        self.mock_db_service.fetch_sales_orders.return_value = {"order": "1234"}
        event = {'path': '/sales_orders', 'queryStringParameters': {'id': '1'}}
        result = self.router.handle_request(event)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body']), {"order": "1234"})

    def test_handle_request_invalid_path(self):
        event = {'path': '/invalid', 'queryStringParameters': {'id': '1'}}
        result = self.router.handle_request(event)
        self.assertEqual(result['statusCode'], 404)
        self.assertEqual(json.loads(result['body']), {"error": "Not Found"})

    def test_handle_request_exception(self):
        self.mock_db_service.fetch_products.side_effect = Exception("Database error")
        event = {'path': '/products', 'queryStringParameters': {'id': '1'}}
        result = self.router.handle_request(event)
        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(json.loads(result['body']), {"error": "Internal Server Error"})
