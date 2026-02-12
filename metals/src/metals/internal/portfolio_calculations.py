from metals.internal.persistency.models import Holding, Portfolio
from metals.internal.types import HoldingOverview, Metal, PortfolioOverview


def _calculate_holding_overview(
    holding: Holding, current_price: float
) -> HoldingOverview:
    """
    Calculate performance metrics for a single holding.

    Args:
        holding: The holding to calculate metrics for.
        current_price: The current market price of the metal in EUR per troy ounce.

    Returns:
        HoldingOverview containing purchase cost, current value, and gain metrics.
    """
    purchase_cost = holding.quantity * holding.purchase_price
    current_value = holding.quantity * current_price
    absolute_gain = current_value - purchase_cost
    gain_percent = (absolute_gain / purchase_cost * 100) if purchase_cost > 0 else 0.0

    return HoldingOverview(
        id=holding.id,
        description=holding.description,
        metal=holding.metal,
        quantity=holding.quantity,
        purchase_price=holding.purchase_price,
        purchase_cost=purchase_cost,
        current_value=current_value,
        gain_percent=gain_percent,
        absolute_gain=absolute_gain,
    )


def calculate_portfolio_overview(
    portfolio: Portfolio, current_prices: dict[Metal, float]
) -> PortfolioOverview:
    """
    Calculate performance metrics for an entire portfolio.

    Calculates individual holding metrics and aggregates them to provide
    total portfolio value, cost, and gain metrics.

    Args:
        portfolio: The portfolio to calculate metrics for.
        current_prices: Dictionary mapping each Metal to its current price in EUR.

    Returns:
        PortfolioOverview containing all holdings with their metrics and
        aggregated portfolio totals.
    """
    holdings = [
        _calculate_holding_overview(holding, current_prices[holding.metal])
        for holding in portfolio.holdings
    ]

    total_purchase_cost = sum(h.purchase_cost for h in holdings)
    total_current_value = sum(h.current_value for h in holdings)
    total_absolute_gain = total_current_value - total_purchase_cost
    total_gain_percent = (
        (total_absolute_gain / total_purchase_cost * 100)
        if total_purchase_cost > 0
        else 0.0
    )

    return PortfolioOverview(
        holdings=holdings,
        total_purchase_cost=total_purchase_cost,
        total_current_value=total_current_value,
        total_gain_percent=total_gain_percent,
        total_absolute_gain=total_absolute_gain,
    )
