from aws_cdk import (
    aws_sns as sns,
    Stack, )
from constructs import Construct


class SnsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.product_scheduled_topic = sns.Topic(self, "NewProductScheduled")
        self.product_persisted_topic = sns.Topic(self, "NewProductPersisted")
