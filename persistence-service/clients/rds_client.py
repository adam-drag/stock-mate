import logging
import os

import psycopg2
from psycopg2 import pool

from models.models import ProductToPersist, SupplierToPersist, CustomerToPersist


class RdsClient:
    def __init__(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=int(os.environ.get('MIN_DB_CONNECTIONS', 1)),
                maxconn=int(os.environ.get('MAX_DB_CONNECTIONS', 10)),
                host=os.environ['DB_HOST'],
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD']
            )
        except Exception as e:
            logging.error(f"Failed to connect to DB: {e}")
            raise e

    def insert_product(self, product: ProductToPersist):
        query = """
        INSERT INTO products (id, name, description, safety_stock, max_stock, quantity) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            product.id, product.name, product.description, product.safety_stock, product.max_stock, product.quantity)
        self._execute(query, params)

    def insert_supplier(self, supplier: SupplierToPersist):
        query = """
        INSERT INTO suppliers (id, name) 
        VALUES (%s, %s)
        """
        params = (supplier.id, supplier.name)
        self._execute(query, params)

    def insert_customer(self, customer: CustomerToPersist):
        query = """
        INSERT INTO customers (id, name) 
        VALUES (%s, %s)
        """
        params = (customer.id, customer.name)
        self._execute(query, params)

    def _execute(self, query, params):
        conn = None
        try:
            conn = self.connection_pool.getconn()
            with conn.cursor() as cur:
                cur.execute(query, params)
            conn.commit()
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                self.connection_pool.putconn(conn)
