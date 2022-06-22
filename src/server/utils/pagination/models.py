from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

from .params import PaginationParams
from .extra import HasExtraPage

T = TypeVar("T", bound=BaseModel)


class PaginationResponse(BaseModel, Generic[T]):
    """
    A pagination response.
    """

    """The data for the current page."""
    data: List[T]
    """The total number of items available."""
    total: int
    """The number of items per page."""
    limit: int
    """The next offset to use for `after=x`."""
    next: Optional[int] = None
    """The previous offset to use for `after=x`."""
    previous: Optional[int] = None

    @classmethod
    def from_params(cls, params: PaginationParams, data: List[T], total: int, extra_pages: HasExtraPage) -> \
            "PaginationResponse[T]":
        """
        Create a pagination response from a pagination params.

        Precondition: data has an integer attribute id.
        """
        data_list = sorted(data, key=lambda x: x.id)
        if extra_pages.next_page and extra_pages.previous_page:
            data_list = data_list[1:-1]
            # When there is both a next and previous page, we know there will be 102
            # items, and so we can easily trim the first and last.
        elif extra_pages.next_page and not extra_pages.previous_page:
            data_list = data_list[:params.limit]
        elif extra_pages.previous_page and not extra_pages.next_page:
            data_list = data_list[-params.limit:]
        retval = cls(
            data=data_list,
            total=total,
            limit=params.limit,
        )
        if extra_pages.next_page:
            retval.next = data_list[-1].id
        if extra_pages.previous_page:
            retval.previous = data_list[0].id
        return retval
