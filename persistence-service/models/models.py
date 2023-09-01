from dataclasses import dataclass


@dataclass
class ProductDto:
    name: str
    description: str
    safety_stock: int
    max_stock: int
    quantity: int


@dataclass
class Product(ProductDto):
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
