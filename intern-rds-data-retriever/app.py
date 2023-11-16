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
        table_name = event['table_name']
        limit = event.get("limit", 10)
        query = f"SELECT * FROM stock_management.{table_name} LIMIT {limit}"

        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            port=os.environ.get('DB_PORT', '5432'),
            user=username,
            password=password,
            database=os.environ['DB_NAME']
        )
        logger.info(f"Connected to db on {os.environ['DB_HOST']}")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        logger.info(f"Received result {result}")

        def default_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            try:
                return datetime.strptime(obj, '%Y-%m-%d').date()
            except:
                return str(obj)

        return {
            'statusCode': 200,
            'body': json.dumps(result, default=default_serializer)
        }
    except Exception as e:
        traceback.print_stack()
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
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
