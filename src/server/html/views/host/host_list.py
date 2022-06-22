from typing import Optional

from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from ....views import get_hosts
from .....server import app, templates


@app.get("/hosts", response_class=HTMLResponse, include_in_schema=False)
async def host_list_html(request: Request, after: Optional[int] = None, before: Optional[int] = None, limit: int = 100):
    data = await get_hosts(after, before, limit)
    query_params = {"after": after, "before": before, "limit": limit}
    for key, val in query_params.copy().items():
        if val is None:
            del query_params[key]
    return templates.TemplateResponse("hostlist.html",
                                      context={"query_params": query_params, "data": data, "request": request})
