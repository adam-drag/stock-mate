import json
import os

import boto3


class SnsDispatcher:
    def __init__(self):
        self.sns_client = boto3.client('sns')
        self.topic_arn = os.environ.get('TOPIC_ARN')

    def dispatch(self, message, subject):
        self.sns_client.publish(
            TopicArn=self.topic_arn,
            Message=json.dumps(message),
            Subject=subject
        )
