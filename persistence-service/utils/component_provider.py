from clients.rds_domain_client import RdsDomainClient
from services.persistence_service import PersistenceService
from services.sns_dispatcher import SnsDispatcher
from services.topic_router import TopicRouter


class ComponentProvider:
    _persistence_service = None
    _topic_router = None
    _rds_domain_client = None
    _sns_dispatcher = None

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
            ComponentProvider._topic_router = TopicRouter(persistence_service, ComponentProvider.get_sns_dispatcher())
        return ComponentProvider._topic_router

    @staticmethod
    def get_sns_dispatcher():
        if ComponentProvider._sns_dispatcher is None:
            ComponentProvider._sns_dispatcher = SnsDispatcher()
        return ComponentProvider._sns_dispatcher
