import os
import unittest
from unittest.mock import patch, MagicMock

from common.clients.rds_client import RdsClient


@patch.dict(os.environ, {
    'DB_HOST': 'localhost',
    'DB_NAME': 'test_db',
    'DB_USER': 'test_user',
    'DB_PASSWORD': 'test_password'
})
class TestRdsClient(unittest.TestCase):

    @patch('common.clients.rds_client.psycopg2.pool.SimpleConnectionPool')
    @patch('common.clients.rds_client.logging')
    def test_init(self, mock_logging, mock_pool):
        mock_pool.return_value = MagicMock()
        client = RdsClient()
        mock_pool.assert_called_once()
        mock_logging.error.assert_not_called()

    @patch('common.clients.rds_client.psycopg2.pool.SimpleConnectionPool')
    @patch('common.clients.rds_client.logging')
    def test_init_fails(self, mock_logging, mock_pool):
        mock_pool.side_effect = Exception('DB connection failed')
        with self.assertRaises(Exception):
            RdsClient()
        mock_logging.error.assert_called_once_with('Failed to connect to DB: DB connection failed')

    @patch('psycopg2.pool.SimpleConnectionPool')
    def test_execute_select_success(self, mock_pool):
        mock_conn = MagicMock()
        mock_cur = MagicMock()

        mock_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchall.return_value = [('result1',), ('result2',)]

        client = RdsClient()
        client.connection_pool = mock_pool
        result = client.execute("SELECT * FROM table")

        self.assertEqual(result, [('result1',), ('result2',)])
        mock_pool.getconn.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cur.execute.assert_called_once_with("SELECT * FROM table")

    @patch('common.clients.rds_client.RdsClient.connection_pool')
    @patch('common.clients.rds_client.logging')
    def test_execute_fails(self, mock_logging, mock_connection_pool):
        mock_conn = MagicMock()
        mock_connection_pool.getconn.return_value = mock_conn

        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception('Query execution failed')

        client = RdsClient()
        result = client.execute('SELECT * FROM table')

        mock_cursor.execute.assert_called_once_with('SELECT * FROM table')
        mock_logging.error.assert_called_once_with('Query execution failed: Query execution failed')
        self.assertIsNone(result)
