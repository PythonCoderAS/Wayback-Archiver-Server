from typing import TypeVar

from tortoise import Model
from tortoise.queryset import QuerySet

from .params import PaginationParams

T = TypeVar("T", bound=Model)


def apply_pagination_params(qs: QuerySet[T], params: PaginationParams) -> QuerySet[T]:
    """
    Applies pagination parameters to a query set.

    Precondition: AsCountes that all models have an integer primary key `id`.
    """
    if params.after:
        qs = qs.filter(id__gt=params.after)
    if params.limit:
        qs = qs.limit(params.limit)
    return qs
