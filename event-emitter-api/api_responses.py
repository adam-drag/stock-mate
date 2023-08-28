import json

INVALID_REQUEST_METHOD_RESPONSE = {
    'statusCode': 405,
    'body': json.dumps({'message': 'Invalid request method'})
}

INVALID_ENDPOINT_RESPONSE = {
    'statusCode': 404,
    'body': json.dumps({'message': 'Invalid endpoint'})
}

FAILED_TO_PUBLISH_TO_SNS_RESPONSE = {
    'statusCode': 500,
    'body': json.dumps({'message': 'Error publishing to SNS'})
}

SUCCESS_RESPONSE = {
    'statusCode': 200,
    'body': json.dumps({'message': f'Event published to SNS'})
}

INVALID_JSON_PAYLOAD_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps({'message': 'Invalid JSON payload'})
}


def response_with_custom_message(message):
    return {
        'statusCode': 400,
        'body': json.dumps({'message': message})
    }
