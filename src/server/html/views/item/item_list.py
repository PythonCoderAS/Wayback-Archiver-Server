from typing import Optional

from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from ....views import get_items
from .....server import app, templates


@app.get("/items", response_class=HTMLResponse, include_in_schema=False)
async def item_list_html(request: Request, after: Optional[int] = None, before: Optional[int] = None, limit: int = 100, host_id: Optional[int] = None,
                         session_id: Optional[int] = None):
    data = await get_items(after, before, limit, host_id, session_id)
    query_params = {"after": after, "before": before, "limit": limit, "host_id": host_id, "session_id": session_id}
    for key, val in query_params.copy().items():
        if val is None:
            del query_params[key]
    return templates.TemplateResponse("itemlist.html",
                                      context={"query_params": query_params, "data": data, "request": request})
