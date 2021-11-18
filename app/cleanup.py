import json
import structlog


logger = structlog.get_logger()


def process(receipt_str: str):

    logger.info(f"This Function was triggered by the PubSub message: {receipt_str}")

    data_dict = json.loads(receipt_str)

    dataset = data_dict['dataset']
    key = dataset.split('|', 1)[1]

    file_location = key.replace('|', '/')
    bind_contextvars(file=file_location)
    logger.info('Extracted file from message')

    if 'comments' in file_location:
        delete_old_comments()

    elif 'seft' in file_location:
        file = file_location.split('/')[1].split(':')[0]
        remove_from_bucket(file, SEFT_INPUT_BUCKET)

    else:
        file_name = file_location.split('/')[1]
        # some response have .json suffix that needs to be removed
        file = file_name.split('.')[0]
        remove_from_bucket(file, SURVEY_INPUT_BUCKET)

    remove_from_bucket(file_location, OUTPUT_BUCKET)
    logger.info('Cloud Function executed: SUCCESS')


def remove_from_bucket(folder_and_file: str, bucket_name: str):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(folder_and_file)
    blob.delete()
    logger.info(f"Successfully deleted: {folder_and_file} from {bucket_name}.", file=folder_and_file)


def delete_old_comments():
    logger.info('Checking for old comments')
    d = date.today()
    ninety_days_ago = datetime(d.year, d.month, d.day) - timedelta(days=OLD_COMMENTS)
    comment_kinds = fetch_comment_kinds()

    for kind in comment_kinds:
        query = datastore_client.query(kind=kind)
        query.add_filter("created", "<", ninety_days_ago)
        query.keys_only()
        keys = [entity.key for entity in query.fetch()]
        datastore_client.delete_multi(keys)
        logger.info(f'successfully removed: {keys} from Datastore')


def fetch_comment_kinds() -> list:
    """
        Fetch a list of all comment kinds from datastore.
        Each kind is represented by {survey_id}_{period}
    """
    try:
        query = datastore_client.query(kind="__kind__")
        query.keys_only()
        return [entity.key.id_or_name for entity in query.fetch() if not entity.key.id_or_name.startswith("_")]
    except Exception as e:
        logger.error(f'Datastore error fetching kinds: {e}')
        raise e


def publish_failure(event):
    logger.info(f'Publishing gcs.key to {CLEANUP_FAILURE_TOPIC}')
    publisher = pubsub_v1.PublisherClient()
    cleanup_failure_topic_path = publisher.topic_path(PROJECT_ID, CLEANUP_FAILURE_TOPIC)

    msg_data = base64.b64decode(event['data'])
    future = publisher.publish(cleanup_failure_topic_path, msg_data)
    while not future.done():
        sleep(1)
    logger.info('Published to failure queue')
