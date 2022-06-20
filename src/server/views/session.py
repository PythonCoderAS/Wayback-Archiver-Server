from typing import Optional

from fastapi import HTTPException

from .. import app
from ..models import GeneratedSession, SessionInput
from ..models.error import ErrorModel
from ..models.session import SessionListPaginationResponse
from ..utils.pagination import PaginationParams, PaginationResponse, apply_pagination_params, validate_pagination
from ...models import Host, Session


@app.get("/api/session", response_model=GeneratedSession, responses={404: {"model": ErrorModel}})
async def get_session(id: int):
    session = await Session.get_or_none(id=id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    await session.fetch_related("host")
    return GeneratedSession(
        session_id=session.id,
        host_id=session.host.id,
        created_at=session.created_on.timestamp(),
    )


@app.get("/api/sessions", response_model=SessionListPaginationResponse, responses={400: {"model": ErrorModel}})
async def get_sessions(after: int = 0, limit: int = 100, host_id: Optional[int] = None):
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
    params = PaginationParams(after=after, limit=limit)
    validate_pagination(params)
    true_base = Session.all()
    if host_id is not None:
        true_base = true_base.filter(host_id=host_id)
    if limit != 0:
        base_qs = apply_pagination_params(true_base, params)
        sessions = await base_qs.prefetch_related("host")
        generated_sessions = [
            GeneratedSession(
                session_id=session.id,
                host_id=session.host.id,
                created_at=session.created_on.timestamp(),
            )
            for session in sessions
        ]
    else:
        generated_sessions = []
    count = await true_base.count()
    return PaginationResponse.from_params(params, generated_sessions, count)


@app.post("/api/session", response_model=GeneratedSession, status_code=201)
async def create_session(session_input: SessionInput):
    """
    Create a session.
    """
    host, created = await Host.get_or_create(hostname=session_input.hostname)
    session = await Session.create(host=host)
    return GeneratedSession(session_id=session.id, host_id=host.id, created_at=session.created_on.timestamp())
