from models.models import Product, Supplier, Customer, PurchaseOrder, SalesOrder

from common.clients.rds_client import RdsClient
from common.utils.logger import get_logger

logger = get_logger(__name__)


class RdsDomainClient(RdsClient):

    def insert_product(self, product: Product):
        query = """
        INSERT INTO stock_management.product (id, name, description, safety_stock, max_stock, quantity) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            product.id, product.name, product.description, product.safety_stock, product.max_stock, product.quantity)
        self.execute(query, params)

    def insert_supplier(self, supplier: Supplier):
        query = """
        INSERT INTO stock_management.supplier (id, name) 
        VALUES (%s, %s)
        """
        params = (supplier.id, supplier.name)
        self.execute(query, params)

    def insert_customer(self, customer: Customer):
        query = """
        INSERT INTO stock_management.customer (id, name) 
        VALUES (%s, %s)
        """
        params = (customer.id, customer.name)
        self.execute(query, params)

    def insert_purchase_order(self, purchase_order: PurchaseOrder):
        try:
            query = """
            INSERT INTO stock_management.purchase_order_header (id, supplier_id, created_at) 
            VALUES (%s, %s, %s)
            """
            params = (
                purchase_order.id, purchase_order.supplier_id, purchase_order.created_at)
            self.execute(query, params)

            for position in purchase_order.order_positions:
                self.insert_purchase_order_position(position, purchase_order.id)

            self.commit_transaction(self.connection_pool.getconn())

        except Exception as e:
            logger.error(f"Failed to insert purchase order: {e}")
            self.rollback_transaction(self.connection_pool.getconn())
            raise e

    def insert_purchase_order_position(self, position, purchase_order_id):
        query = """
        INSERT INTO stock_management.purchase_order_position (id, product_id, purchase_order_header_id, quantity_ordered, quantity_received, price, delivery_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            position.id, position.product_id, purchase_order_id, position.quantity_ordered, position.quantity_received,
            position.price, position.delivery_date)
        self.execute(query, params)

    def insert_sales_order(self, sales_order: SalesOrder):  # TODO order positions
        query = """
        INSERT INTO stock_management.sales_order (id, customer_id, created_at) 
        VALUES (%s, %s, %s)
        """
        params = (sales_order.id, sales_order.customer_id, sales_order.created_at)
        self.execute(query, params)
