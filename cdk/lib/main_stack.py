import json

from aws_cdk import (
    aws_events as events,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_events_targets as targets,
    Stack,
)
from constructs import Construct

from lib.config import PERSISTENCE_SERVICE_SOURCE_NAME
from lib.customer_stack import CustomerStack
from lib.product_stack import ProductStack
from lib.purchase_order_stack import PurchaseOrderStack
from lib.supplier_stack import SupplierStack



class MainStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        persistence_lambda = _lambda.Function(
            self,
            "PersistenceLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="persistence.handler",
            code=_lambda.Code.from_asset("../persistence-service"),
        )

        event_bus = events.EventBus(self, "MyEventBus")

        archive = events.CfnArchive(
            self,
            "MyEventBusArchive",
            source_arn=event_bus.event_bus_arn,
            archive_name="YourArchiveName",
            description="YourArchiveDescription",
            event_pattern={
                "source": [PERSISTENCE_SERVICE_SOURCE_NAME]
            },
            retention_days=365,  # Optional: Define the retention days
        )

        persistence_service_rule = events.Rule(
            self,
            "PersistenceServiceRule",
            event_bus=event_bus,
            event_pattern=events.EventPattern(source=[PERSISTENCE_SERVICE_SOURCE_NAME]),
        )

        persistence_service_rule.add_target(targets.LambdaFunction(persistence_lambda))

        eventbridge_role = iam.Role(
            self,
            "EventBridgeRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
            inline_policies={
                "EventBridgePolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["events:PutEvents"],
                            resources=[event_bus.event_bus_arn],
                        )
                    ]
                )
            },
        )

        product_stack = ProductStack(self, "ProductStack", event_bus, eventbridge_role)
        supplier_stack = SupplierStack(self, "SupplierStack", event_bus, eventbridge_role)
        customer_stack = CustomerStack(self, "CustomerStack", event_bus, eventbridge_role)
        purchase_order_stack = PurchaseOrderStack(self, "PurchaseOrderStack", event_bus, eventbridge_role)
