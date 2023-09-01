import os
import unittest
from unittest.mock import patch, MagicMock

from clients.rds_client import RdsClient
from models.models import Product, Supplier, Customer


@patch.dict(os.environ, {
    'DB_HOST': 'localhost',
    'DB_NAME': 'test_db',
    'DB_USER': 'test_user',
    'DB_PASSWORD': 'test_password'
})
class TestRdsClient(unittest.TestCase):

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_init(self, mock_pool):
        RdsClient()
        mock_pool.assert_called_once()

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_init_fail(self, mock_pool):
        mock_pool.side_effect = Exception("Connection Error")
        with self.assertRaises(Exception):
            RdsClient()

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_insert_product(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        client = RdsClient()
        client.connection_pool = mock_pool
        product = Product(id='prod_123', name='TestProduct', description='Desc',
                          safety_stock=10, max_stock=50, quantity=30)

        client.insert_product(product)

        mock_cur.execute.assert_called()
        mock_conn.commit.assert_called()

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_insert_supplier(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        client = RdsClient()
        client.connection_pool = mock_pool
        supplier = Supplier(id='sup_123', name='TestSupplier')

        client.insert_supplier(supplier)

        mock_cur.execute.assert_called()
        mock_conn.commit.assert_called()

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_insert_customer(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        client = RdsClient()
        client.connection_pool = mock_pool
        customer = Customer(id='cus_123', name='TestCustomer')

        client.insert_customer(customer)

        mock_cur.execute.assert_called()
        mock_conn.commit.assert_called()

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_execute_fail(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.execute.side_effect = Exception('Execute failed')

        client = RdsClient()
        client.connection_pool = mock_pool
        product = Product(id='prod_123', name='TestProduct', description='Desc',
                          safety_stock=10, max_stock=50, quantity=30)

        with self.assertRaises(Exception):
            client.insert_product(product)

        mock_conn.rollback.assert_called()
