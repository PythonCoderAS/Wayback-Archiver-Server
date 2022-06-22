from typing import Optional

from fastapi import HTTPException
from tortoise.functions import Count

from .. import app
from ..models.error import ErrorModel
from ..models.session import GeneratedSession, SessionInput, SessionListPaginationResponse
from ..utils.pagination import HasExtraPage, PaginationParams, PaginationResponse, apply_pagination_params, \
    determine_next_and_previous, validate_pagination
from ...models import Host, Session


@app.get("/api/session/{id}", response_model=GeneratedSession, responses={404: {"model": ErrorModel}})
async def get_session(id: int):
    session = await Session.get_or_none(id=id).prefetch_related("host").annotate(count=Count("items"))
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    return GeneratedSession(
        id=session.id,
        host_id=session.host_id,
        created_on=session.created_on.timestamp(),
        items=session.count or 0
    )


@app.get("/api/sessions", response_model=SessionListPaginationResponse, responses={400: {"model": ErrorModel}})
async def get_sessions(after: Optional[int] = None, before: Optional[int] = None, limit: int = 100, host_id: Optional[int] = None):
    """
    Gets a list of sessions.

    - `after`: The ID of the session to start after.
    - `limit`: The maximum number of sessions to return. Must be less than or equal to 100.
    - `host_id`: The ID of the host to filter by.

    Returns a pagination object containing the list of sessions as well as pagination data.

    - `data`: The list of sessions.
    - `total`: The total number of sessions, respecting the `host_id` filter.
    - `limit`: The maximum number of possible entries to return.
    - `next`: The ID value of the last item. This should be provided directly to the `after` query parameter. If
    there is no next item, this will be `null`.

    """
    params = PaginationParams(after=after, before=before, limit=limit)
    validate_pagination(params)
    true_base = Session.all()
    if host_id is not None:
        true_base = true_base.filter(host_id=host_id)
    if limit != 0:
        base_qs = apply_pagination_params(true_base, params)
        sessions = await base_qs.prefetch_related("host").annotate(count=Count("items"))
        extra_pages = determine_next_and_previous(sessions, params)
        generated_sessions = [
            GeneratedSession(
                id=session.id,
                host_id=session.host_id,
                created_on=session.created_on.timestamp(),
                items=session.count or 0
            )
            for session in sessions
        ]
    else:
        generated_sessions = []
        extra_pages = HasExtraPage()
    count = await true_base.count()
    return PaginationResponse.from_params(params, generated_sessions, count, extra_pages)


@app.post("/api/session", response_model=GeneratedSession, status_code=201)
async def create_session(session_input: SessionInput):
    """
    Create a session.
    """
    host, created = await Host.get_or_create(hostname=session_input.hostname)
    session = await Session.create(host=host)
    return GeneratedSession(id=session.id, host_id=host.id, created_on=session.created_on.timestamp(), items=0)
