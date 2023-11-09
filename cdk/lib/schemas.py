from aws_cdk import aws_apigateway as apigateway

product_schema = {
    "type": apigateway.JsonSchemaType.OBJECT,
    "properties": {
        "product_id": {"type": apigateway.JsonSchemaType.STRING},
        "name": {"type": apigateway.JsonSchemaType.STRING},
        "description": {"type": apigateway.JsonSchemaType.STRING},
        "quantity": {
            "type": apigateway.JsonSchemaType.NUMBER,
            "minimum": 0
        },
        "safety_stock": {
            "type": apigateway.JsonSchemaType.NUMBER,
            "minimum": 0
        },
        "max_stock": {
            "type": apigateway.JsonSchemaType.NUMBER,
            "minimum": 0
        }
    },
    "required": ["product_id", "name"]
}

purchase_order_schema = {
    "type": apigateway.JsonSchemaType.OBJECT,
    "properties": {
        "order_id": {"type": apigateway.JsonSchemaType.STRING},
        "supplier_id": {"type": apigateway.JsonSchemaType.STRING},
        "products": {
            "type": apigateway.JsonSchemaType.ARRAY,
            "items": product_schema
        },
    },
    "required": ["order_id", "supplier_id", "products"]
}

supplier_schema = {
    "type": apigateway.JsonSchemaType.OBJECT,
    "properties": {
        "supplier_id": {"type": apigateway.JsonSchemaType.STRING},
        "name": {"type": apigateway.JsonSchemaType.STRING},
        "contact_email": {"type": apigateway.JsonSchemaType.STRING},
    },
    "required": ["supplier_id", "name"]
}

customer_schema = {
    "type": apigateway.JsonSchemaType.OBJECT,
    "properties": {
        "customer_id": {"type": apigateway.JsonSchemaType.STRING},
        "name": {"type": apigateway.JsonSchemaType.STRING},
        "email": {"type": apigateway.JsonSchemaType.STRING},
    },
    "required": ["customer_id", "name"]
}

sales_order_schema = {
    "title": "SalesOrder",
    "type": "object",
    "properties": {
        "order_id": {"type": "string"},
        "customer_id": {"type": "string"},
        "products": {
            "type": apigateway.JsonSchemaType.ARRAY,
            "items": product_schema
        },
        "total_amount": {"type": "number"},
    },
    "required": ["order_id", "customer_id", "products", "total_amount"],
}
