import os
import structlog
from app.logger import logging_config
from google.cloud import pubsub_v1, storage
from google.cloud import datastore
from flask import Flask

logging_config()
logger = structlog.get_logger()
project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')


class Config:
    """class to hold required configuration data"""

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id

        self.OUTPUT_BUCKET_NAME = f'{proj_id}-outputs'
        self.OUTPUT_BUCKET = None
        self.SEFT_INPUT_BUCKET_NAME = f'{proj_id}-seft-responses'
        self.SEFT_INPUT_BUCKET = None
        self.SURVEY_INPUT_BUCKET_NAME = f'{proj_id}-survey-responses'
        self.SURVEY_INPUT_BUCKET = None

        self.RECEIPT_SUBSCRIPTION_ID = "dap-receipt-subscription"
        self.RECEIPT_SUBSCRIPTION_PATH = None
        self.RECEIPT_SUBSCRIBER = None
        self.QUARANTINE_TOPIC_ID = "cleanup-failure-topic"
        self.QUARANTINE_TOPIC_PATH = None
        self.QUARANTINE_PUBLISHER = None

        self.DATASTORE_CLIENT = None
        self.COMMENT_EXPIRY_IN_DAYS = 90


CONFIG = Config(project_id)


def cloud_config():
    """
    Loads configuration required for running against GCP based environments

    This function makes calls to GCP native tools such as Google PubSub
    and therefore should not be called in situations where these connections are
    not possible, e.g running the unit tests locally.
    """
    logger.info('Loading cloud config')

    storage_client = storage.Client(CONFIG.PROJECT_ID)
    CONFIG.OUTPUT_BUCKET = storage_client.bucket(CONFIG.OUTPUT_BUCKET_NAME)
    CONFIG.SEFT_INPUT_BUCKET = storage_client.bucket(CONFIG.SEFT_INPUT_BUCKET_NAME)
    CONFIG.SURVEY_INPUT_BUCKET = storage_client.bucket(CONFIG.SURVEY_INPUT_BUCKET_NAME)

    receipt_subscriber = pubsub_v1.SubscriberClient()
    CONFIG.RECEIPT_SUBSCRIBER = receipt_subscriber
    CONFIG.RECEIPT_SUBSCRIPTION_PATH = receipt_subscriber.subscription_path(CONFIG.PROJECT_ID, CONFIG.RECEIPT_SUBSCRIPTION_ID)

    # quarantine config
    quarantine_publisher = pubsub_v1.PublisherClient()
    CONFIG.QUARANTINE_TOPIC_PATH = quarantine_publisher.topic_path(CONFIG.PROJECT_ID, CONFIG.QUARANTINE_TOPIC_ID)
    CONFIG.QUARANTINE_PUBLISHER = quarantine_publisher

    CONFIG.DATASTORE_CLIENT = datastore.Client(project=project_id)


app = Flask(__name__)
