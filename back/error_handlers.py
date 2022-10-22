from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorMessage(BaseModel):
    message: str


class UniqueObjectException(Exception):
    def __init__(self, fieldname: str):
        self.fieldname = fieldname.capitalize()

    @property
    def message(self):
        return f"{self.fieldname} is not unique!"


async def unique_validation_handler(request: Request, exc: UniqueObjectException):
    return JSONResponse(
        status_code=400,
        content={
            "message": exc.message,
        },
    )
