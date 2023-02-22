import json
import structlog
from google.cloud.exceptions import NotFound
from google.cloud.storage import Bucket
from structlog.contextvars import bind_contextvars

from app import CONFIG
from app.comments import delete_stale_comments

logger = structlog.get_logger()


def process(receipt_str: str):
    """Perform the required cleanup based on the information within the receipt

    For all submission types this involves removal from the output bucket.
    Additionally survey and seft types also require removal from their respective input buckets
    and comment types execute a job to remove stale comments from datastore

    :param receipt_str: The receipt as a String
    """

    logger.info(f"Cleanup triggered by PubSub message: {receipt_str}")

    try:
        data_dict = json.loads(receipt_str)
        dataset = data_dict['dataset']
        file = dataset.split('|', 1)[1]

        # file is of the form: survey/a148ac43-a937-401f-1234-b9bc5c123b5a
        if not file.contains('/'):
            logger.info("Invalid file format, doesn't contain '/'")
            return

        file_type, file_name = file.split('/', 1)
        # bind_contextvars(file_name=file_name, file_type=file_type)
        # logger.info('Extracted filename from message')
        #
        # # all artefacts require removing from outputs bucket
        # remove_from_bucket(file, CONFIG.OUTPUT_BUCKET)
        #
        # # special actions depending on type
        # if file_type == "comments":
        #     delete_stale_comments()
        #
        # elif file_type == "seft":
        #     remove_from_bucket(file_name, CONFIG.SEFT_INPUT_BUCKET)
        #
        # elif file_type == "feedback":
        #     feedback_filename = file_name.split('-fb-')[0]
        #     remove_from_bucket(feedback_filename, CONFIG.SURVEY_INPUT_BUCKET)
        #
        # else:
        #     # dap response have .json suffix that needs to be removed
        #     f = file_name.split('.')[0]
        #     remove_from_bucket(f, CONFIG.SURVEY_INPUT_BUCKET)

        logger.info('Cleanup ran successfully')

    except Exception as e:
        logger.info(e)


def remove_from_bucket(file: str, bucket: Bucket):
    """Remove a file from a bucket

    :param file: The filename and path e.g. survey/a148ac43-a937-401f-1234-b9bc5c123b5a
    :param bucket: A reference to a Bucket object
    """
    try:
        blob = bucket.blob(file)
        blob.delete()
        logger.info(f"Successfully deleted: file from bucket", bucket=bucket.name)
    except NotFound as nf:
        logger.error("Unable to find file in bucket", bucket=bucket.name, error=nf)
