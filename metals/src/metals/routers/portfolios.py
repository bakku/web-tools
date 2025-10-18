import uuid

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import UUID4

from ..internal.models import Portfolio
from ..internal.portfolio_calculations import calculate_portfolio_overview
from ..internal.price_cache import get_price_cache
from ..internal.repo import add_portfolio, get_portfolio
from .shared import get_template_context, templates

router = APIRouter()


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
        cache = get_price_cache()
        current_prices = await cache.get_prices()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch current metal prices: {str(e)}",
        )

    portfolio_overview = calculate_portfolio_overview(portfolio, current_prices)

    context = await get_template_context(
        portfolio_id=portfolio.id, data=portfolio_overview, request=request
    )
    return templates.TemplateResponse("portfolios/show.html.jinja2", context)
