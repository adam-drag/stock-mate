ERROR_MSG = "Only SELECT queries are allowed."


class QueryNotAllowedException(Exception):

    def __init__(self, message=ERROR_MSG, *args):
        super().__init__(message, *args)
