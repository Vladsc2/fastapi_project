from pydantic import BaseModel, Field


class ItemSlot(BaseModel):
    url: str
    name: str
    count: int
    stack_limit: int

