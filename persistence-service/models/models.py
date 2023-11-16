from dataclasses import dataclass, asdict

from utils.id_generator import IdGenerator


@dataclass
class ProductDto:
    name: str
    description: str
    safety_stock: int
    max_stock: int
    quantity: int


default_product = ProductDto('', '', 0, 0, 0)
default_product_dict = asdict(default_product)


@dataclass
class Product(ProductDto):
    id: str


@dataclass
class Supplier(ProductDto):
    id: str


@dataclass
class Customer(ProductDto):
    id: str


@dataclass
class SupplierDto:
    name: str


@dataclass
class Supplier(SupplierDto):
    id: str


@dataclass
class CustomerDto:
    name: str


@dataclass
class Customer(CustomerDto):
    id: str


@dataclass
class OrderPositionDto:
    product_id: str
    price: float
    quantity_ordered: int
    quantity_received: int
    delivery_date: str


@dataclass
class PurchaseOrderDto:
    supplier_id: str
    created_at: str
    order_positions: list[OrderPositionDto]


@dataclass
class OrderPosition(OrderPositionDto):
    id: str

    def __init__(self, product_id: str, price: float, quantity_ordered: int, quantity_received: int,
                 delivery_date: str):
        self.id = IdGenerator.generate_order_position_id()
        self.product_id = product_id
        self.price = price
        self.quantity_ordered = quantity_ordered
        self.quantity_received = quantity_received
        self.delivery_date = delivery_date


@dataclass
class SalesOrderDto:
    customer_id: str
    created_at: str
    order_positions: list[OrderPosition]


class PurchaseOrder:
    id: str
    supplier_id: str
    created_at: str
    order_positions: list[OrderPosition]

    def __init__(self, supplier_id: str, created_at: str, order_positions_dto: list[OrderPositionDto]):
        self.id = IdGenerator.generate_purchase_order_id()
        self.supplier_id = supplier_id
        self.created_at = created_at
        self.order_positions = self.transform_order_positions(order_positions_dto)

    def transform_order_positions(self, order_positions_dto_list) -> list[OrderPosition]:
        order_positions_list = []
        for dto in order_positions_dto_list:
            order_positions_list.append(OrderPosition(
                product_id=dto['product_id'],
                price=dto['price'],
                quantity_ordered=dto['quantity_ordered'],
                delivery_date=dto['delivery_date'],
                quantity_received=dto.get('quantity_received', 0)
            ))
            return order_positions_list

@dataclass
class SalesOrder(SalesOrderDto):
    id: str
