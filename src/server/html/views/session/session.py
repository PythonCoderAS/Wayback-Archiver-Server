from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from ....views import get_session
from .....models import Session
from .....server import app, templates


@app.get("/session/{id}", response_class=HTMLResponse, include_in_schema=False)
async def session_html(request: Request, id: int):
    session = await get_session(id)
    total = await Session.all().count()
    return templates.TemplateResponse("session.html", context={"session": session, "total": total, "request": request})
