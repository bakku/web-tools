import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from metals.internal.types import Metal


class BaseModel(DeclarativeBase):
    pass


class MetalPrice(BaseModel):
    __tablename__ = "metal_prices"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    metal: Mapped[Metal]
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    __table_args__ = (
        # Composite index for efficiently finding latest price per metal
        Index("ix_metal_prices_metal_created_at", "metal", "created_at"),
    )


class Holding(BaseModel):
    __tablename__ = "holdings"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    description: Mapped[str]
    metal: Mapped[Metal]
    quantity: Mapped[float]
    purchase_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE")
    )
    portfolio: Mapped[Portfolio] = relationship(back_populates="holdings")


class Portfolio(BaseModel):
    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    holdings: Mapped[list[Holding]] = relationship(
        back_populates="portfolio", cascade="all, delete-orphan"
    )
