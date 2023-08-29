import unittest
from unittest.mock import patch, Mock
import json
from lambda_handler import lambda_handler, provider


class TestLambdaHandler(unittest.TestCase):

    @patch.object(provider, 'get_request_router')
    def test_lambda_handler_success(self, mock_get_request_router):
        mock_request_router = Mock()
        mock_get_request_router.return_value = mock_request_router
        mock_request_router.handle_request.return_value = {"key": "value"}

        event = {"some": "event"}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body']), {"key": "value"})
        mock_request_router.handle_request.assert_called_with(event)

    @patch.object(provider, 'get_request_router')
    def test_lambda_handler_exception(self, mock_get_request_router):
        mock_request_router = Mock()
        mock_get_request_router.return_value = mock_request_router
        mock_request_router.handle_request.side_effect = Exception("some error")

        event = {"some": "event"}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(result['body'], json.dumps('Internal Server Error'))
        mock_request_router.handle_request.assert_called_with(event)
