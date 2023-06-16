import logging
from datetime import date, datetime, timedelta

from sdx_gcp.app import get_logger

from app import CONFIG, sdx_app

logger = get_logger()

MAX_ENTITIES = 500


def delete_stale_comments():
    """
    Remove stale comments from datastore.
    A stale comment is one that has existed for longer than CONFIG.COMMENT_EXPIRY_IN_DAYS
    """
    logger.info('Searching for stale comments')
    d = date.today()
    removal_date = datetime(d.year, d.month, d.day) - timedelta(days=CONFIG.COMMENT_EXPIRY_IN_DAYS)
    comment_kinds = sdx_app.datastore_fetch_kinds()
    client = sdx_app.datastore_client()

    for kind in comment_kinds:

        try:
            query = client.query(kind=kind)
            query.add_filter("created", "<", removal_date)
            query.keys_only()
            keys = [entity.key for entity in query.fetch(limit=MAX_ENTITIES)]
            client.delete_multi(keys)
            logger.info('successfully removed from Datastore', keys=keys)

        except Exception as e:
            logger.error(f"failed to delete for kind {kind}")
            logging.error(str(e))
