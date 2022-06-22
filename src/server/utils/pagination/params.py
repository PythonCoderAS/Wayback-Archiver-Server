from dataclasses import dataclass
from typing import Optional


@dataclass()
class PaginationParams:
    after: Optional[int] = None
    before: Optional[int] = None
    limit: int = 100

    def __post_init__(self):
        if self.after is None and self.before is None:
            self.after = 0  # Default to after=0 is neither is defined.
