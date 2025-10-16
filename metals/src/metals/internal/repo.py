from pydantic import UUID4

from .models import Holding, Portfolio

portfolios: list[Portfolio] = []
holdings: list[Holding] = []


def add_portfolio(portfolio: Portfolio) -> None:
    portfolios.append(portfolio)


def get_portfolio(portfolio_id: UUID4) -> Portfolio | None:
    for portfolio in portfolios:
        if portfolio.id == portfolio_id:
            return portfolio

    return None


def update_portfolio(portfolio: Portfolio) -> None:
    for i, p in enumerate(portfolios):
        if p.id == portfolio.id:
            portfolios[i] = portfolio
            return

    raise ValueError(f"Portfolio with id {portfolio.id} not found")
