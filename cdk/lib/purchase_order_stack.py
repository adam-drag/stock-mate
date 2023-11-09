import json

from aws_cdk import (
    aws_apigateway as apigateway,
    aws_events as events,
    aws_iam as iam,
    Stack,
)
from constructs import Construct

from common.events.events import EventType
from lib.config import PERSISTENCE_SERVICE_SOURCE_NAME
from lib.schemas import purchase_order_schema


class PurchaseOrderStack(Stack):

    def __init__(self, scope: Construct, id: str, event_bus: events.EventBus, eventbridge_role: iam.Role,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the PurchaseOrderModel
        api = apigateway.RestApi(self, "purchaseOrderAPI")

        purchase_order_model = api.add_model(
            "PurchaseOrderModel",
            content_type="application/json",
            model_name="PurchaseOrderModel",
            schema=apigateway.JsonSchema(**purchase_order_schema)
        )

        # Create a resource for "purchase-order"
        purchase_order_api_resource = api.root.add_resource("purchase-order")

        # Add a POST method for "purchase-order" resource
        purchase_order_api_resource.add_method(
            "POST",
            integration=apigateway.AwsIntegration(
                service="events",
                action="PutEvents",
                options=apigateway.IntegrationOptions(
                    credentials_role=eventbridge_role,
                    request_templates={
                        "application/json": json.dumps({
                            "Entries": [{
                                "Source": PERSISTENCE_SERVICE_SOURCE_NAME,
                                "EventBusName": event_bus.event_bus_name,
                                "DetailType": EventType.NewPurchaseOrderScheduled.name,
                                "Detail": "$input.json('$')"
                            }]
                        })
                    },
                    integration_responses=[
                        apigateway.IntegrationResponse(
                            status_code="200",
                            response_templates={
                                "application/json": '{"result": "Event sent."}'
                            }
                        )
                    ]
                )
            ),
            request_models={"application/json": purchase_order_model},
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_models={"application/json": purchase_order_model}
                )
            ]
        )
