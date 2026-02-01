import datetime as dt
import uuid

from sqlalchemy import Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from masstimes.internal.types import Church


class BaseModel(DeclarativeBase):
    pass


class Event(BaseModel):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    church: Mapped[Church]
    occurring_at: Mapped[dt.datetime]
    description: Mapped[str]
    created_at: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now(dt.UTC))
    updated_at: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now(dt.UTC), onupdate=dt.datetime.now(dt.UTC)
    )

    __table_args__ = (Index("idx_events_church", "church"),)
