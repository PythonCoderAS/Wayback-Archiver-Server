from dataclasses import dataclass


@dataclass()
class HasExtraPage:
    next_page: bool = False
    previous_page: bool = False
