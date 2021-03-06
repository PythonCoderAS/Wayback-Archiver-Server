from fastapi import HTTPException

from .params import PaginationParams


def validate_pagination(params: PaginationParams, max_limit: int = 100) -> bool:
    if params.limit > max_limit:
        raise HTTPException(400, f"Limit must be less than or equal to {max_limit}.")
    if params.after is not None and params.after < 0:
        raise HTTPException(400, "After must be greater than or equal to 0.")
    if params.before is not None and params.before <= 0:
        raise HTTPException(400, "Before must be greater than 0.")
    if params.limit < 0:
        raise HTTPException(400, "Limit must be greater than or equal to 0.")
    return True
