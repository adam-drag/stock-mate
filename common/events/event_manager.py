import logging
import uuid
import os
import json

from datetime import datetime

from common.clients.rds_client import RdsClient
from common.clients.sns_client import SnsClient
from common.events.events import EventType
from common.exceptions.failed_to_save_event_exception import FailedToSaveEventException


class EventManager:

    def __init__(self, rds_client: RdsClient = None, sns_client: SnsClient = None):
        self.rds_client = rds_client if rds_client else RdsClient()
        self.sns_client = sns_client if sns_client else SnsClient()
        self.sns_map = {
            EventType.NewProductScheduled: os.environ.get("NEW_PRODUCT_SCHEDULED_SNS_ARN"),
            EventType.NewProductPersisted: os.environ.get("NEW_PRODUCT_PERSISTED_SNS_ARN"),
            EventType.NewSalesOrderScheduled: os.environ.get("NEW_SALES_ORDER_SCHEDULED_SNS_ARN"),
            EventType.NewDeliveryScheduled: os.environ.get("NEW_DELIVERY_SCHEDULED_SNS_ARN"),
            EventType.NewDispatchRequested: os.environ.get("DISPATCH_REQUESTED_SNS_ARN"),
            EventType.UsageUpdateScheduled: os.environ.get("USAGE_UPDATE_SNS_ARN"),
            EventType.NewPurchaseOrderScheduled: os.environ.get("NEW_PURCHASE_ORDER_SCHEDULED_SNS_ARN"),
            EventType.NewPurchaseOrderPersisted: os.environ.get("NEW_PURCHASE_ORDER_PERSISTED_SNS_ARN"),
            EventType.NewSupplierScheduled: os.environ.get("NEW_SUPPLIER_SCHEDULED_SNS_ARN"),
            EventType.NewSupplierPersisted: os.environ.get("NEW_SUPPLIER_PERSISTED_SNS_ARN"),
            EventType.NewCustomerScheduled: os.environ.get("NEW_CUSTOMER_SCHEDULED_SNS_ARN"),
        }

    def send_event(self, payload, event_type: EventType, emitter: str):
        try:
            message = {
                "event_type": event_type.name,
                "payload": payload
            }
            message_json = json.dumps(message)
            sns_arn = self.sns_map.get(event_type)
            self.persist_event(emitter, event_type, message_json)
            self.sns_client.send_sns_message(sns_arn, message_json)
        except Exception as e:
            logging.error(f"Failed to insert event: {e}")
            raise FailedToSaveEventException(e)

    def persist_event(self, emitter, event_type, message):
        event_id = self._generate_unique_event_id()
        insert_query = (
            "INSERT INTO stock_management.events (event_id, event_type, emitter, message, created_at) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        params = (event_id, event_type.name, emitter, message, datetime.now())
        self.rds_client.execute(insert_query, params)

    def _generate_unique_event_id(self):
        return f"evnt_{str(uuid.uuid4()).split('-')[-1]}"
