from typing import Literal

from pydantic import UUID4, BaseModel


class Holding(BaseModel):
    metal: Literal["Silver", "Gold"]
    quantity: float
    purchase_price: float
    currency: Literal["USD", "GBP", "EUR"]


class Portfolio(BaseModel):
    id: UUID4
    holdings: list[Holding]
