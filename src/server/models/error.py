from pydantic import BaseModel

class ErrorModel(BaseModel):
    """
    An error model.
    """
    detail: str
