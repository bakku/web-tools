import uuid
from enum import Enum

from pydantic import BaseModel


class Metal(str, Enum):
    SILVER = "Silver"
    GOLD = "Gold"


class HoldingOverview(BaseModel):
    id: uuid.UUID
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
