import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.metals.internal.types import Metal


class BaseModel(DeclarativeBase):
    pass


class Holding(BaseModel):
    __tablename__ = "holdings"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    description: Mapped[str]
    metal: Mapped[Metal]
    quantity: Mapped[float]
    purchase_price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE")
    )
    portfolio: Mapped[Portfolio] = relationship(back_populates="holdings")


class Portfolio(BaseModel):
    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)

    holdings: Mapped[list[Holding]] = relationship(
        back_populates="portfolio", cascade="all, delete-orphan"
    )
