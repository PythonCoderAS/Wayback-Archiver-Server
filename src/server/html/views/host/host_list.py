from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from ....views import get_hosts
from .....server import app, templates


@app.get("/hosts", response_class=HTMLResponse, include_in_schema=False)
async def host_list_html(request: Request, after: int = 0, limit: int = 100):
    data = await get_hosts(after, limit)
    query_params = {"after": after, "limit": limit}
    for key, val in query_params.copy().items():
        if val is None:
            del query_params[key]
    return templates.TemplateResponse("hostlist.html",
                                      context={"query_params": query_params, "data": data, "request": request})
