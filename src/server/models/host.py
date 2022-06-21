from datetime import datetime
from typing import List

from pydantic import BaseModel

from ..utils.pagination import PaginationResponse


class GeneratedHost(BaseModel):
    id: int
    created_on: datetime
    items: int
    sessions: int


class HostListPaginationResponse(PaginationResponse[GeneratedHost]):
    data: List[GeneratedHost]
