from datetime import datetime
from typing import List

from pydantic import BaseModel

from ..utils.pagination import PaginationResponse


class SessionInput(BaseModel):
    hostname: str


class GeneratedSession(BaseModel):
    id: int
    host_id: int
    items: int
    created_on: datetime


class SessionListPaginationResponse(PaginationResponse[GeneratedSession]):
    data: List[GeneratedSession]
