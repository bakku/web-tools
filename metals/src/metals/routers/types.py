from pydantic import BaseModel

from ..internal.types import Metal


class HoldingForm(BaseModel):
    description: str
    metal: Metal
    quantity: float
    purchase_price: float
