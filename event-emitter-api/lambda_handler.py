import json
import os

import boto3

sns = boto3.client('sns')

TOPIC_ARN = os.environ['TOPIC_ARN']


def lambda_handler(event, context):
    http_method = event.get("httpMethod", "")

    if http_method != "POST":
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid request method'})
        }
    path = event['path']
    if path == '/purchase-orders':
        subject = 'NEW_PURCHASE_ORDER_SCHEDULED'
    elif path == '/sales-orders':
        subject = 'NEW_SALES_ORDER_SCHEDULED'
    elif path == '/product':
        subject = 'NEW_PRODUCT_SCHEDULED'
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid endpoint'})
        }

    try:
        request_data = json.loads(event['body'])
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON payload'})
        }

    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps(request_data),
        Subject=subject
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Event {subject} published to SNS'})
    }
