from clients.rds_client import RdsClient
from models.models import IncomingProduct, IncomingSupplier, IncomingCustomer, ProductToPersist, SupplierToPersist, \
    CustomerToPersist
from utils.id_generator import IdGenerator


class PersistenceService:
    def __init__(self, db_client: RdsClient):
        self.db_client = db_client

    def persist_product(self, incoming_product: IncomingProduct):
        product_id = IdGenerator.generate_product_id()
        product_to_persist = ProductToPersist(id=product_id, **incoming_product.__dict__)
        self.db_client.insert_product(product_to_persist)

    def persist_supplier(self, incoming_supplier: IncomingSupplier):
        supplier_id = IdGenerator.generate_supplier_id()
        supplier_to_persist = SupplierToPersist(id=supplier_id, **incoming_supplier.__dict__)
        self.db_client.insert_supplier(supplier_to_persist)

    def persist_customer(self, incoming_customer: IncomingCustomer):
        customer_id = IdGenerator.generate_customer_id()
        customer_to_persist = CustomerToPersist(id=customer_id, **incoming_customer.__dict__)
        self.db_client.insert_customer(customer_to_persist)
