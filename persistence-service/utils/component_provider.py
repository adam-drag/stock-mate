from clients.rds_domain_client import RdsDomainClient
from common.events.event_manager import EventManager
from services.persistence_service import PersistenceService
from services.topic_router import TopicRouter


class ComponentProvider:
    _persistence_service = None
    _topic_router = None
    _rds_domain_client = None
    _event_manager = None

    @staticmethod
    def get_rds_domain_client():
        if ComponentProvider._rds_domain_client is None:
            ComponentProvider._rds_domain_client = RdsDomainClient()
        return ComponentProvider._rds_domain_client

    @staticmethod
    def get_persistence_service():
        if ComponentProvider._persistence_service is None:
            db_client = ComponentProvider.get_rds_domain_client()
            ComponentProvider._persistence_service = PersistenceService(db_client)
        return ComponentProvider._persistence_service

    @staticmethod
    def get_topic_router():
        if ComponentProvider._topic_router is None:
            persistence_service = ComponentProvider.get_persistence_service()
            ComponentProvider._topic_router = TopicRouter(persistence_service, ComponentProvider.get_event_manager())
        return ComponentProvider._topic_router

    @staticmethod
    def get_event_manager():
        if ComponentProvider._event_manager is None:
            ComponentProvider._event_manager = EventManager()
        return ComponentProvider._event_manager
