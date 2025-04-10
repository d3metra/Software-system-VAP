from dataclasses import dataclass

from pydantic import BaseModel

class DefaultError(BaseModel):
    detail: str

responses = {
    404: {"description": "Not Found", "model": DefaultError},
}

@dataclass
class HTTPException(Exception):
    status: int
    code: str
    message: str

class InternalServerError(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(500, "INTERNAL_SERVER_ERROR", message)

class NotFound(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(404, "NOT_FOUND", message)

class ValidationError(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(422, "VALIDATION_ERROR", message)