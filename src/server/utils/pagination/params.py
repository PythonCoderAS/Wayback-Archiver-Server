from dataclasses import dataclass


@dataclass()
class PaginationParams:
    after: int = 0
    limit: int = 100
