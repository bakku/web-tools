from typing import Literal

from pydantic import UUID4, BaseModel


class HoldingOverview(BaseModel):
    id: UUID4
    description: str
    metal: str
    quantity: float
    purchase_price: float
    purchase_cost: float
    current_value: float
    gain_percent: float
    absolute_gain: float


class PortfolioOverview(BaseModel):
    holdings: list[HoldingOverview]
    total_purchase_cost: float
    total_current_value: float
    total_gain_percent: float
    total_absolute_gain: float


Metal = Literal["Silver", "Gold"]
