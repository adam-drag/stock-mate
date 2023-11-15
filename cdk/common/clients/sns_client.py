import json

import boto3

from common.api_responses import FAILED_TO_PUBLISH_TO_SNS_RESPONSE
from common.utils.logger import get_logger

logger = get_logger(__name__)


class SnsClient:

    def __init__(self, sns_client=None):
        self.sns_client = sns_client if sns_client else boto3.client('sns')

    def send_sns_message(self, topic_arn, message:str):
        try:
            self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
            )
        except Exception as e:
            logger.error(f"Error publishing to SNS: {e}")
            return FAILED_TO_PUBLISH_TO_SNS_RESPONSE
