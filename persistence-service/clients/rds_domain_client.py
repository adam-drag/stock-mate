from common.clients.rds_client import RdsClient
from common.utils.logger import get_logger
from models.models import Product, Supplier, Customer, PurchaseOrder, SalesOrder, Inventory

logger = get_logger(__name__)


class RdsDomainClient(RdsClient):

    def insert_product(self, product: Product):
        query = """
        INSERT INTO stock_management.product (id, name, description, safety_stock, max_stock) 
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            product.id, product.name, product.description, product.safety_stock, product.max_stock)
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

    def insert_sales_order(self, sales_order: SalesOrder):
        query = """
        INSERT INTO stock_management.sales_order (id, customer_id, created_at) 
        VALUES (%s, %s, %s)
        """
        params = (sales_order.id, sales_order.customer_id, sales_order.created_at)
        self.execute(query, params)

    def insert_inventory(self, inventory: Inventory):
        query = """
        INSERT INTO stock_management.inventory (id, product_id,purchase_order_position_id, quantity_received,
        quantity_available, received_at,created_by, updated_by, comments) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (inventory.id, inventory.product_id, inventory.purchase_order_position_id, inventory.quantity_received,
                  inventory.quantity_received, inventory.received_at, inventory.created_by, inventory.updated_by,
                  inventory.comments)
        self.execute(query, params)

    def add_qty_received_in_purchase_order_position(self, purchase_order_position_id, quantity_received):
        update_query = """
        UPDATE stock_management.purchase_order_position
        SET quantity_received = quantity_received + %s
        WHERE id = %s
        RETURNING quantity_received;
        """

        update_params = (quantity_received, purchase_order_position_id)

        updated_qty_received = self.execute(update_query, update_params)

        if isinstance(updated_qty_received, list):
            updated_qty_received = updated_qty_received[0]

        return updated_qty_received
