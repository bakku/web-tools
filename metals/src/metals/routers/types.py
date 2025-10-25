from pydantic import BaseModel

from ..internal.models import Metal


class HoldingForm(BaseModel):
    description: str
    metal: Metal
    quantity: float
    purchase_price: float
