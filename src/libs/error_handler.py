import json
import traceback

from starlette import status
from starlette.requests import Request
from starlette.responses import Response


def create_error_response(request: Request, exc: Exception):
    call_stack = traceback.format_exc()
    return Response(
        content=json.dumps(
            {"Exception": str(exc), "Call Stack": call_stack, "API": request.url.path}
        ),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        media_type="application/json",
    )
