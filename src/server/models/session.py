from pydantic import BaseModel


class SessionInput(BaseModel):
    hostname: str


class GeneratedSession(BaseModel):
    session_id: int
    host_id: int
    created_at: float
