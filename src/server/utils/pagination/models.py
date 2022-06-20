from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from .params import PaginationParams

T = TypeVar("T", bound=BaseModel)


class PaginationResponse(BaseModel, Generic[T]):
    """
    A pagination response.
    """

    """The data for the current page."""
    data: T
    """The total number of items available."""
    total: int
    """The number of items per page."""
    limit: int
    """The next offset to use for `after=x`."""
    next: Optional[int] = None

    @classmethod
    def from_params(cls, params: PaginationParams, data: T, total: int) -> "PaginationResponse[T]":
        """
        Create a pagination response from a pagination params.
        """
        retval = cls(
            data=data,
            total=total,
            limit=params.limit,
        )
        if params.after + params.limit < total:
            retval.next = params.after + params.limit
        return retval
