import logging
import uuid
from datetime import datetime

from common.clients.rds_client import RdsClient
from common.clients.sns_client import SnsClient
from common.events.events import EventType
from common.exceptions.failed_to_save_event_exception import FailedToSaveEventException


class EventManager:

    def __init__(self, emitter_name, rds_client: RdsClient = None, sns_client=None):
        self.rds_client = rds_client if rds_client else RdsClient()
        self.sns_client = sns_client if sns_client else SnsClient(emitter_name)

    def send_event(self, sns_arn: str, event_type: EventType, emitter: str, message: str):
        try:
            self.persist_event(emitter, event_type, message)
            self.sns_client.send_sns_message(sns_arn, message)
        except Exception as e:
            logging.error(f"Failed to insert event: {e}")
            raise FailedToSaveEventException(e)

    def persist_event(self, emitter, event_type, message):
        event_id = self._generate_unique_event_id()
        insert_query = (
            "INSERT INTO events (event_id, event_type, emitter, message, created_at) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        params = (event_id, event_type.name, emitter, message, datetime.now())
        self.rds_client.execute(insert_query, params)

    def _generate_unique_event_id(self):
        return f"evnt_{str(uuid.uuid4()).split('-')[-1]}"
