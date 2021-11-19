from app import CONFIG

from google.cloud.pubsub_v1.subscriber.message import Message


def quarantine_receipt(message: Message, error: str):
    """Place receipt on quarantine queue

    :param message: The message provided by google pubsub
    :param error: A description of the error as a String
    """
    data = message.data
    future = CONFIG.QUARANTINE_PUBLISHER.publish(CONFIG.QUARANTINE_TOPIC_PATH, data, error=error)
    return future.result()
