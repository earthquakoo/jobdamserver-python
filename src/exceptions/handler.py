from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.base_exceptions import BaseCustomException


def base_custom_exception_handler(request: Request, exc: BaseCustomException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
