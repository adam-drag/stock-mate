from common.clients.rds_client import RdsClient
from models.models import Product, Supplier, Customer


class RdsDomainClient(RdsClient):

    def insert_product(self, product: Product):
        query = """
        INSERT INTO products (id, name, description, safety_stock, max_stock, quantity) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            product.id, product.name, product.description, product.safety_stock, product.max_stock, product.quantity)
        self.execute(query, params)

    def insert_supplier(self, supplier: Supplier):
        query = """
        INSERT INTO suppliers (id, name) 
        VALUES (%s, %s)
        """
        params = (supplier.id, supplier.name)
        self.execute(query, params)

    def insert_customer(self, customer: Customer):
        query = """
        INSERT INTO customers (id, name) 
        VALUES (%s, %s)
        """
        params = (customer.id, customer.name)
        self.execute(query, params)
