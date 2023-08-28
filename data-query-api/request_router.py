import json
import logging
from typing import Any, Dict

from services.db_service import DbService


class RequestRouter:

    def __init__(self, db_service: DbService):
        self.db_service = db_service
        logging.basicConfig(level=logging.INFO)
        self.routing_table = {
            '/products': self.db_service.fetch_products,
            '/sales_orders': self.db_service.fetch_sales_orders,
            '/purchase_orders': self.db_service.fetch_purchase_orders
        }

    def handle_request(self, event: Dict[str, Any]) -> Dict[str, Any]:
        try:
            path = event.get('path', '')
            params = event.get('queryStringParameters', {})

            handler = self.routing_table.get(path)
            if handler:
                result = handler(params)
                return self._successful_response(result)
            else:
                return self._error_response(404, 'Not Found')
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return self._error_response(500, 'Internal Server Error')

    def _error_response(self, status_code: int, body: str) -> Dict[str, Any]:
        return {
            'statusCode': status_code,
            'body': json.dumps({'error': body})
        }

    def _successful_response(self, body: Any) -> Dict[str, Any]:
        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }
