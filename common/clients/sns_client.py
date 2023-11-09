import json
import logging

import boto3

from common.api_responses import FAILED_TO_PUBLISH_TO_SNS_RESPONSE

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SnsClient:

    def __init__(self, emitter_name, sns_client=None):
        self.sns_client = sns_client if sns_client else boto3.client('sns')
        self.emitter_name = emitter_name

    def send_sns_message(self, topic_arn, message):
        try:
            payload = json.dumps(message)
            self.sns_client.publish(
                TopicArn=topic_arn,
                Message=payload,
            )
        except Exception as e:
            logger.error(f"Error publishing to SNS: {e}")
            return FAILED_TO_PUBLISH_TO_SNS_RESPONSE
