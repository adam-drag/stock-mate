from dataclasses import dataclass


@dataclass
class IncomingProduct:
    name: str
    description: str
    safety_stock: int
    max_stock: int
    quantity: int


@dataclass
class ProductToPersist(IncomingProduct):
    id: str


@dataclass
class IncomingSupplier:
    name: str


@dataclass
class SupplierToPersist(IncomingSupplier):
    id: str


@dataclass
class IncomingCustomer:
    name: str


@dataclass
class CustomerToPersist(IncomingCustomer):
    id: str
