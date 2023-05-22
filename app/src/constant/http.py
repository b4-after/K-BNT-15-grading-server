from enum import Enum


class HTTPStatusCode(Enum):
    OK: int = 200
    NOT_FOUND: int = 404
    UNPROCESSABLE_ENTITY: int = 422
    INTERNAL_SERVER_ERROR: int = 500
