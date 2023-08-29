import json
import logging

from component_provider import ComponentProvider

logging.basicConfig(level=logging.INFO)

provider = ComponentProvider()


def lambda_handler(event, context):
    try:
        logging.info(f"Received event: {event}")
        request_router = provider.get_request_router()
        response = request_router.handle_request(event)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
