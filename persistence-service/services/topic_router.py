import json
import logging

from common.events.events import EventType
from models.models import ProductDto, CustomerDto, SupplierDto, Product, Supplier, Customer, PurchaseOrderDto, \
    SalesOrderDto, PurchaseOrder, SalesOrder
from services.persistence_service import PersistenceService
from services.sns_dispatcher import SnsDispatcher

logging.basicConfig(level=logging.INFO)


class TopicRouter:

    def __init__(self, persistence_service: PersistenceService, sns_dispatcher: SnsDispatcher):
        self.persistence_service = persistence_service
        self.sns_dispatcher = sns_dispatcher
        self.topic_to_handler = {
            EventType.NewProductScheduled.name: self.handle_new_product,
            EventType.NewSupplierScheduled.name: self.handle_new_supplier,
            EventType.NewCustomerScheduled.name: self.handle_new_customer,
            EventType.NewPurchaseOrderScheduled.name: self.handle_new_purchase_order,
            EventType.NewSalesOrderScheduled.name: self.handle_new_sales_order,
        }

    def handle_new_product(self, sns_message):
        incoming_product = ProductDto(**sns_message)
        product: Product = self.persistence_service.persist_product(incoming_product)
        self.sns_dispatcher.dispatch(product.__dict__, EventType.NewProductPersisted)

    def handle_new_supplier(self, sns_message):
        incoming_supplier = SupplierDto(**sns_message)
        supplier: Supplier = self.persistence_service.persist_supplier(incoming_supplier)
        self.sns_dispatcher.dispatch(supplier.__dict__, EventType.NewSupplierPersisted)

    def handle_new_customer(self, sns_message):
        incoming_customer = CustomerDto(**sns_message)
        customer: Customer = self.persistence_service.persist_customer(incoming_customer)
        self.sns_dispatcher.dispatch(customer.__dict__, EventType.NewCustomerPersisted)

    def handle_new_purchase_order(self, sns_message):
        incoming_purchase_order = PurchaseOrderDto(**sns_message)
        purchase_order: PurchaseOrder = self.persistence_service.persist_purchase_order(incoming_purchase_order)
        self.sns_dispatcher.dispatch(purchase_order.__dict__, EventType.NewPurchaseOrderPersisted)

    def handle_new_sales_order(self, sns_message):
        incoming_sales_order = SalesOrderDto(**sns_message)
        sales_order: SalesOrder = self.persistence_service.persist_sales_order(incoming_sales_order)
        self.sns_dispatcher.dispatch(sales_order.__dict__, EventType.NewSalesOrderPersisted)

    def route(self, event):
        for record in event['Records']:
            sns_message = json.loads(record['Sns']['Message'])

            topic_arn = record['Sns']['TopicArn']
            topic_name = topic_arn.split(':')[-1]

            handler = self.topic_to_handler.get(topic_name)

            if handler:
                handler(sns_message)
            else:
                logging.error(f"Unknown topic: {topic_name}")
