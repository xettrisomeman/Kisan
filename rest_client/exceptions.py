from typing import Optional
from fastapi import HTTPException, status
from http import HTTPStatus


class CustomException(HTTPException):
    def __init__(
        self, detail: Optional[str] = None, status_code=status.HTTP_303_SEE_OTHER
    ):
        if not detail:
            status_code = HTTPStatus(status_code)

        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExists(CustomException):
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnauthorizedException(CustomException):
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class NotFoundException(CustomException):
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
