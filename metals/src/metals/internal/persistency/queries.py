import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from metals.internal.persistency.models import Holding, MetalPrice, Portfolio
from metals.internal.types import Metal


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


def insert_metal_price(session: Session, metal: Metal, price: float) -> MetalPrice:
    """Insert a new metal price into the database."""
    metal_price = MetalPrice(metal=metal, price=price)
    session.add(metal_price)
    session.commit()
    session.refresh(metal_price)
    return metal_price


def insert_metal_prices_batch(
    session: Session, prices: dict[Metal, float]
) -> list[MetalPrice]:
    """
    Insert multiple metal prices in a single transaction.

    Args:
        session: Database session
        prices: Dictionary mapping Metal to price

    Returns:
        List of inserted MetalPrice records
    """
    metal_prices = [
        MetalPrice(metal=metal, price=price) for metal, price in prices.items()
    ]
    session.add_all(metal_prices)
    session.commit()

    for metal_price in metal_prices:
        session.refresh(metal_price)

    return metal_prices


def get_latest_metal_price(session: Session, metal: Metal) -> MetalPrice | None:
    """Get the latest price for a specific metal."""
    return session.scalars(
        select(MetalPrice)
        .where(MetalPrice.metal == metal)
        .order_by(MetalPrice.created_at.desc())
        .limit(1)
    ).first()


def get_latest_metal_prices(session: Session) -> dict[Metal, float]:
    """
    Get the latest prices for all metals in a single query.
    Returns:
        Dictionary mapping Metal to price in EUR
    """
    # Use a subquery to get the latest created_at for each metal
    subq = (
        select(
            MetalPrice.metal,
            func.max(MetalPrice.created_at).label("max_created_at"),
        )
        .group_by(MetalPrice.metal)
        .subquery()
    )

    # Join to get the full records with latest created_at
    stmt = select(MetalPrice).join(
        subq,
        (MetalPrice.metal == subq.c.metal)
        & (MetalPrice.created_at == subq.c.max_created_at),
    )

    results = session.scalars(stmt).all()

    return {result.metal: result.price for result in results}
