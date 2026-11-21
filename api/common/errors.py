import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ..cinemacity.error import CinemaCityError
from ..schemas.common import ErrorResponse

logger = logging.getLogger(__name__)

NOT_FOUND_RESPONSE: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
        'model': ErrorResponse,
        'description': 'Resource not found.',
    },
}
UPSTREAM_ERROR_RESPONSE: dict[int | str, dict[str, Any]] = {
    status.HTTP_502_BAD_GATEWAY: {
        'model': ErrorResponse,
        'description': 'The Cinema City API is unavailable or returned an error.',
    },
}


async def _handle_cinema_city_error(request: Request, exc: Exception) -> JSONResponse:
    logger.warning('Cinema City API error on %s: %s', request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content=ErrorResponse(detail=f'Cinema City API error: {exc}').model_dump(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(CinemaCityError, _handle_cinema_city_error)
