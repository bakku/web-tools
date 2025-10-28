from metals.internal.persistency.models import Holding, Portfolio
from metals.internal.types import HoldingOverview, Metal, PortfolioOverview


def _calculate_holding_overview(
    holding: Holding, current_price: float
) -> HoldingOverview:
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
