from .. import app
from ..models.error import ErrorModel
from ..models.host import HostID, HostListPaginationResponse
from ..utils.pagination import PaginationParams, PaginationResponse, apply_pagination_params, validate_pagination
from ...models import Host


@app.get("/api/hosts", response_model=HostListPaginationResponse, responses={400: {"model": ErrorModel}})
async def get_hosts(after: int = 0, limit: int = 100):
    params = PaginationParams(after=after, limit=limit)
    validate_pagination(params)
    true_base = Host.all()
    if limit != 0:
        base_qs = apply_pagination_params(true_base, params)
        hosts = await base_qs
        host_data = [
            HostID(
                id=host.id
            )
            for host in hosts
        ]
    else:
        host_data = []
    count = await true_base.count()
    return PaginationResponse.from_params(params, host_data, count)
