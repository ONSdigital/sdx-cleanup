from fastapi import APIRouter, Request, Response, Depends
from sdx_base.models.pubsub import get_message, Message
from starlette.responses import JSONResponse

from app.cleanup import Cleanup
from app.dependencies import get_cleanup

router = APIRouter()


@router.post("/")
async def handle(request: Request, cleanup: Cleanup = Depends(get_cleanup)) -> Response:
    message: Message = await get_message(request)
    cleanup.process(message)
    return Response(status_code=204)


def unrecoverable_error_handler(_: Request, e: Exception) -> Response:
    # Respond with a 200 to ack the message as no point in retrying
    return JSONResponse(content={"error": str(e)}, status_code=200)
