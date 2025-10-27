import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .db import engine
from .models import Holding, Portfolio


def insert_portfolio(portfolio: Portfolio) -> Portfolio:
    with Session(engine) as session:
        session.add(portfolio)
        session.commit()
        session.refresh(portfolio)

    return portfolio


def get_portfolio(portfolio_id: uuid.UUID) -> Portfolio | None:
    with Session(engine) as session:
        return session.scalars(
            select(Portfolio)
            .where(Portfolio.id == portfolio_id)
            .options(selectinload(Portfolio.holdings))
        ).first()


def update_portfolio(portfolio: Portfolio) -> Portfolio:
    with Session(engine) as session:
        merged = session.merge(portfolio)
        session.commit()
        session.refresh(merged)

    return merged


def get_holding(portfolio_id: uuid.UUID, holding_id: uuid.UUID) -> Holding | None:
    with Session(engine) as session:
        return session.scalars(
            select(Holding).where(
                (Holding.id == holding_id) & (Holding.portfolio_id == portfolio_id)
            )
        ).first()


def update_holding(holding: Holding) -> Holding:
    with Session(engine) as session:
        merged = session.merge(holding)
        session.commit()
        session.refresh(merged)

    return merged


def delete_holding(holding: Holding) -> None:
    with Session(engine) as session:
        session.delete(holding)
        session.commit()
