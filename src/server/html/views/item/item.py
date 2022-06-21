from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from ....views import get_item
from .....models import SessionItem
from .....server import app, templates


@app.get("/item/{id}", response_class=HTMLResponse, include_in_schema=False)
async def item_html(request: Request, id: int):
    item = await get_item(id)
    total = await SessionItem.all().count()
    return templates.TemplateResponse("item.html", context={"item": item, "total": total, "request": request})
