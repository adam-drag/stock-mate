from clients.rds_client import RdsClient
from services.persistence_service import PersistenceService
from services.topic_router import TopicRouter


class ComponentProvider:
    _persistence_service = None
    _topic_router = None
    _rds_client = None

    @staticmethod
    def get_rds_client():
        if ComponentProvider._rds_client is None:
            ComponentProvider._rds_client = RdsClient()
        return ComponentProvider._rds_client

    @staticmethod
    def get_persistence_service():
        if ComponentProvider._persistence_service is None:
            db_client = ComponentProvider.get_rds_client()
            ComponentProvider._persistence_service = PersistenceService(db_client)
        return ComponentProvider._persistence_service

    @staticmethod
    def get_topic_router():
        if ComponentProvider._topic_router is None:
            persistence_service = ComponentProvider.get_persistence_service()
            ComponentProvider._topic_router = TopicRouter(persistence_service)
        return ComponentProvider._topic_router
