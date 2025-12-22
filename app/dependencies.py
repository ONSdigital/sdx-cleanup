from fastapi import Depends
from sdx_base.services.datastore import DatastoreService
from sdx_base.services.storage import StorageService

from app.cleanup import Cleanup
from app.comments import CommentDeleter
from app.settings import Settings, get_instance


def get_settings() -> Settings:
    return get_instance()


def get_datastore_service() -> DatastoreService:
    return DatastoreService()


def get_storage_service() -> StorageService:
    return StorageService()


def get_comments_deleter(
    settings: Settings = Depends(get_settings), datastore: DatastoreService = Depends(get_datastore_service)
) -> CommentDeleter:
    return CommentDeleter(settings.project_id, expiry_days=settings.expiry_days, data_store_service=datastore)


def get_cleanup(
    settings: Settings = Depends(get_settings),
    storage_service: StorageService = Depends(get_storage_service),
    comments_deleter: CommentDeleter = Depends(get_comments_deleter)
) -> Cleanup:
    return Cleanup(settings, file_deleter=storage_service, comment_deleter=comments_deleter)
