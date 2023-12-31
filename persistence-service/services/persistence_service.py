from clients.rds_domain_client import RdsDomainClient
from models.models import ProductDto, SupplierDto, CustomerDto, Product, Supplier, \
    Customer, PurchaseOrderDto, PurchaseOrder, SalesOrderDto, SalesOrder, InventoryDTO, Inventory
from utils.id_generator import IdGenerator


class PersistenceService:
    def __init__(self, db_client: RdsDomainClient):
        self.db_client = db_client

    def persist_product(self, incoming_product: ProductDto) -> Product:
        product_id = IdGenerator.generate_product_id()
        product_to_persist = Product(id=product_id, **incoming_product.__dict__)
        self.db_client.insert_product(product_to_persist)
        return product_to_persist

    def persist_supplier(self, incoming_supplier: SupplierDto) -> Supplier:
        supplier_id = IdGenerator.generate_supplier_id()
        supplier_to_persist = Supplier(id=supplier_id, **incoming_supplier.__dict__)
        self.db_client.insert_supplier(supplier_to_persist)
        return supplier_to_persist

    def persist_customer(self, incoming_customer: CustomerDto) -> Customer:
        customer_id = IdGenerator.generate_customer_id()
        customer_to_persist = Customer(id=customer_id, **incoming_customer.__dict__)
        self.db_client.insert_customer(customer_to_persist)
        return customer_to_persist

    def persist_purchase_order(self, incoming_purchase_order: PurchaseOrderDto) -> PurchaseOrder:
        purchase_order_to_persist = PurchaseOrder(incoming_purchase_order.supplier_id,
                                                  incoming_purchase_order.created_at,
                                                  incoming_purchase_order.order_positions)
        self.db_client.insert_purchase_order(purchase_order_to_persist)
        return purchase_order_to_persist

    def persist_sales_order(self, incoming_sales_order: SalesOrderDto) -> SalesOrder:
        sales_order_id = IdGenerator.generate_sales_order_id()
        sales_order_to_persist = SalesOrder(id=sales_order_id, **incoming_sales_order.__dict__)
        self.db_client.insert_sales_order(sales_order_to_persist)
        return sales_order_to_persist

    def persist_inventory(self, incoming_inventory: InventoryDTO) -> Inventory:
        inventory_id = IdGenerator.generate_inventory_id()
        inventory_to_persist = Inventory(id=inventory_id, **incoming_inventory.__dict__)
        self.db_client.insert_inventory(inventory_to_persist)
        self.db_client.add_qty_received_in_purchase_order_position(incoming_inventory.purchase_order_position_id,
                                                                   incoming_inventory.quantity_received)
        return inventory_to_persist
