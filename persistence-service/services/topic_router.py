import json

from common.events.event_manager import EventManager
from common.events.events import EventType
from common.utils.logger import get_logger
from models.models import ProductDto, CustomerDto, SupplierDto, Product, Supplier, Customer, PurchaseOrderDto, \
    SalesOrderDto, PurchaseOrder, SalesOrder, default_product_dict, InventoryDTO, Inventory
from services.persistence_service import PersistenceService

EMITTER_NAME = "PersistenceService"

logger = get_logger(__name__)


class TopicRouter:

    def __init__(self, persistence_service: PersistenceService, event_manager: EventManager):
        self.persistence_service = persistence_service
        self.event_manager = event_manager
        self.event_type_to_handler = {
            EventType.NewProductScheduled.name: self.handle_new_product,
            EventType.NewSupplierScheduled.name: self.handle_new_supplier,
            EventType.NewCustomerScheduled.name: self.handle_new_customer,
            EventType.NewPurchaseOrderScheduled.name: self.handle_new_purchase_order,
            EventType.NewSalesOrderScheduled.name: self.handle_new_sales_order,
            EventType.NewDeliveryScheduled.name: self.handle_new_delivery
        }

    def handle_new_product(self, sns_message):
        incoming_product = ProductDto(**{**default_product_dict, **sns_message})
        product: Product = self.persistence_service.persist_product(incoming_product)
        self.event_manager.send_event(product.__dict__, EventType.NewProductPersisted, EMITTER_NAME)

    def handle_new_supplier(self, sns_message):
        incoming_supplier = SupplierDto(**sns_message)
        supplier: Supplier = self.persistence_service.persist_supplier(incoming_supplier)
        self.event_manager.send_event(supplier.__dict__, EventType.NewSupplierPersisted, EMITTER_NAME)

    def handle_new_customer(self, sns_message):
        incoming_customer = CustomerDto(**sns_message)
        customer: Customer = self.persistence_service.persist_customer(incoming_customer)
        self.event_manager.send_event(customer.__dict__, EventType.NewCustomerPersisted, EMITTER_NAME)

    def handle_new_purchase_order(self, sns_message):
        incoming_purchase_order = PurchaseOrderDto(**sns_message)
        purchase_order: PurchaseOrder = self.persistence_service.persist_purchase_order(incoming_purchase_order)
        self.event_manager.send_event(purchase_order.__dict__, EventType.NewPurchaseOrderPersisted, EMITTER_NAME)

    def handle_new_sales_order(self, sns_message):
        incoming_sales_order = SalesOrderDto(**sns_message)
        sales_order: SalesOrder = self.persistence_service.persist_sales_order(incoming_sales_order)
        self.event_manager.send_event(sales_order.__dict__, EventType.NewSalesOrderPersisted, EMITTER_NAME)

    def handle_new_delivery(self, sns_message):
        incoming_inventory = InventoryDTO(**sns_message)
        inventory: Inventory = self.persistence_service.persist_inventory(incoming_inventory)
        self.event_manager.send_event(inventory.__dict__, EventType.NewDeliveryPersisted, EMITTER_NAME)

    def route(self, event):
        for record in event['Records']:
            logger.info(f"Processing record:{record}")
            sns_message = json.loads(record['Sns']['Message'])
            logger.info(f"Sns message: {sns_message}")

            handler = self.event_type_to_handler.get(sns_message["event_type"])

            if handler:
                handler(sns_message["payload"])
            else:
                logger.error(f"Unknown event_type: {sns_message['event_type']}")
