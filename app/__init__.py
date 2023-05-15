import os

from sdx_gcp.app import get_logger, SdxApp

logger = get_logger()

project_id = os.getenv('PROJECT_ID', 'ons-sdx-sandbox')


class Config:
    """class to hold required configuration data"""

    def __init__(self, proj_id) -> None:
        self.PROJECT_ID = proj_id

        self.OUTPUT_BUCKET_NAME = f'{proj_id}-outputs'
        self.SEFT_INPUT_BUCKET_NAME = f'{proj_id}-seft-responses'
        self.SURVEY_INPUT_BUCKET_NAME = f'{proj_id}-survey-responses'

        self.RECEIPT_SUBSCRIPTION_ID = "dap-receipt-subscription"
        self.QUARANTINE_TOPIC_ID = "cleanup-failure-topic"

        self.COMMENT_EXPIRY_IN_DAYS = 90


CONFIG = Config(project_id)

sdx_app = SdxApp("sdx-cleanup", project_id)
