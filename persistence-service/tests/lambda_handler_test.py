import json
import unittest
from unittest.mock import patch, Mock

from app import lambda_handler, component_provider


class TestLambdaHandler(unittest.TestCase):

    @patch.object(component_provider, 'get_topic_router')
    def test_lambda_handler_success(self, mock_get_topic_router):
        mock_topic_router = Mock()
        mock_get_topic_router.return_value = mock_topic_router
        mock_topic_router.route.return_value = {"statusCode": 200, "body": json.dumps({"key": "value"})}

        event = {"Records": [{"Sns": {"Message": "some_message", "TopicArn": "some_topic"}}]}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(json.loads(result['body']), {"key": "value"})
        mock_topic_router.route.assert_called_with(event)

    @patch.object(component_provider, 'get_topic_router')
    def test_lambda_handler_exception(self, mock_get_topic_router):
        mock_topic_router = Mock()
        mock_get_topic_router.return_value = mock_topic_router
        mock_topic_router.route.side_effect = Exception("some error")

        event = {"Records": [{"Sns": {"Message": "some_message", "TopicArn": "some_topic"}}]}
        context = {}

        with self.assertRaises(Exception) as context:
            lambda_handler(event, context)

        self.assertTrue('some error' in str(context.exception))


