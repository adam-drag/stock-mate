import json
import logging

from models.models import ProductDto, CustomerDto, SupplierDto, Product
from services.persistence_service import PersistenceService
from services.sns_dispatcher import SnsDispatcher

logging.basicConfig(level=logging.INFO)


class TopicRouter:

    def __init__(self, persistence_service: PersistenceService, sns_dispatcher: SnsDispatcher):
        self.persistence_service = persistence_service
        self.sns_dispatcher = sns_dispatcher
        self.topic_to_handler = {
            'NewProductTopic': self.handle_new_product,
            'NewSupplierTopic': self.handle_new_supplier,
            'NewCustomerTopic': self.handle_new_customer,
        }

    def handle_new_product(self, sns_message):
        incoming_product = ProductDto(**sns_message)
        product: Product = self.persistence_service.persist_product(incoming_product)
        self.sns_dispatcher.dispatch(product.__dict__, 'NewProductDispatched')

    def handle_new_supplier(self, sns_message):
        incoming_supplier = SupplierDto(**sns_message)
        self.persistence_service.persist_supplier(incoming_supplier)

    def handle_new_customer(self, sns_message):
        incoming_customer = CustomerDto(**sns_message)
        self.persistence_service.persist_customer(incoming_customer)

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
