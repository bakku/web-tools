import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .models import Holding, Portfolio


def insert_portfolio(session: Session, portfolio: Portfolio) -> Portfolio:
    session.add(portfolio)
    session.commit()
    session.refresh(portfolio)

    return portfolio


def get_portfolio(session: Session, portfolio_id: uuid.UUID) -> Portfolio | None:
    return session.scalars(
        select(Portfolio)
        .where(Portfolio.id == portfolio_id)
        .options(selectinload(Portfolio.holdings))
    ).first()


def update_portfolio(session: Session, portfolio: Portfolio) -> Portfolio:
    session.commit()
    session.refresh(portfolio)

    return portfolio


def get_holding(
    session: Session, portfolio_id: uuid.UUID, holding_id: uuid.UUID
) -> Holding | None:
    return session.scalars(
        select(Holding).where(
            (Holding.id == holding_id) & (Holding.portfolio_id == portfolio_id)
        )
    ).first()


def update_holding(session: Session, holding: Holding) -> Holding:
    session.commit()
    session.refresh(holding)

    return holding


def delete_holding(session: Session, holding: Holding) -> None:
    session.delete(holding)
    session.commit()
