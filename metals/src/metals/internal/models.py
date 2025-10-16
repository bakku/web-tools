from typing import Literal

from pydantic import UUID4, BaseModel

Metal = Literal["Silver", "Gold"]


class Holding(BaseModel):
    metal: Metal
    quantity: float
    purchase_price: float


class Portfolio(BaseModel):
    id: UUID4
    holdings: list[Holding]
