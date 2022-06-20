from typing import List

from pydantic import BaseModel

from ..utils.pagination import PaginationResponse


class ItemInput(BaseModel):
    session_id: int
    url: str


class GeneratedItem(BaseModel):
    id: int
    session_id: int
    host_id: int
    url: str
    created_at: float


class ItemListPaginationResponse(PaginationResponse[GeneratedItem]):
    data: List[GeneratedItem]
