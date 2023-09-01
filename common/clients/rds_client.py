import logging
import os

import psycopg2
from psycopg2 import pool

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

    def execute(self, query, params=None):
        conn = None
        result = None

        try:
            conn = self.connection_pool.getconn()
            with conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)

                if query.strip().upper().startswith('SELECT'):
                    result = cur.fetchall()
                else:
                    result = cur.rowcount

            conn.commit()

        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            if conn:
                conn.rollback()

        finally:
            if conn:
                self.connection_pool.putconn(conn)

        return result
