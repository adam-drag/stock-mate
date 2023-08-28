import logging
import os

import psycopg2
from psycopg2 import pool

from exceptions.query_not_allowed_exception import QueryNotAllowedException

DEFAULT_MIN_DB_CONNECTIONS = 1
DEFAULT_MAX_DB_CONNECTIONS = 10


class RdsClient:

    def __init__(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                os.environ.get('MIN_DB_CONNECTIONS', DEFAULT_MIN_DB_CONNECTIONS),
                os.environ.get('MAX_DB_CONNECTIONS', DEFAULT_MAX_DB_CONNECTIONS),
                host=os.environ['DB_HOST'],
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD']
            )
        except Exception as e:
            logging.error(f"Failed to connect to DB: {e}")
            raise e

    def execute_select(self, query, params=None):
        conn = None
        result = None

        if not query.strip().upper().startswith('SELECT'):
            raise QueryNotAllowedException("Only SELECT queries are allowed.")

        try:
            conn = self.connection_pool.getconn()
            with conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                result = cur.fetchall()
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
        finally:
            if conn:
                self.connection_pool.putconn(conn)

        return result
