import json
import logging
import os
import sys
import traceback
from datetime import datetime

import boto3
import psycopg2

now = datetime.now()
timestamp = datetime.timestamp(now)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def database_exists(conn, db_name):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
            return cursor.fetchone() is not None
    except Exception as e:
        logger.error(f"Error checking if database exists {e}")
        raise
    finally:
        conn.commit()


def create_database(conn):
    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {os.environ['DB_NAME']};")
        conn.commit()
        logger.info("Database 'stock_mate_main_db' created successfully.")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise
    finally:
        conn.commit()


def get_logger(name):
    """
        Sets log level to INFO for prod.
        For everything else (dev, staging, None), it is DEBUG.
    """
    environment = os.environ.get("APP_ENV")
    if environment == "production":
        desired_log_level = logging.INFO
    else:
        desired_log_level = logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(desired_log_level)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(desired_log_level)

    stdout_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    return logger


logger = get_logger(__name__)


def lambda_handler(event, context):
    try:
        logger.info("Starting lambda")
        secret_string = pull_secret_string()
        secret_dict = json.loads(secret_string)
        username = secret_dict.get("username")
        password = secret_dict.get("password")
        logger.info("Successfully pulled db credentials")

        create_db_if_not_exists(password, username)
        run_sql_statements(password, username)
        return {
            'statusCode': 200,
            'body': 'RDS schema initialization successful!'
        }
    except Exception as e:
        traceback.print_stack()
        return {
            'statusCode': 500,
            'body': f'RDS schema initialization failed. Error: {str(e)}'
        }


def pull_secret_string():
    secret_name = os.environ.get("DB_SECRET_NAME", "DBSecretD58955BC-UVVkK4RmuFL7")
    client = boto3.client('secretsmanager')
    logger.info(f"Pulling secret: {secret_name}")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        logger.info("received response from secret manager")
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise e
    secret_string = response['SecretString']
    return secret_string


def run_sql_statements(password, username):
    sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ.get('DB_PORT', '5432'),
        user=username,
        password=password,
        database=os.environ['DB_NAME']
    )
    logger.info(f"Connected to db on {os.environ['DB_HOST']}")
    cursor = conn.cursor()
    with open(sql_file_path, "r") as sql_file:
        sql_commands = sql_file.read().split(";")
        for command in sql_commands:
            logger.info(f"Executing {command}")
            if command.strip():
                cursor.execute(command)
    logger.info("Executing commands")
    conn.commit()
    cursor.close()
    conn.close()


def create_db_if_not_exists(password, username):
    default_conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ.get('DB_PORT', '5432'),
        user=username,
        password=password,
        database='postgres'
    )
    if not database_exists(default_conn, os.environ['DB_NAME']):
        create_database(default_conn)
    default_conn.close()
