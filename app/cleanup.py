from typing import Protocol, Optional

from sdx_base.models.pubsub import Message

from app import get_logger
from app.comments import CommentDeleter
from app.context import extract_context, FileContext
from app.settings import Settings

logger = get_logger()


class FileDeleter(Protocol):

    def delete(self,
               filename: str,
               bucket_name: str,
               sub_dir: Optional[str] = None,
               project_id: Optional[str] = None) -> bool:
        ...


class Cleanup:

    def __init__(
            self,
            settings: Settings,
            file_deleter: FileDeleter,
            comment_deleter: CommentDeleter):
        self._settings = settings
        self._file_deleter = file_deleter
        self._comment_deleter = comment_deleter

    def process(self, message: Message):
        """Perform the required cleanup based on the information within the receipt

        For all submission types this involves removal from the output bucket.
        Additionally, survey and seft types also require removal from their respective input buckets
        and comment types execute a job to remove stale comments from datastore
        """
        context: FileContext = extract_context(message)

        logger.info(f'Extracted file context from message: {context}')

        # all artifacts require removing from outputs bucket
        self._file_deleter.delete(context["output_path"], self._settings.get_output_bucket_name())

        # special actions depending on type
        if context["survey_type"] == "comments":
            self._comment_deleter.delete_stale_comments()

        elif context["survey_type"] == "seft":
            self._file_deleter.delete(context["input_name"], self._settings.get_seft_bucket_name())

        else:
            self._file_deleter.delete(context["input_name"], self._settings.get_survey_bucket_name())

        logger.info('Cleanup ran successfully')
