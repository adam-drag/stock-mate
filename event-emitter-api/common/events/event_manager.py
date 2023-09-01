import logging
import uuid
from datetime import datetime

from common.clients.rds_client import RdsClient
from common.events.events import EventType
from common.exceptions.failed_to_save_event_exception import FailedToSaveEventException


class EventManager:

    def __init__(self, rds_client: RdsClient = None):
        self.rds_client = rds_client if rds_client else RdsClient()

    def insert_event(self, event_type: EventType, emitter: str, payload: str):
        try:
            event_id = self._generate_unique_event_id()
            insert_query = (
                "INSERT INTO events (event_id, event_type, emitter, payload, created_at) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            params = (event_id, event_type.name, emitter, payload, datetime.now())
            self.rds_client.execute(insert_query, params)
        except Exception as e:
            logging.error(f"Failed to insert event: {e}")
            raise FailedToSaveEventException(e)

    def _generate_unique_event_id(self):
        return f"evnt_{str(uuid.uuid4()).split('-')[-1]}"
