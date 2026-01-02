from fastapi import Request
from sdx_base.models.pubsub import Message, get_message

from app import get_logger
from app.context import extract_context, FileContext

logger = get_logger()


async def get_tx_id(request: Request) -> str:
    logger.info(f"Extracting tx_id from {request}")
    message: Message = await get_message(request)
    context: FileContext = extract_context(message)
    tx_id = context['input_name']
    return tx_id
