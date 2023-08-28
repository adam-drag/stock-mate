import unittest
from unittest.mock import patch

from services.db_service import DbService


class TestDbService(unittest.TestCase):

    @patch('clients.rds_client.RdsClient')
    def setUp(self, mock_rds_client):
        self.mock_rds_client = mock_rds_client()
        self.db_service = DbService(self.mock_rds_client)

    def test_fetch_products(self):
        self.mock_rds_client.execute_select.return_value = [{"product": "apple"}]

        params = {'id': '1'}
        result = self.db_service.fetch_products(params)

        self.assertEqual(result, [{"product": "apple"}])

    def test_fetch_sales_orders(self):
        self.mock_rds_client.execute_select.return_value = [{"order": "1234"}]

        params = {'id': '1'}
        result = self.db_service.fetch_sales_orders(params)

        self.assertEqual(result, [{"order": "1234"}])

    def test_fetch_purchase_orders(self):
        self.mock_rds_client.execute_select.return_value = [{"purchase_order": "5678"}]

        params = {'id': '1'}
        result = self.db_service.fetch_purchase_orders(params)

        self.assertEqual(result, [{"purchase_order": "5678"}])

    def test_build_query(self):
        base_query = "SELECT * FROM products WHERE 1=1"
        params = {'name': 'apple', 'category': 'fruit'}
        expected_query = "SELECT * FROM products WHERE 1=1 AND name = %s AND category = %s"
        expected_query_params = ['apple', 'fruit']

        query, query_params = self.db_service._build_query(base_query, params)

        self.assertEqual(query, expected_query)
        self.assertEqual(query_params, expected_query_params)
