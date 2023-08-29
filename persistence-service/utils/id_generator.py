import uuid


class IdGenerator:

    @staticmethod
    def _generate_unique_id():
        return str(uuid.uuid4()).split('-')[-1]

    @staticmethod
    def generate_product_id():
        return "prod_" + IdGenerator._generate_unique_id()

    @staticmethod
    def generate_supplier_id():
        return "sup_" + IdGenerator._generate_unique_id()

    @staticmethod
    def generate_customer_id():
        return "cus_" + IdGenerator._generate_unique_id()
