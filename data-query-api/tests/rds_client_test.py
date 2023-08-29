import os
import unittest
from unittest.mock import patch, MagicMock

from clients.rds_client import RdsClient
from exceptions.query_not_allowed_exception import QueryNotAllowedException


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
    def test_execute_select_query_not_allowed(self, mock_pool):
        client = RdsClient()
        with self.assertRaises(QueryNotAllowedException):
            client.execute_select("INSERT INTO table VALUES (1, 2, 3)")

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_execute_select_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchall.return_value = [('result1',), ('result2',)]

        client = RdsClient()
        client.connection_pool = mock_pool
        result = client.execute_select("SELECT * FROM table")

        self.assertEqual(result, [('result1',), ('result2',)])
        mock_pool.getconn.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cur.execute.assert_called_once_with("SELECT * FROM table")

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_constructor_exception(self, mock_pool):
        mock_pool.side_effect = Exception("Connection failed")
        with self.assertRaises(Exception):
            RdsClient()

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_execute_select_with_params(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        client = RdsClient()
        client.connection_pool = mock_pool
        client.execute_select("SELECT * FROM table WHERE column = %s", params=['value'])

        mock_cur.execute.assert_called_once_with("SELECT * FROM table WHERE column = %s", ['value'])

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_execute_select_exception(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchall.side_effect = Exception("Query failed")

        client = RdsClient()
        client.connection_pool = mock_pool
        result = client.execute_select("SELECT * FROM table")

        self.assertEqual(result, None)
        mock_pool.getconn.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cur.execute.assert_called_once_with("SELECT * FROM table")
