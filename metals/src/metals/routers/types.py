from pydantic import BaseModel, field_validator

from metals.internal.types import Metal


class HoldingForm(BaseModel):
    description: str
    metal: Metal
    quantity: float
    purchase_price: float

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Description cannot be empty")
        if len(v) > 200:
            raise ValueError("Description cannot exceed 200 characters")
        return v.strip()

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        if v > 1000000:
            raise ValueError("Quantity cannot exceed 1,000,000 oz")
        return v

    @field_validator("purchase_price")
    @classmethod
    def validate_purchase_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Purchase price must be greater than 0")
        if v > 1000000:
            raise ValueError("Purchase price cannot exceed €1,000,000 per oz")
        return v
