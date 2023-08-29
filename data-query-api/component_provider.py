from clients.rds_client import RdsClient
from request_router import RequestRouter
from services.db_service import DbService


class ComponentProvider:
    def __init__(self):
        self._db_client = None
        self._db_service = None
        self._request_router = None

    def get_db_client(self):
        if self._db_client is None:
            self._db_client = RdsClient()
        return self._db_client

    def get_db_service(self):
        if self._db_service is None:
            self._db_service = DbService(self.get_db_client())
        return self._db_service

    def get_request_router(self):
        if self._request_router is None:
            self._request_router = RequestRouter(self.get_db_service())
        return self._request_router

    def set_db_client(self, db_client):
        self._db_client = db_client

    def set_db_service(self, db_service):
        self._db_service = db_service

    def set_request_router(self, request_router):
        self._request_router = request_router
