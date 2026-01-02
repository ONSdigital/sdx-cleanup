import logging
from datetime import date, datetime, timedelta
from typing import Final

from google.cloud.datastore import Client
from sdx_base.services.datastore import DatastoreService

from app import get_logger

logger = get_logger()

MAX_ENTITIES: Final[int] = 500


class CommentDeleter:

    def __init__(self, project_id: str, expiry_days: int, data_store_service: DatastoreService):
        self._project_id = project_id
        self._expiry_days = expiry_days
        self._data_store_service = data_store_service

    def delete_stale_comments(self):
        """
        Remove stale comments from datastore.
        A stale comment is one that has existed for longer than the configured "expiry_days".
        """
        logger.info('Searching for stale comments')
        d = date.today()
        removal_date = datetime(d.year, d.month, d.day) - timedelta(days=self._expiry_days)
        comment_kinds: list[str] = self._data_store_service.fetch_kinds()
        client = Client(project=self._project_id)

        for kind in comment_kinds:

            try:
                query = client.query(kind=kind)
                query.add_filter("created", "<", removal_date)
                query.keys_only()
                keys = [entity.key for entity in query.fetch(limit=MAX_ENTITIES)]
                client.delete_multi(keys)
                logger.info('successfully removed from Datastore', {"keys": keys})

            except Exception as e:
                logger.error(f"failed to delete for kind {kind}")
                logging.error(str(e))
