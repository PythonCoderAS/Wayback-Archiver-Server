from datetime import datetime
from typing import List

from pydantic import BaseModel

from ..utils.pagination import PaginationResponse


class SessionInput(BaseModel):
    hostname: str


class GeneratedSession(BaseModel):
    session_id: int
    host_id: int
    created_on: datetime


class SessionListPaginationResponse(PaginationResponse[GeneratedSession]):
    data: List[GeneratedSession]
