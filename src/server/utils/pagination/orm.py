from typing import List, TypeVar

from tortoise import Model
from tortoise.queryset import QuerySet

from .extra import HasExtraPage
from .params import PaginationParams

T = TypeVar("T", bound=Model)


def apply_pagination_params(qs: QuerySet[T], params: PaginationParams) -> QuerySet[T]:
    """
    Applies pagination parameters to a query set.

    Precondition: Assumes that all models have an integer primary key `id`.
    """
    # Why are we filtering with params.after/params.before +-1? In order to determine if there is a next/previous page,
    # we need to know if there is more than `limit` items left. For example, if the limit is 100 items, we want to
    # request 102 items, where one of them is one before the limit and one of them is one after the limit.
    # If there are 101 or more items returned, this means that is at least a next page **or** a previous page, but
    # we need to run some checks to determine exactly which type of extra page there is. For example,
    # if there are 101/102 items and the first one is less than `params.after`, we know that there is a previous page.
    # Otherwise, we know that there is a next page. Similarly, if there are 101/102 items and the last one is greater
    # than `params.before`, we know that there is a next page. Otherwise, we know that there is a previous page.
    # A helper function, `determine_next_and_previous`, will return booleans if these are true.
    if params.after:
        qs = qs.filter(id__gt=params.after - 1)
    if params.before:
        qs = qs.filter(id__lt=params.before + 1)
        qs = qs.order_by("-id")
    else:
        qs = qs.order_by("id")
    if params.limit:
        qs = qs.limit(params.limit + 2)
    return qs


def determine_next_and_previous(items: List[T], params: PaginationParams) -> HasExtraPage:
    """
    Determines if there is a next and previous page, using the logic highlighted in
    `apply_pagination_params`.
    """
    item_length = len(items)
    if item_length > params.limit:
        if params.before:
            if items[0].id >= params.before:
                if item_length == params.limit + 2:
                    return HasExtraPage(next_page=True, previous_page=True)
                else:
                    return HasExtraPage(next_page=True, previous_page=False)
            else:
                return HasExtraPage(next_page=False, previous_page=True)
        else:
            if items[0].id <= params.after:
                if item_length == params.limit + 2:
                    return HasExtraPage(next_page=True, previous_page=True)
                else:
                    return HasExtraPage(next_page=False, previous_page=True)
            else:
                return HasExtraPage(next_page=True, previous_page=False)
    else:
        return HasExtraPage(next_page=False, previous_page=False)
