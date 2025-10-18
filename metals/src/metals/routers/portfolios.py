import uuid

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import UUID4, BaseModel

from ..internal.models import Holding, Metal, Portfolio
from ..internal.prices import get_all_metal_prices_in_eur
from ..internal.repo import add_portfolio, get_portfolio
from .shared import templates

router = APIRouter()


class HoldingDisplayData(BaseModel):
    metal: str
    quantity: float
    purchase_price: float
    purchase_cost: float
    current_value: float
    gain_percent: float
    absolute_gain: float


class PortfolioDisplayData(BaseModel):
    holdings: list[HoldingDisplayData]
    total_purchase_cost: float
    total_current_value: float
    total_gain_percent: float
    total_absolute_gain: float


def calculate_holding_display_data(
    holding: Holding, current_price: float
) -> HoldingDisplayData:
    purchase_cost = holding.quantity * holding.purchase_price
    current_value = holding.quantity * current_price
    absolute_gain = current_value - purchase_cost
    gain_percent = (absolute_gain / purchase_cost * 100) if purchase_cost > 0 else 0.0

    return HoldingDisplayData(
        metal=holding.metal,
        quantity=holding.quantity,
        purchase_price=holding.purchase_price,
        purchase_cost=purchase_cost,
        current_value=current_value,
        gain_percent=gain_percent,
        absolute_gain=absolute_gain,
    )


def calculate_portfolio_display_data(
    portfolio: Portfolio, current_prices: dict[Metal, float]
) -> PortfolioDisplayData:
    holdings_display = [
        calculate_holding_display_data(holding, current_prices[holding.metal])
        for holding in portfolio.holdings
    ]

    total_purchase_cost = sum(h.purchase_cost for h in holdings_display)
    total_current_value = sum(h.current_value for h in holdings_display)
    total_absolute_gain = total_current_value - total_purchase_cost
    total_gain_percent = (
        (total_absolute_gain / total_purchase_cost * 100)
        if total_purchase_cost > 0
        else 0.0
    )

    return PortfolioDisplayData(
        holdings=holdings_display,
        total_purchase_cost=total_purchase_cost,
        total_current_value=total_current_value,
        total_gain_percent=total_gain_percent,
        total_absolute_gain=total_absolute_gain,
    )


@router.post("/p/")
async def portfolios_create() -> RedirectResponse:
    portfolio = Portfolio(id=uuid.uuid4(), holdings=[])

    add_portfolio(portfolio)

    return RedirectResponse(f"/p/{portfolio.id}", status_code=303)


@router.get("/p/{_id}")
async def portfolios_show(_id: UUID4, request: Request) -> HTMLResponse:
    portfolio = get_portfolio(_id)

    if portfolio is None:
        raise HTTPException(status_code=404)

    try:
        current_prices = await get_all_metal_prices_in_eur()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch current metal prices: {str(e)}",
        )

    portfolio_data = calculate_portfolio_display_data(portfolio, current_prices)

    return templates.TemplateResponse(
        "portfolios/show.html.jinja2",
        {"portfolio_id": portfolio.id, "data": portfolio_data, "request": request},
    )
