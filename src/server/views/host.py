from fastapi import HTTPException
from tortoise.functions import Count

from .. import app
from ..models.error import ErrorModel
from ..models.host import GeneratedHost, HostListPaginationResponse
from ..utils.pagination import PaginationParams, PaginationResponse, apply_pagination_params, validate_pagination
from ...models import Host

@app.get("/api/host/{id}", response_model=GeneratedHost, responses={404: {"model": ErrorModel}})
async def get_host(id: int):
    host = await Host.get_or_none(id=id).annotate(count=Count("sessions__items"), session_count=Count("sessions"))
    if host is None:
        raise HTTPException(status_code=404, detail="Host not found.")
    return GeneratedHost(
        id=host.id,
        created_on=host.created_on.timestamp(),
        items=host.count or 0,
        sessions=host.session_count or 0
    )

@app.get("/api/hosts", response_model=HostListPaginationResponse, responses={400: {"model": ErrorModel}})
async def get_hosts(after: int = 0, limit: int = 100):
    params = PaginationParams(after=after, limit=limit)
    validate_pagination(params)
    true_base = Host.all()
    if limit != 0:
        base_qs = apply_pagination_params(true_base, params)
        hosts = await base_qs.annotate(count=Count("sessions__items"), session_count=Count("sessions")).order_by("id")
        host_data = [
            GeneratedHost(
                id=host.id,
                created_on=host.created_on.timestamp(),
                items=host.count or 0,
                sessions=host.session_count or 0
            )
            for host in hosts
        ]
    else:
        host_data = []
    count = await true_base.count()
    return PaginationResponse.from_params(params, host_data, count)
