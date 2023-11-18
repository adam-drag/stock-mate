from aws_cdk import (
    aws_sns as sns,
    Stack, )
from constructs import Construct


class SnsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.product_scheduled_topic = sns.Topic(self, "NewProductScheduled")
        self.product_persisted_topic = sns.Topic(self, "NewProductPersisted")

        self.purchase_order_scheduled_topic = sns.Topic(self, "NewPurchaseOrderScheduled")
        self.purchase_order_persisted_topic = sns.Topic(self, "NewPurchaseOrderPersisted")

        self.supplier_scheduled_topic = sns.Topic(self, "NewSupplierScheduled")
        self.supplier_persisted_topic = sns.Topic(self, "NewSupplierPersisted")

        self.delivery_scheduled_topic = sns.Topic(self, "NewDeliveryScheduled")
        self.delivery_persisted_topic = sns.Topic(self, "NewDeliveryPersisted")
