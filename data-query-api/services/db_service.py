from typing import Dict, Any, List

from clients.rds_client import RdsClient


class DbService:

    def __init__(self, rds_client: RdsClient):
        self.rds_client = rds_client
        self.products_table_name = "products"
        self.sales_orders_table_name = "sales_orders"
        self.purchase_orders_table_name = "purchase_orders"
        self.query_pattern = "SELECT * FROM {} WHERE 1=1"

    def fetch_products(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        base_query = self.query_pattern.format(self.products_table_name)
        return self.fetch(base_query, params)

    def fetch_sales_orders(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        base_query = self.query_pattern.format(self.sales_orders_table_name)
        return self.fetch(base_query, params)

    def fetch_purchase_orders(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        base_query = self.query_pattern.format(self.purchase_orders_table_name)
        return self.fetch(base_query, params)

    def fetch(self, base_query: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        query, query_params = self._build_query(base_query, params)
        return self.rds_client.execute_select(query, query_params)

    def _build_query(self, base_query: str, params: Dict[str, Any]) -> (str, List[Any]):
        query = base_query
        query_params = []
        for key, value in params.items():
            query += f" AND {key} = %s"
            query_params.append(value)

        return query, query_params
