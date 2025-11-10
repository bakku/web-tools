import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from metals.internal.persistency.models import Holding, MetalPrice, Portfolio
from metals.internal.types import Metal


def insert_portfolio(session: Session, portfolio: Portfolio) -> Portfolio:
    """
    Insert a new portfolio into the database.

    Args:
        session: Database session for executing the query.
        portfolio: The portfolio to insert.

    Returns:
        The inserted portfolio with its generated ID.
    """
    session.add(portfolio)
    session.commit()
    session.refresh(portfolio)

    return portfolio


def get_portfolio(session: Session, portfolio_id: uuid.UUID) -> Portfolio | None:
    """
    Retrieve a portfolio by ID with all its holdings eagerly loaded.

    Args:
        session: Database session for executing the query.
        portfolio_id: UUID of the portfolio to retrieve.

    Returns:
        The portfolio with its holdings, or None if not found.
    """
    return session.scalars(
        select(Portfolio)
        .where(Portfolio.id == portfolio_id)
        .options(selectinload(Portfolio.holdings))
    ).first()


def update_portfolio(session: Session, portfolio: Portfolio) -> Portfolio:
    """
    Update a portfolio in the database.

    Args:
        session: Database session for executing the query.
        portfolio: The portfolio with updated values.

    Returns:
        The updated portfolio.
    """
    session.commit()
    session.refresh(portfolio)

    return portfolio


def get_holding(
    session: Session, portfolio_id: uuid.UUID, holding_id: uuid.UUID
) -> Holding | None:
    """
    Retrieve a holding by ID within a specific portfolio.

    Args:
        session: Database session for executing the query.
        portfolio_id: UUID of the portfolio containing the holding.
        holding_id: UUID of the holding to retrieve.

    Returns:
        The holding if found, or None if not found or not in the specified portfolio.
    """
    return session.scalars(
        select(Holding).where(
            (Holding.id == holding_id) & (Holding.portfolio_id == portfolio_id)
        )
    ).first()


def update_holding(session: Session, holding: Holding) -> Holding:
    """
    Update a holding in the database.

    Args:
        session: Database session for executing the query.
        holding: The holding with updated values.

    Returns:
        The updated holding.
    """
    session.commit()
    session.refresh(holding)

    return holding


def delete_holding(session: Session, holding: Holding) -> None:
    """
    Delete a holding from the database.

    Args:
        session: Database session for executing the query.
        holding: The holding to delete.
    """
    session.delete(holding)
    session.commit()


def insert_metal_prices_batch(
    session: Session, prices: dict[Metal, float]
) -> list[MetalPrice]:
    """
    Insert multiple metal prices into the database in a single transaction.

    Args:
        session: Database session for executing the query.
        prices: Dictionary mapping each Metal to its price in EUR.

    Returns:
        List of inserted MetalPrice records.
    """
    metal_prices = [
        MetalPrice(metal=metal, price=price) for metal, price in prices.items()
    ]
    session.add_all(metal_prices)
    session.commit()

    return metal_prices


def get_latest_metal_prices(session: Session) -> dict[Metal, float]:
    """
    Retrieve the most recent price for each metal from the database.

    Args:
        session: Database session for executing the query.

    Returns:
        Dictionary mapping each Metal to its most recent price in EUR.
        Returns empty dict if no prices are available.
    """
    subq = (
        select(
            MetalPrice.metal,
            func.max(MetalPrice.created_at).label("max_created_at"),
        )
        .group_by(MetalPrice.metal)
        .subquery()
    )

    stmt = select(MetalPrice).join(
        subq,
        (MetalPrice.metal == subq.c.metal)
        & (MetalPrice.created_at == subq.c.max_created_at),
    )

    results = session.scalars(stmt).all()

    return {result.metal: result.price for result in results}
