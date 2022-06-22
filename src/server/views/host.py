from typing import Optional

from fastapi import HTTPException
from tortoise.functions import Count

from .. import app
from ..models.error import ErrorModel
from ..models.host import GeneratedHost, HostListPaginationResponse
from ..utils.pagination import HasExtraPage, PaginationParams, PaginationResponse, apply_pagination_params, \
    determine_next_and_previous, validate_pagination
from ...models import Host


@app.get("/api/host/{id}", response_model=GeneratedHost, responses={404: {"model": ErrorModel}})
async def get_host(id: int):
    host: Host = await Host.get_or_none(id=id).annotate(count=Count("sessions__items"))
    if host is None:
        raise HTTPException(status_code=404, detail="Host not found.")
    session_count = await host.sessions.all().count()
    return GeneratedHost(
        id=host.id,
        created_on=host.created_on.timestamp(),
        items=host.count or 0,
        sessions=session_count or 0
    )


@app.get("/api/hosts", response_model=HostListPaginationResponse, responses={400: {"model": ErrorModel}})
async def get_hosts(after: Optional[int] = None, before: Optional[int] = None, limit: int = 100):
    params = PaginationParams(after=after, before=before, limit=limit)
    validate_pagination(params)
    true_base = Host.all()
    if limit != 0:
        base_qs = apply_pagination_params(true_base, params)
        hosts = await base_qs.annotate(count=Count("sessions__items"))
        extra_pages = determine_next_and_previous(hosts, params)
        ids = {host.id for host in hosts}
        sessions_mapping = {host.id: host.session_count for host in await Host.all().filter(id__in=ids).annotate(
            session_count=Count("sessions"))}
        host_data = [
            GeneratedHost(
                id=host.id,
                created_on=host.created_on.timestamp(),
                items=host.count or 0,
                sessions=sessions_mapping[host.id] or 0
            )
            for host in hosts
        ]
    else:
        host_data = []
        extra_pages = HasExtraPage()
    count = await true_base.count()
    return PaginationResponse.from_params(params, host_data, count, extra_pages)
