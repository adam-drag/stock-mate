import json
import logging

import psycopg2
from psycopg2.extras import RealDictCursor

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    # Extract the path parameter to decide what data to fetch
    path = event.get('path', '')

    # Initialize DB connection
    conn = None
    try:
        conn = psycopg2.connect(
            host="your_db_host",
            database="your_db_name",
            user="your_db_user",
            password="your_db_password"
        )
    except Exception as e:
        logging.error(f"Failed to connect to DB: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

    # Fetch data based on the path
    if path == '/products':
        return fetch_products(conn)
    elif path == '/sales-orders':
        return fetch_sales_orders(conn)
    elif path == '/purchase-orders':
        return fetch_purchase_orders(conn)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Not Found')
        }


def fetch_products(conn):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
        return {
            'statusCode': 200,
            'body': json.dumps(products)
        }
    except Exception as e:
        logging.error(f"Failed to fetch products: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

# Similarly, implement fetch_sales_orders and fetch_purchase_orders functions
