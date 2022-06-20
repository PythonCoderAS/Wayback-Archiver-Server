from typing import List

from pydantic import BaseModel

from ..utils.pagination import PaginationResponse


class SessionInput(BaseModel):
    hostname: str


class GeneratedSession(BaseModel):
    session_id: int
    host_id: int
    created_at: float


class SessionListPaginationResponse(PaginationResponse[GeneratedSession]):
    data: List[GeneratedSession]