import threading
from concurrent.futures import TimeoutError

import structlog
from google.cloud.pubsub_v1.subscriber.message import Message
from structlog.contextvars import bind_contextvars, clear_contextvars

from app import CONFIG
from app.cleanup import process
from app.quarantine import quarantine_receipt

logger = structlog.get_logger()


def callback(message: Message):
    """
    Manages the life cycle of the received message.
    Handles pre processing events such as setting up logging bindings.
    Extracts the data and passes it on to be processed.
    Handles post processing events such acking the message and
    catching exceptions raised during processing.

    :param message: The message object provided google pubsub
    """
    bind_contextvars(app="SDX-Cleanup")
    bind_contextvars(thread=threading.currentThread().getName())
    try:
        receipt_str = message.data.decode('utf-8')
        process(receipt_str)
        message.ack()
    except Exception as e:
        logger.exception(f"Quarantining receipt: error {str(e)}")
        quarantine_receipt(message, str(e))
        message.ack()
    finally:
        clear_contextvars()


def start():
    """
    Begin listening to the dap receipt pubsub subscription.

    This functions spawns new threads that listen to the subscription topic and
    on receipt of a message invoke the callback function.

    The main thread blocks indefinitely unless the connection times out
    """
    streaming_pull_future = CONFIG.RECEIPT_SUBSCRIBER.subscribe(CONFIG.RECEIPT_SUBSCRIPTION_PATH, callback=callback)
    logger.info(f"Listening for messages on {CONFIG.RECEIPT_SUBSCRIPTION_PATH}..")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with CONFIG.RECEIPT_SUBSCRIBER:
        try:
            # Result() will block indefinitely, unless an exception is encountered first.
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
