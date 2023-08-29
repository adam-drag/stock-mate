import unittest
from unittest.mock import Mock, patch

from models.models import IncomingProduct, IncomingSupplier, IncomingCustomer
from services.persistence_service import PersistenceService


class TestPersistenceService(unittest.TestCase):

    @patch('services.persistence_service.RdsClient')
    @patch('services.persistence_service.IdGenerator')
    def test_persist_product(self, mock_IdGenerator, mock_RdsClient):
        mock_db_client = Mock()
        mock_IdGenerator.generate_product_id.return_value = "prod_123"
        service = PersistenceService(db_client=mock_db_client)

        incoming_product = IncomingProduct(name="Test Product", description="Description", safety_stock=10,
                                           max_stock=100, quantity=50)
        service.persist_product(incoming_product)

        mock_db_client.insert_product.assert_called_once()

    @patch('services.persistence_service.RdsClient')
    @patch('services.persistence_service.IdGenerator')
    def test_persist_supplier(self, mock_IdGenerator, mock_RdsClient):
        mock_db_client = Mock()
        mock_IdGenerator.generate_supplier_id.return_value = "sup_123"
        service = PersistenceService(db_client=mock_db_client)

        incoming_supplier = IncomingSupplier(name="Test Supplier")
        service.persist_supplier(incoming_supplier)

        mock_db_client.insert_supplier.assert_called_once()

    @patch('services.persistence_service.RdsClient')
    @patch('services.persistence_service.IdGenerator')
    def test_persist_customer(self, mock_IdGenerator, mock_RdsClient):
        mock_db_client = Mock()
        mock_IdGenerator.generate_customer_id.return_value = "cus_123"
        service = PersistenceService(db_client=mock_db_client)

        incoming_customer = IncomingCustomer(name="Test Customer")
        service.persist_customer(incoming_customer)

        mock_db_client.insert_customer.assert_called_once()
