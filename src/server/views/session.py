from .. import app
from ..models import GeneratedSession, SessionInput
from ..utils.pagination import PaginationParams, PaginationResponse, apply_pagination_params, validate_pagination
from ...models import Host, Session


@app.get("/api/session", response_model=GeneratedSession)
async def get_session(id: str):
    session = await Session.get(id=id)
    await session.fetch_related("host")
    return GeneratedSession(
        session_id=session.id,
        host_id=session.host.name,
        created_at=session.created_on.timestamp(),
    )


@app.get("/api/sessions", response_model=PaginationResponse[GeneratedSession])
async def get_sessions(after: int = 0, limit: int = 100):
    params = PaginationParams(after=after, limit=limit)
    validate_pagination(params)
    base_qs = apply_pagination_params(Session.all(), params)
    sessions = await base_qs.prefetch_related("host")
    generated_sessions = [
        GeneratedSession(
            session_id=session.id,
            host_id=session.host.name,
            created_at=session.created_on.timestamp(),
        )
        for session in sessions
    ]
    count = await Session.all().count()
    return PaginationResponse.from_params(params, generated_sessions, count)


@app.post("/api/session", response_model=GeneratedSession)
async def create_session(session_input: SessionInput):
    """
    Create a session.
    """
    host, created = await Host.get_or_create(hostname=session_input.hostname)
    session = await Session.create(host=host)
    return GeneratedSession(session_id=session.id, host_id=host.id, created_at=session.created_on.timestamp())
