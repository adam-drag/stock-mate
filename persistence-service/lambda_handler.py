from utils.component_provider import ComponentProvider

component_provider = ComponentProvider()


def lambda_handler(event, context):
    topic_router = component_provider.get_topic_router()
    return topic_router.route(event)
