import json

from sdx_gcp import Message, Request, get_message, get_data, TX_ID
from sdx_gcp.app import get_logger

from app import CONFIG, sdx_app
from app.comments import delete_stale_comments

logger = get_logger()


def process(message: Message, tx_id: TX_ID):
    """Perform the required cleanup based on the information within the receipt

    For all submission types this involves removal from the output bucket.
    Additionally, survey and seft types also require removal from their respective input buckets
    and comment types execute a job to remove stale comments from datastore
    """
    data: str = get_data(message)
    logger.info(f"Cleanup triggered by PubSub message with data: {data}")

    file, file_name, file_type = extract_file_filename_and_type(data)

    logger.info('Extracted filename from message')

    # all artifacts require removing from outputs bucket
    sdx_app.gcs_delete(file, CONFIG.OUTPUT_BUCKET_NAME)

    # Some surveys have their survey id prepended to the filename, so we need to remove it in order to delete it
    naughty_survey_ids = ["739", "738", "740"]

    for survey_id in naughty_survey_ids:
        if file_name.startswith(f"{survey_id}-"):
            # Remove the survey id
            file_name = file_name[4:]
            logger.info(f"Using different filename to delete from bucket for survey id: {survey_id}, new filename: {file_name}")
            break

    # special actions depending on type
    if file_type == "comments":
        delete_stale_comments()

    elif file_type == "seft":
        sdx_app.gcs_delete(file_name, CONFIG.SEFT_INPUT_BUCKET_NAME)

    elif file_type == "feedback":
        feedback_filename = file_name.split('-fb-')[0]
        sdx_app.gcs_delete(feedback_filename, CONFIG.SURVEY_INPUT_BUCKET_NAME)

    else:
        # dap response have .json suffix that needs to be removed
        f = file_name.split('.')[0]
        sdx_app.gcs_delete(f, CONFIG.SURVEY_INPUT_BUCKET_NAME)

    logger.info('Cleanup ran successfully')


def extract_file_filename_and_type(receipt_str: str) -> tuple[str, str, str]:
    data_dict = json.loads(receipt_str)
    dataset = data_dict['dataset']
    file = dataset.split('|', 1)[1]

    # file is of the form: survey/a148ac43-a937-401f-1234-b9bc5c123b5a
    if '/' not in file:
        # Pulling information out of the message json
        file_name = data_dict["files"][0]["name"]
        file_type = data_dict['description'].split(' ')[1]
        file = f"{file_type}/{file_name}"
        logger.info(f"Found file type is {file_type}, found file name is {file_name}.")
    else:
        file_type, file_name = file.split('/', 1)

    return file, file_name, file_type


def get_tx_id(req: Request) -> str:
    logger.info(f"Extracting tx_id from {req}")
    message: Message = get_message(req)
    data: str = get_data(message)
    filename = extract_file_filename_and_type(data)[1]
    return filename
