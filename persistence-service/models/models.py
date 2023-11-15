from dataclasses import dataclass, asdict


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
    quantityOrdered: int
    deliveryDate: str


@dataclass
class PurchaseOrderDto:
    supplier_id: str
    created_at: str
    order_positions: list[OrderPositionDto]


@dataclass
class SalesOrderDto:
    customer_id: str
    created_at: str
    order_positions: list[OrderPositionDto]


@dataclass
class PurchaseOrder(PurchaseOrderDto):
    id: str


@dataclass
class SalesOrder(SalesOrderDto):
    id: str
