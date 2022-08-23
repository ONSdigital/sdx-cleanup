import logging
from datetime import date, datetime, timedelta

import structlog

from app import CONFIG

logger = structlog.get_logger()

MAX_ENTITIES = 500


def delete_stale_comments():
    """
    Remove stale comments from datastore.
    A stale comment is one that has existed for longer than CONFIG.COMMENT_EXPIRY_IN_DAYS
    """
    logger.info('Searching for stale comments')
    d = date.today()
    removal_date = datetime(d.year, d.month, d.day) - timedelta(days=CONFIG.COMMENT_EXPIRY_IN_DAYS)
    comment_kinds = fetch_comment_kinds()

    for kind in comment_kinds:

        try:
            query = CONFIG.DATASTORE_CLIENT.query(kind=kind)
            query.add_filter("created", "<", removal_date)
            query.keys_only()
            keys = [entity.key for entity in query.fetch(limit=MAX_ENTITIES)]
            CONFIG.DATASTORE_CLIENT.delete_multi(keys)
            logger.info(f'successfully removed from Datastore', keys=keys)

        except Exception as e:
            logger.error(f"failed to delete for kind {kind}")
            logging.error(str(e))


def fetch_comment_kinds() -> list:
    """
    Fetch a list of all comment kinds from datastore.
    Each kind is represented by {survey_id}_{period}
    """
    try:
        query = CONFIG.DATASTORE_CLIENT.query(kind="__kind__")
        query.keys_only()
        return [entity.key.id_or_name for entity in query.fetch() if not entity.key.id_or_name.startswith("_")]
    except Exception as e:
        logger.error(f'Datastore error fetching kinds: {e}')
        raise e
