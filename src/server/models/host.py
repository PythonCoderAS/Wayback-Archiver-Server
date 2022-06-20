from typing import List

from pydantic import BaseModel

from ..utils.pagination import PaginationResponse


class HostID(BaseModel):
    id: int


class HostListPaginationResponse(PaginationResponse[HostID]):
    data: List[HostID]
