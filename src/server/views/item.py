from typing import Optional

from fastapi import HTTPException
from validators import url

from .. import app
from ..models.error import ErrorModel
from ..models.item import GeneratedItem, ItemInput, ItemListPaginationResponse
from ..utils.pagination import PaginationParams, PaginationResponse, apply_pagination_params, validate_pagination
from ...models import Session, SessionItem


@app.get("/api/item/{id}", response_model=GeneratedItem, responses={404: {"model": ErrorModel}})
async def get_item(id: int):
    item = await SessionItem.get_or_none(id=id)
    if item is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    await item.fetch_related("session")
    return GeneratedItem(
        id=item.id,
        session_id=item.session.id,
        host_id=item.session.host_id,
        created_on=item.created_on.timestamp(),
        url=item.url
    )


@app.get("/api/items", response_model=ItemListPaginationResponse, responses={400: {"model": ErrorModel}})
async def get_items(after: int = 0, limit: int = 100, host_id: Optional[int] = None, session_id: Optional[int] = None):
    """
    Gets a list of items.

    - `after`: The ID of the item to start after.
    - `limit`: The maximum number of items to return. Must be less than or equal to 100.
    - `host_id`: The ID of the host to filter by.
    - `session_id`: The ID of the session to filter by.

    Returns a pagination object containing the list of item as well as pagination data.

    - `data`: The list of items.
    - `total`: The total number of items, respecting the `host_id` filter.
    - `limit`: The maximum number of possible entries to return.
    - `next`: The ID value of the last item. This should be provided directly to the `after` query parameter. If
    there is no next item, this will be `null`.

    """
    params = PaginationParams(after=after, limit=limit)
    validate_pagination(params)
    true_base = SessionItem.all()
    if host_id is not None:
        true_base = true_base.filter(session__host_id=host_id)
    if session_id is not None:
        true_base = true_base.filter(session__id=session_id)
    if limit != 0:
        base_qs = apply_pagination_params(true_base, params)
        items = await base_qs.prefetch_related("session")
        generated_items = [
            GeneratedItem(
                id=item.id,
                session_id=item.session.id,
                host_id=item.session.host_id,
                created_on=item.created_on,
                url=item.url
            )
            for item in items
        ]
    else:
        generated_items = []
    count = await true_base.count()
    return PaginationResponse.from_params(params, generated_items, count)


@app.post("/api/item", response_model=GeneratedItem, status_code=201, responses={404: {"model": ErrorModel}, 400: {"model": ErrorModel}})
async def create_item(item_input: ItemInput):
    """
    Create an item.
    """
    # Validate the supplied URL
    if not url(item_input.url):
        raise HTTPException(status_code=400, detail="Invalid URL.")
    session = await Session.get_or_none(id=item_input.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    item = await SessionItem.create(
        session=session,
        url=item_input.url,
    )
    await item.fetch_related("session")
    return GeneratedItem(
        id=item.id,
        session_id=item.session.id,
        host_id=item.session.host_id,
        created_on=item.created_on.timestamp(),
        url=item.url
    )
