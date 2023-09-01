import unittest
from datetime import datetime
from unittest.mock import patch

from common.events.event_manager import EventManager
from common.events.events import EventType


class TestEventManager(unittest.TestCase):

    @patch('common.clients.rds_client.RdsClient')
    def setUp(self, mock_rds_client):
        self.mock_rds_client = mock_rds_client
        self.event_manager = EventManager(mock_rds_client)

    def test_insert_event(self):
        with patch('common.events.event_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 1, 1)
            self.event_manager.insert_event(EventType.NewPurchaseOrderScheduled, 'emitter', 'payload')
            self.mock_rds_client.execute.assert_called()
