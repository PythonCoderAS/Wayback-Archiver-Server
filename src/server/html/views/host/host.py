from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from ....views import get_host
from .....models import Host
from .....server import app, templates


@app.get("/host/{id}", response_class=HTMLResponse, include_in_schema=False)
async def host_html(request: Request, id: int):
    host = await get_host(id)
    total = await Host.all().count()
    return templates.TemplateResponse("host.html", context={"host": host, "total": total, "request": request})
