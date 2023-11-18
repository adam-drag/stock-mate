product_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "safety_stock": {"type": ["number", "null"], "minimum": 0},
        "max_stock": {"type": ["number", "null"], "minimum": 0}
    },
    "required": ["name"]
}

supplier_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
    },
    "required": ["name"]
}

purchase_order_position_schema = {
    "type": "object",
    "properties": {
        "product_id": {"type": "string", "minLength": 1},
        "quantity_ordered": {"type": "integer", "minimum": 1},
        "quantity_received": {"type": "integer", "minimum": 0},
        "price": {"type": "number", "minimum": 0},
        "delivery_date": {
            "type": "string",
            "format": "date",
        }
    },
    "required": ["product_id", "quantity_ordered", "price", "delivery_date"],
    "additionalProperties": True
}

purchase_order_schema = {
    "type": "object",
    "properties": {
        "supplier_id": {"type": "string", "minLength": 1},
        "created_at": {"type": "string", "format": "date"},
        "order_positions": {
            "type": "array",
            "items": purchase_order_position_schema,
            "minItems": 1
        }
    },
    "required": ["supplier_id", "created_at", "order_positions"],
    "additionalProperties": True
}

inventory_schema = {
    "type": "object",
    "properties": {
        "product_id": {"type": "string", "minLength": 1},
        "purchase_order_position_id": {"type": "string", "minLength": 1},
        "quantity_received": {"type": "integer", "minimum": 0},
        "received_at": {"type": "string", "format": "date"},
        "created_by": {"type": "string", "minLength": 1},
        "updated_by": {"type": "string", "minLength": 1},
        "comments": {"type": "string"}
    },
    "required": [
        "product_id",
        "purchase_order_position_id",
        "quantity_received",
        "received_at",
        "created_by",
    ],
}
