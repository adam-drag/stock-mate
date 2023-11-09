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
from lib.schemas import supplier_schema


class SupplierStack(Stack):

    def __init__(self, scope: Construct, id: str, event_bus: events.EventBus, eventbridge_role: iam.Role,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the SupplierModel
        api = apigateway.RestApi(self, "supplierAPI")

        supplier_model = api.add_model(
            "SupplierModel",
            content_type="application/json",
            model_name="SupplierModel",
            schema=apigateway.JsonSchema(**supplier_schema)
        )

        # Create a resource for "supplier"
        supplier_api_resource = api.root.add_resource("supplier")

        # Add a POST method for "supplier" resource
        supplier_api_resource.add_method(
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
                                "DetailType": EventType.NewSupplierScheduled.name,
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
            request_models={"application/json": supplier_model},
            method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_models={"application/json": supplier_model}
                )
            ]
        )
