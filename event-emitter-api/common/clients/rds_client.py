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
                host=f"{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}",
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD']
            )
        except Exception as e:
            logging.error(f"Failed to connect to DB: {e}")
            raise e

    def start_transaction(self):
        return self.connection_pool.getconn()

    def commit_transaction(self, conn):
        try:
            conn.commit()
        except Exception as e:
            logging.error(f"Commit transaction failed: {e}")
            raise e

    def rollback_transaction(self, conn):
        try:
            if conn:
                conn.rollback()
        except Exception as e:
            logging.error(f"Rollback transaction failed: {e}")
            raise e
        finally:
            self.connection_pool.putconn(conn)

    def execute(self, query, params=None, conn=None, commit=True):
        is_conn_from_pool = False

        try:
            if conn is None:
                conn = self.connection_pool.getconn()
                is_conn_from_pool = True

            with conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)

                if query.strip().upper().startswith('SELECT'):
                    result = cur.fetchall()
                else:
                    result = cur.rowcount

                if commit and not query.strip().upper().startswith('SELECT'):
                    self.commit_transaction(conn)

        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            self.rollback_transaction(conn)
            raise e

        finally:
            if is_conn_from_pool:
                self.connection_pool.putconn(conn)

        return result
